"""从 STRUCTURE 重新生成 README 索引、文档骨架、测试骨架。

原则：只写不存在的文件，绝不覆盖已有实现/富文档。
"""
from __future__ import annotations

from pathlib import Path

from .structure import STRUCTURE

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs" / "sections"
TESTS_DIR = ROOT / "tests"


def _san(s: str) -> str:
    return s.replace(" ", "_").replace("-", "_")


def walk():
    """yield (part, chap, kid, part_dir, chap_dir, sec_dir, key)。"""
    for part, chapters in STRUCTURE.items():
        pd = _san(part)
        for chap, sections in chapters.items():
            cd = _san(chap)
            for kid in sections:
                sd = _san(kid)
                yield part, chap, kid, pd, cd, sd, kid.split(" ")[0]


def gen_doc_skeletons() -> int:
    n = 0
    for part, chap, kid, pd, cd, sd, key in walk():
        doc = DOCS_DIR / pd / cd / f"{sd}.md"
        if doc.exists():
            continue
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(
            f"# {kid}\n\n## 概述\n<!-- 待填充 -->\n\n"
            f"## 核心概念与公式\n<!-- 待填充 -->\n\n"
            f"## 代码说明\n<!-- 待填充 -->\n\n"
            f"## 运行\n`python -m netlab.demos {key}`\n\n"
            f"## 可视化\n<!-- 待填充 -->\n\n"
            f"## 测试\n<!-- 待填充 -->\n\n"
            f"## 延伸实验\n<!-- 待填充 -->\n",
            encoding="utf-8",
        )
        n += 1
    return n


def gen_test_skeletons() -> int:
    n = 0
    for part, chap, kid, pd, cd, sd, key in walk():
        # 测试文件名必须可被 pytest 导入 → 去掉点号（用下划线）
        tname = f"test_{sd.replace('.', '_')}.py"
        t = TESTS_DIR / pd / cd / tname
        if t.exists():
            continue
        t.parent.mkdir(parents=True, exist_ok=True)
        # 骨架保持最简 → ruff 零告警（占位，将被真实测试替换）
        t.write_text(
            f'"""占位：{kid}（待填充真实测试）"""\n\n'
            f"def test_skeleton_placeholder():\n"
            f"    assert True\n",
            encoding="utf-8",
        )
        n += 1
    return n


def gen_readme() -> None:
    links = []
    for part, chap, kid, pd, cd, sd, key in walk():
        sec_file = f"{pd}/{cd}/{sd}/{sd}.py"
        doc_file = f"docs/sections/{pd}/{cd}/{sd}.md"
        links.append(
            f"### {part}/{chap}/{kid}\n\n"
            f"- [源码](./{sec_file})\n- [文档](./{doc_file})"
        )
    README = ROOT / "README.md"
    README.write_text(
        "# 网络的实证研究（《Networks》配套）\n\n"
        "## 快速开始\n\n```bash\n"
        "python -m pip install -e .[dev]\n"
        "python -m netlab.demos 7.3\n"
        "python -m pytest\n```\n\n"
        "## 章节索引\n\n" + "\n\n".join(links) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    nd = gen_doc_skeletons()
    nt = gen_test_skeletons()
    gen_readme()
    print(f"生成完成：文档骨架 {nd}，测试骨架 {nt}，已重写 README。")