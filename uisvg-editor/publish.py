#!/usr/bin/env python3
"""发布：执行构建并说明 dist/ 输出路径。"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"


def main() -> int:
    if not (ROOT / "node_modules").is_dir():
        print("缺少 node_modules，请先执行: npm install", file=sys.stderr)
        return 2
    code = subprocess.call(["npm", "run", "build"], cwd=ROOT, shell=sys.platform == "win32")
    if code != 0:
        return code
    print(f"可分发静态资源目录: {DIST}")
    print("可将 dist/ 部署到任意静态文件托管。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
