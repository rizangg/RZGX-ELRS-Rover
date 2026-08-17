import argparse
import gzip
import hashlib
import io
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
BUILD = SOURCE / ".pio" / "build" / "Unified_ESP8285_2400_RX_via_WIFI" / "firmware.bin"
OUTPUT_DIR = ROOT / "work" / "builds"
EXPECTED_VERSION = b"4.0.1.5I"

BETAFPV_TARGET_PATH = ("betafpv", "rx_2400", "pwmp")
BETAFPV_PRODUCT = "BETAFPV PWM 2.4GHz RX"
BETAFPV_LUA = "BFPV PWM 2G4RX"
BETAFPV_PRIOR_TARGET = "DIY_2400_RX_PWMP"
BETAFPV_OPTIONS = {
    "uid": [206, 45, 75, 19, 81, 15],
    "wifi-on-interval": 60,
    "rcvr-uart-baud": 420000,
    "lock-on-first-connection": True,
    "flash-discriminator": 465315751,
}

ER5_TARGET_PATH = ("radiomaster", "rx_2400", "er5-v2")
ER5_PRODUCT = "RadioMaster ER5A/C V2 2.4GHz PWM RX"
ER5_LUA = "RM ER5A/C V2"

SENSITIVE_OPTION_KEYS = {
    "uid",
    "wifi-ssid",
    "wifi-password",
    "home-wifi-ssid",
    "home-wifi-password",
}


sys.path.insert(0, str(SOURCE / "python"))
import UnifiedConfiguration  # noqa: E402


def unpack_firmware(path):
    payload = path.read_bytes()
    if payload[:2] == b"\x1f\x8b":
        payload = gzip.decompress(payload)
    if not payload or payload[0] != 0xE9:
        raise RuntimeError(f"Not an ESP8266/ESP8285 firmware image: {path}")
    return payload


def read_c_string(data, offset, size):
    return data[offset:offset + size].split(b"\0", 1)[0].decode("utf-8")


def read_metadata(data):
    metadata = UnifiedConfiguration.findFirmwareEnd(io.BytesIO(data))
    product = read_c_string(data, metadata, 128)
    lua_name = read_c_string(data, metadata + 128, 16)
    options = json.loads(read_c_string(data, metadata + 144, 512))
    layout = json.loads(read_c_string(data, metadata + 656, 2048))
    return metadata, product, lua_name, options, layout


def get_target(path):
    target = json.loads((SOURCE / "hardware" / "targets.json").read_text(encoding="utf-8"))
    for key in path:
        target = target[key]
    if target["platform"] != "esp8285" or target["firmware"] != "Unified_ESP8285_2400_RX":
        raise RuntimeError(f"Target {path} is no longer the expected ESP8285 Unified 2.4GHz RX")
    return target


def expected_layout(target):
    layout_path = SOURCE / "hardware" / "RX" / target["layout_file"]
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    layout.update(target.get("overlay", {}))
    return layout


def reference_er5_options(path):
    data = unpack_firmware(path)
    _, product, lua_name, options, layout = read_metadata(data)
    target = get_target(ER5_TARGET_PATH)
    if product != ER5_PRODUCT or lua_name != ER5_LUA:
        raise RuntimeError(f"ER5 reference target mismatch: {product!r} / {lua_name!r}")
    if layout != expected_layout(target):
        raise RuntimeError("ER5 reference layout differs from the official ER5A/C V2 target")
    return options


def redact_options(options):
    return {
        key: ("<redacted>" if key.lower() in SENSITIVE_OPTION_KEYS else value)
        for key, value in options.items()
    }


def package_target(payload, target_path, expected_product, expected_lua, options, output_name,
                   expected_prior_target=None):
    target = get_target(target_path)
    if target["product_name"] != expected_product or target["lua_name"] != expected_lua:
        raise RuntimeError(f"Official target identity mismatch for {target_path}")

    output_bin = OUTPUT_DIR / output_name
    output_gz = output_bin.with_suffix(".bin.gz")
    layout_path = SOURCE / "hardware" / "RX" / target["layout_file"]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_bin.write_bytes(payload)
    with output_bin.open("r+b") as firmware:
        UnifiedConfiguration.appendToFirmware(
            firmware,
            target["product_name"],
            target["lua_name"],
            json.dumps(options, separators=(",", ":")),
            target,
            str(layout_path),
            None,
        )
        firmware.truncate()

    data = output_bin.read_bytes()
    metadata, product, lua_name, packaged_options, layout = read_metadata(data)
    if product != expected_product or lua_name != expected_lua:
        raise RuntimeError(f"Packaged target identity mismatch: {product!r} / {lua_name!r}")
    if packaged_options != options:
        raise RuntimeError(f"Packaged options mismatch for {expected_product}")
    if layout != expected_layout(target):
        raise RuntimeError(f"Packaged hardware layout mismatch for {expected_product}")
    if data.count(EXPECTED_VERSION) != 1:
        raise RuntimeError(f"Packaged {expected_product} image lost the 4.0.1.5I marker")

    marker_prefix = b"\xBE\xEF\xCA\xFE"
    if expected_prior_target is None:
        if marker_prefix in data[metadata + 2704:]:
            raise RuntimeError(f"Unexpected prior-target marker in {expected_product} image")
    else:
        expected_marker = marker_prefix + expected_prior_target.encode() + b"\0"
        if expected_marker not in data[metadata:]:
            raise RuntimeError(f"Expected prior-target marker is missing from {expected_product} image")

    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, compresslevel=9, mtime=0) as stream:
        stream.write(data)
    output_gz.write_bytes(compressed.getvalue())
    if gzip.decompress(output_gz.read_bytes()) != data:
        raise RuntimeError(f"Gzip round-trip failed for {expected_product}")

    result = {
        "product": product,
        "lua": lua_name,
        "options": redact_options(packaged_options),
        "vbat_range_mv": [layout["vbat_cal_min"], layout["vbat_cal_max"]],
        "bin": output_bin,
        "bin_size": len(data),
        "bin_sha256": hashlib.sha256(data).hexdigest(),
        "gz": output_gz,
        "gz_size": output_gz.stat().st_size,
        "gz_sha256": hashlib.sha256(output_gz.read_bytes()).hexdigest(),
    }
    print(json.dumps({key: str(value) if isinstance(value, Path) else value for key, value in result.items()},
                     separators=(",", ":")))
    return result


def main():
    parser = argparse.ArgumentParser(description="Package and validate both RZGX Rover 0.5I receiver targets")
    parser.add_argument(
        "--er5-reference",
        required=True,
        type=Path,
        help="Original ER5 V2 .bin or .bin.gz used only for its audited target options.",
    )
    args = parser.parse_args()

    payload = unpack_firmware(BUILD)
    if payload.count(EXPECTED_VERSION) != 1:
        raise RuntimeError("Bare build does not contain exactly one 4.0.1.5I marker")

    package_target(
        payload,
        BETAFPV_TARGET_PATH,
        BETAFPV_PRODUCT,
        BETAFPV_LUA,
        BETAFPV_OPTIONS,
        "RZGX-Rover-ELRS-MVP-0.5I-BETAFPV-PWM-2G4RX.bin",
        BETAFPV_PRIOR_TARGET,
    )
    package_target(
        payload,
        ER5_TARGET_PATH,
        ER5_PRODUCT,
        ER5_LUA,
        reference_er5_options(args.er5_reference),
        "RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin",
    )


if __name__ == "__main__":
    main()
