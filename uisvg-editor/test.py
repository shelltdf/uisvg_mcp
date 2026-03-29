#!/usr/bin/env python3
"""冒烟：在已安装依赖的前提下执行生产构建。"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    if not (ROOT / "node_modules").is_dir():
        print("缺少 node_modules，请先在此目录执行: npm install", file=sys.stderr)
        return 2
    return subprocess.call(["npm", "run", "build"], cwd=ROOT, shell=sys.platform == "win32")


if __name__ == "__main__":
    raise SystemExit(main())
