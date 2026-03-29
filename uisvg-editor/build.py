#!/usr/bin/env python3
"""生产构建：npm run build"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    if not (ROOT / "node_modules").is_dir():
        rc = subprocess.call(["npm", "install"], cwd=ROOT, shell=sys.platform == "win32")
        if rc != 0:
            return rc
    return subprocess.call(["npm", "run", "build"], cwd=ROOT, shell=sys.platform == "win32")


if __name__ == "__main__":
    raise SystemExit(main())
