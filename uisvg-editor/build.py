#!/usr/bin/env python3
"""生产构建：npm run build"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    return subprocess.call(["npm", "run", "build"], cwd=ROOT, shell=sys.platform == "win32")


if __name__ == "__main__":
    raise SystemExit(main())
