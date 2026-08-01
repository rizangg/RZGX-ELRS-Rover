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
OUTPUT_BIN = OUTPUT_DIR / "RZGX-Rover-ELRS-MVP-0.5G.1-RADIOMASTER-ER5A-V2.bin"
OUTPUT_GZ = OUTPUT_BIN.with_suffix(".bin.gz")

TARGET_PATH = ("radiomaster", "rx_2400", "er5-v2")
EXPECTED_PRODUCT = "RadioMaster ER5A/C V2 2.4GHz PWM RX"
EXPECTED_LUA = "RM ER5A/C V2"
EXPECTED_VERSION = b"4.0.1.5G"
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
    targets = json.loads((SOURCE / "hardware" / "targets.json").read_text(encoding="utf-8"))
    target = targets
    for key in TARGET_PATH:
        target = target[key]
    if target["product_name"] != EXPECTED_PRODUCT or target["lua_name"] != EXPECTED_LUA:
        raise RuntimeError("Official target identity does not match RadioMaster ER5A/C V2")
    if target["platform"] != "esp8285" or target["firmware"] != "Unified_ESP8285_2400_RX":
        raise RuntimeError("Official ER5 V2 target is no longer ESP8285 Unified 2.4GHz RX")
    return target


def expected_layout(target):
    layout_path = SOURCE / "hardware" / "RX" / target["layout_file"]
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    layout.update(target.get("overlay", {}))
    return layout


def reference_options(path):
    data = unpack_firmware(path)
    _, product, lua_name, options, layout = read_metadata(data)
    if product != EXPECTED_PRODUCT or lua_name != EXPECTED_LUA:
        raise RuntimeError(f"Reference firmware target mismatch: {product!r} / {lua_name!r}")

    target = get_target()
    if layout != expected_layout(target):
        raise RuntimeError("Reference firmware hardware layout differs from the official ER5 V2 target")
    return options


def redact_options(options):
    return {
        key: ("<redacted>" if key.lower() in SENSITIVE_OPTION_KEYS else value)
        for key, value in options.items()
    }


def configure_firmware(options):
    payload = unpack_firmware(BUILD)
    if payload.count(EXPECTED_VERSION) != 1:
        raise RuntimeError("Bare build is not the audited 4.0.1.5G source build")

    target = get_target()
    layout_path = SOURCE / "hardware" / "RX" / target["layout_file"]
    options_json = json.dumps(options, separators=(",", ":"))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_BIN.write_bytes(payload)
    with OUTPUT_BIN.open("r+b") as firmware:
        UnifiedConfiguration.appendToFirmware(
            firmware,
            target["product_name"],
            target["lua_name"],
            options_json,
            target,
            str(layout_path),
            None,
        )
        firmware.truncate()


def validate_firmware(expected_options):
    data = OUTPUT_BIN.read_bytes()
    metadata, product, lua_name, options, layout = read_metadata(data)
    target = get_target()

    if product != EXPECTED_PRODUCT:
        raise RuntimeError(f"Product mismatch: {product!r}")
    if lua_name != EXPECTED_LUA:
        raise RuntimeError(f"Lua name mismatch: {lua_name!r}")
    if options != expected_options:
        raise RuntimeError("Firmware options differ from the reference ER5 V2 firmware")
    if layout != expected_layout(target):
        raise RuntimeError("Packaged hardware layout differs from the official ER5 V2 target")
    if data.count(EXPECTED_VERSION) != 1:
        raise RuntimeError("Packaged firmware does not contain exactly one 4.0.1.5G version marker")
    if b"\xBE\xEF\xCA\xFE" in data[metadata + 2704:]:
        raise RuntimeError("Unexpected prior-target marker in ER5 V2 firmware")

    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, compresslevel=9, mtime=0) as compressed:
        compressed.write(data)
    OUTPUT_GZ.write_bytes(buffer.getvalue())

    if gzip.decompress(OUTPUT_GZ.read_bytes()) != data:
        raise RuntimeError("Gzip round-trip validation failed")

    print(f"Validated product: {product}")
    print(f"Validated Lua name: {lua_name}")
    print(f"Validated options: {json.dumps(redact_options(options), separators=(',', ':'))}")
    print(f"Validated VBAT range: {layout['vbat_cal_min']}..{layout['vbat_cal_max']} mV")
    print(f"Raw: {OUTPUT_BIN} ({len(data)} bytes)")
    print(f"WiFi: {OUTPUT_GZ} ({OUTPUT_GZ.stat().st_size} bytes)")
    print(f"BIN SHA256: {hashlib.sha256(data).hexdigest()}")
    print(f"GZ SHA256: {hashlib.sha256(OUTPUT_GZ.read_bytes()).hexdigest()}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Package ER5A release 0.5G.1 from the audited 4.0.1.5G source build. "
            "The release suffix is external so the executable remains identical to BETAFPV 0.5G."
        )
    )
    parser.add_argument(
        "--reference",
        required=True,
        type=Path,
        help="Original ER5 V2 .bin or .bin.gz used only for target options such as binding UID.",
    )
    args = parser.parse_args()

    options = reference_options(args.reference)
    configure_firmware(options)
    validate_firmware(options)


if __name__ == "__main__":
    main()
