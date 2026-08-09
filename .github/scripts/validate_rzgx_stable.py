#!/usr/bin/env python3
"""Validate the preserved RZGX stable release set without rebuilding firmware."""

from __future__ import annotations

import gzip
import hashlib
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
BUILDS = ROOT / "work" / "builds"

MANIFESTS = (
    BUILDS / "SHA256SUMS-STABLE-02-BETAFPV-0.5D.txt",
    BUILDS / "SHA256SUMS-0.5H.txt",
    BUILDS / "SHA256SUMS-STABLE-04-ER5C-0.5I.txt",
)

ER5_BIN = BUILDS / "RZGX-Rover-ELRS-MVP-0.5I-RADIOMASTER-ER5A-ER5C-V2.bin"
ER5_GZ = ER5_BIN.with_suffix(".bin.gz")
ER5_PRODUCT = b"RadioMaster ER5A/C V2 2.4GHz PWM RX"
ER5_LUA = b"RM ER5A/C V2"
FORBIDDEN_5I_MARKERS = (
    b"4.0.1.5J",
    b"START FIRST",
    b"GAS TO CENTER",
    b"BETAFPV PWM 2.4GHz RX",
    b"BFPV PWM 2G4RX",
    b"DIY_2400_RX_PWMP",
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def validate_manifests() -> None:
    for manifest in MANIFESTS:
        if not manifest.is_file():
            fail(f"missing manifest: {manifest.relative_to(ROOT)}")
        for line_number, raw_line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
            line = raw_line.strip()
            if not line:
                continue
            fields = line.split(maxsplit=1)
            if len(fields) != 2 or not re.fullmatch(r"[0-9a-fA-F]{64}", fields[0]):
                fail(f"invalid SHA-256 line: {manifest.relative_to(ROOT)}:{line_number}")
            artifact = BUILDS / fields[1].lstrip("*")
            if not artifact.is_file():
                fail(f"manifest references missing artifact: {artifact.relative_to(ROOT)}")
            actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
            if actual.lower() != fields[0].lower():
                fail(f"SHA-256 mismatch: {artifact.relative_to(ROOT)}")


def validate_gzip_pairs() -> None:
    for version in ("0.5H", "0.5I"):
        binary = BUILDS / f"RZGX-Rover-ELRS-MVP-{version}-RADIOMASTER-ER5A-ER5C-V2.bin"
        compressed = binary.with_suffix(".bin.gz")
        if gzip.decompress(compressed.read_bytes()) != binary.read_bytes():
            fail(f"gzip payload mismatch: {compressed.relative_to(ROOT)}")


def validate_source_and_binary_identity() -> None:
    version_header = ROOT / "src" / "include" / "rzgx_version.h"
    if 'RZGX_ROVER_FIRMWARE_VERSION "4.0.1.5I"' not in version_header.read_text(encoding="utf-8"):
        fail("source version marker is not 4.0.1.5I")

    data = ER5_BIN.read_bytes()
    if data.count(b"4.0.1.5I") != 1:
        fail("Stable 04 binary must contain exactly one 4.0.1.5I marker")
    if data.count(ER5_PRODUCT) != 1 or data.count(ER5_LUA) != 1:
        fail("Stable 04 binary ER5 target identity is missing or duplicated")
    for marker in FORBIDDEN_5I_MARKERS:
        if marker in data:
            fail(f"Stable 04 binary contains forbidden marker: {marker!r}")


def validate_documentation_contract() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    flashing = (ROOT / "docs" / "FLASHING_AND_CONFIGURATION.md").read_text(encoding="utf-8")
    if "Stable 04 / MVP 0.5I" not in readme:
        fail("README does not identify Stable 04 / MVP 0.5I")
    for target in ("BETAFPV PWM 2.4GHz RX", "RadioMaster ER5A/C V2 2.4GHz PWM RX"):
        if target not in flashing:
            fail(f"flashing guide is missing target: {target}")
    if "| --- | --- | --- |" not in flashing:
        fail("flashing guide target table separator is malformed")


def validate_relative_markdown_links() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    failures: list[str] = []
    for markdown in ROOT.rglob("*.md"):
        if any(part in {".git", ".pio", "node_modules"} for part in markdown.parts):
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            path_part = unquote(target.split("#", 1)[0])
            if path_part and not (markdown.parent / path_part).resolve().exists():
                failures.append(f"{markdown.relative_to(ROOT)} -> {target}")
    if failures:
        fail("broken relative Markdown links:\n  " + "\n  ".join(failures))


def main() -> int:
    checks = (
        validate_manifests,
        validate_gzip_pairs,
        validate_source_and_binary_identity,
        validate_documentation_contract,
        validate_relative_markdown_links,
    )
    try:
        for check in checks:
            check()
            print(f"PASS {check.__name__}")
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("RZGX Stable 04 validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
