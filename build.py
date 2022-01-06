# -*- coding: utf-8 -*-
import PyInstaller.__main__
import platform

# fmt: off
cmd = [
        "iscc_cli/cli.py",
        "--clean",
        "--console",
        "--hidden-import", "dotenv",
        "--collect-binaries", "exiv2",
        "--collect-data", "iscc_core",
        "--name", "iscc",
        "--onefile"
]
# fmt: on

PyInstaller.__main__.run(cmd)
