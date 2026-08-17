"""统一 demo 入口：python -m netlab.demos <key>"""
from __future__ import annotations

import sys

SECTION_PATHS = {
    "7.3": "第Ⅱ部分_网络理论基础/第7章_测度与参数/7.3_Katz中心性/7.3_Katz中心性.py",
    "10.3": "第Ⅲ部分_计算机算法/第10章_网络基础算法/10.3_最短路径和广度优先搜索/10.3_最短路径和广度优先搜索.py",  # noqa: E501
    "14.2": "第Ⅳ部分_网络模型/第14章_网络生成模型/14.2_Barabási_Albert模型/14.2_Barabási_Albert模型.py",  # noqa: E501
    "17.3": "第Ⅴ部分_网络过程/第17章_传染病的网络模型/17.3_SIR模型/17.3_SIR模型.py",
    "6.13": "第Ⅱ部分_网络理论基础/第6章_网络的数学基础/6.13_图拉普拉斯矩阵/6.13_图拉普拉斯矩阵.py",
}


def _load(rel: str):
    import importlib.util
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    full = (root / rel).resolve()
    spec = importlib.util.spec_from_file_location(full.stem, full)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载模块: {full}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(key: str) -> int:
    if key not in SECTION_PATHS:
        raise KeyError(f"未知节键: {key}")
    mod = _load(SECTION_PATHS[key])
    if hasattr(mod, "main"):
        mod.main()
        return 0
    raise AttributeError(f"{key} 未定义 main()")


def run_demo(key: str) -> int:
    return run(key)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python -m netlab.demos <key>")
    sys.exit(run(sys.argv[1]))