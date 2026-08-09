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

ER5_TARGET_PATH = ("radiomaster", "rx_2400", "er5-v2")
ER5_PRODUCT = "RadioMaster ER5A/C V2 2.4GHz PWM RX"
ER5_LUA = "RM ER5A/C V2"
OUTPUT_NAME = "RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin"
FORBIDDEN_BETAFPV_MARKERS = (
    b"BETAFPV PWM 2.4GHz RX",
    b"BFPV PWM 2G4RX",
    b"DIY_2400_RX_PWMP",
)
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


def get_target():
    target = json.loads((SOURCE / "hardware" / "targets.json").read_text(encoding="utf-8"))
    for key in ER5_TARGET_PATH:
        target = target[key]
    if target["platform"] != "esp8285" or target["firmware"] != "Unified_ESP8285_2400_RX":
        raise RuntimeError("Official ER5 target is no longer the expected Unified ESP8285 2.4GHz RX")
    if target["product_name"] != ER5_PRODUCT or target["lua_name"] != ER5_LUA:
        raise RuntimeError("Official ER5 target identity changed")
    return target


def expected_layout(target):
    layout_path = SOURCE / "hardware" / "RX" / target["layout_file"]
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    layout.update(target.get("overlay", {}))
    return layout


def reference_options(path, target):
    data = unpack_firmware(path)
    _, product, lua_name, options, layout = read_metadata(data)
    if product != ER5_PRODUCT or lua_name != ER5_LUA:
        raise RuntimeError(f"ER5 reference target mismatch: {product!r} / {lua_name!r}")
    if layout != expected_layout(target):
        raise RuntimeError("ER5 reference layout differs from the official ER5A/C V2 target")
    if not isinstance(options.get("uid"), list) or len(options["uid"]) != 6:
        raise RuntimeError("ER5 reference does not contain a valid six-byte binding UID")
    return options


def redact_options(options):
    return {
        key: ("<redacted>" if key.lower() in SENSITIVE_OPTION_KEYS else value)
        for key, value in options.items()
    }


def package(reference_path):
    payload = unpack_firmware(BUILD)
    if payload.count(EXPECTED_VERSION) != 1:
        raise RuntimeError("Bare build does not contain exactly one 4.0.1.5I marker")
    for marker in FORBIDDEN_BETAFPV_MARKERS:
        if marker in payload:
            raise RuntimeError(f"Bare build contains forbidden BetaFPV marker: {marker!r}")

    target = get_target()
    options = reference_options(reference_path, target)
    layout_path = SOURCE / "hardware" / "RX" / target["layout_file"]
    output_bin = OUTPUT_DIR / OUTPUT_NAME
    output_gz = output_bin.with_suffix(".bin.gz")
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
    if product != ER5_PRODUCT or lua_name != ER5_LUA:
        raise RuntimeError(f"Packaged target identity mismatch: {product!r} / {lua_name!r}")
    if packaged_options != options:
        raise RuntimeError("Packaged ER5 options differ from the original ER5 reference")
    if layout != expected_layout(target):
        raise RuntimeError("Packaged hardware layout differs from the official ER5 target")
    if data.count(EXPECTED_VERSION) != 1:
        raise RuntimeError("Packaged image lost or duplicated the 4.0.1.5I marker")
    if b"\xBE\xEF\xCA\xFE" in data[metadata + 2704:]:
        raise RuntimeError("Packaged ER5 image contains an unexpected prior-target marker")
    for marker in FORBIDDEN_BETAFPV_MARKERS:
        if marker in data:
            raise RuntimeError(f"Packaged image contains forbidden BetaFPV marker: {marker!r}")

    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, compresslevel=9, mtime=0) as stream:
        stream.write(data)
    output_gz.write_bytes(compressed.getvalue())
    if gzip.decompress(output_gz.read_bytes()) != data:
        raise RuntimeError("ER5 gzip round-trip failed")

    result = {
        "product": product,
        "lua": lua_name,
        "options": redact_options(packaged_options),
        "uid_matches_reference": packaged_options["uid"] == options["uid"],
        "vbat_range_mv": [layout["vbat_cal_min"], layout["vbat_cal_max"]],
        "metadata_offset": metadata,
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
    parser = argparse.ArgumentParser(description="Package and validate RZGX Rover 0.5I for RadioMaster ER5C V2")
    parser.add_argument(
        "--er5-reference",
        required=True,
        type=Path,
        help="Original ER5 V2 .bin or .bin.gz used only for audited target options and binding UID.",
    )
    args = parser.parse_args()
    package(args.er5_reference)


if __name__ == "__main__":
    main()
