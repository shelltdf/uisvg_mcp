#!/usr/bin/env python3
"""开发服务器：npm run dev"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    if not (ROOT / "node_modules").is_dir():
        rc = subprocess.call(["npm", "install"], cwd=ROOT, shell=sys.platform == "win32")
        if rc != 0:
            return rc
    return subprocess.call(["npm", "run", "dev"], cwd=ROOT, shell=sys.platform == "win32")


if __name__ == "__main__":
    raise SystemExit(main())
