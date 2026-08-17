"""兼容入口：调用 netlab.generate 重新生成索引/骨架。"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from netlab.generate import main

if __name__ == "__main__":
    main()