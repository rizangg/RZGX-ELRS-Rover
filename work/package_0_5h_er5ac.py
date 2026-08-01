import argparse
from pathlib import Path

import package_0_5g_1_er5a as package


package.OUTPUT_BIN = package.OUTPUT_DIR / "RZGX-Rover-ELRS-MVP-0.5H-RADIOMASTER-ER5A-ER5C-V2.bin"
package.OUTPUT_GZ = package.OUTPUT_BIN.with_suffix(".bin.gz")
package.EXPECTED_VERSION = b"4.0.1.5H"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Package the shared RadioMaster ER5A/ER5C V2 release 0.5H."
    )
    parser.add_argument(
        "--reference",
        required=True,
        type=Path,
        help="Original ER5 V2 .bin or .bin.gz used only for target options such as binding UID.",
    )
    args = parser.parse_args()

    if not package.BUILD.exists():
        raise FileNotFoundError(f"Build firmware not found: {package.BUILD}")
    options = package.reference_options(args.reference)
    package.configure_firmware(options)
    package.validate_firmware(options)
