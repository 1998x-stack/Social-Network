# 专业代码库增强 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **Full pilot source code is in the companion appendix** `docs/superpowers/plans/2026-08-17-enhance-pilot-code.md` — read that file for the exact `section .py`, `test .py`, and doc skeletons referenced by Tasks 7–11.

**Goal:** 将 Social-Network 代码库提升为专业水准——共享 `netlab` 核心库（日志、绘图、图工具、生成器、demo 入口）、pytest 镜像测试树、富教程 per-section 文档、CI，并以 5 个试点节作为金标准模板。

**Architecture:** 保留 124 个节为独立可运行脚本（因其文件名含点号/中文字符无法 import），导入共享的 `netlab` 包；新增 `tests/` 与 `docs/sections/` 镜像树由 `netlab.generate` 生成；`tests/conftest.py` 用 `importlib` 加载任意中文/带点文件名脚本。

**Tech Stack:** Python ≥3.10, numpy, scipy, networkx, matplotlib；dev: pytest, pytest-cov, ruff, mypy。CI：GitHub Actions。

## Global Constraints

- Python ≥ 3.10。
- 节脚本文件名含中文与点号，**一律**通过 `tests/conftest.py::load_section()` 加载，禁止 `import` 节模块。
- 所有纯函数**导入时无副作用**；仅 `if __name__ == "__main__":` 运行 demo（日志 + 图件 + 结果）。
- 图件输出统一到 `outputs/<section>/`（`.gitignore`）。
- 日志统一用 `netlab.logging_setup.setup_logging`，禁止散落 `print`。
- 中文字体回退列表 `["PingFang SC","Hiragino Sans GB","Noto Sans CJK SC","WenQuanYi Micro Hei","SimHei","sans-serif"]`。
- 所有随机模型固定 `seed`。
- 每节完成门槛：实现 → 测试通过 → 日志 → 图 → 文档 → 链接校验。
- CI 无网络依赖，`matplotlib.use("Agg")`。

**试点节键与相对路径（Global，多次引用）**
- `7.3`: `第Ⅱ部分_网络理论基础/第7章_测度与参数/7.3_Katz中心性` （文件 `7.3_Katz中心性.py`）
- `10.3`: `第Ⅲ部分_计算机算法/第10章_网络基础算法/10.3_最短路径和广度优先搜索`
- `14.2`: `第Ⅳ部分_网络模型/第14章_网络生成模型/14.2_Barabási_Albert模型`
- `17.3`: `第Ⅴ部分_网络过程/第17章_传染病的网络模型/17.3_SIR模型`
- `6.13`: `第Ⅱ部分_网络理论基础/第6章_网络的数学基础/6.13_图拉普拉斯矩阵`

---

## Task 1: 项目脚手架（pyproject + .gitignore + netlab 包骨架）

**Files:** Create `pyproject.toml`, `.gitignore`, `netlab/__init__.py`

- [ ] **Step 1: 写 `.gitignore`**

```
__pycache__/
*.py[cod]
*.egg-info/
.venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/
outputs/
```

- [ ] **Step 2: 写 `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "netlab"
version = "0.1.0"
description = "《网络》配套的共享核心库：日志、绘图、图工具、生成器、demo 入口"
readme = "README.md"
requires-python = ">=3.10"
dependencies = ["numpy>=1.24", "scipy>=1.10", "networkx>=3.0", "matplotlib>=3.7"]

[project.optional-dependencies]
dev = ["pytest>=7", "pytest-cov>=4", "ruff>=0.4", "mypy>=1.8"]

[tool.setuptools.packages.find]
where = ["."]
include = ["netlab*"]

[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.10"
check_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q --cov=netlab --cov-report=term-missing"
```

- [ ] **Step 3: 写 `netlab/__init__.py`**

```python
"""netlab —— 网络的配套共享核心库。"""
__version__ = "0.1.0"

from .logging_setup import setup_logging
from .plotting import configure, new_figure, save_fig
from .graph_utils import adjacency_matrix, degree_sequence

__all__ = ["setup_logging", "configure", "new_figure", "save_fig",
           "adjacency_matrix", "degree_sequence", "__version__"]
```

- [ ] **Step 4: 运行验证**

`python -c "import netlab; print(netlab.__version__)"` → 输出 `0.1.0`。若 `netlab` 子模块未创建导致 ImportError，按 Task 2/3/4 顺序落地后再验证。

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml .gitignore netlab/__init__.py netlab/logging_setup.py netlab/plotting.py netlab/graph_utils.py 2>/dev/null
git commit -m "build: add pyproject, gitignore, netlab package skeleton"
```

---

## Task 2: netlab.logging_setup

**Files:** Create `netlab/logging_setup.py`; Test `tests/test_logging_setup.py`

**Interface:** `setup_logging(module: str = "main", level: int = logging.INFO, logfile: str|Path|None = None) -> logging.Logger`

格式 `%(asctime)s [<module>|%(levelname)-7s] %(message)s`；可选 `logfile` 自动建父目录；`module` 文本替换到格式里。

Tests must pass:
```python
def test_logfile_writes_structured_record(tmp_path):
    log = ls.setup_logging(module="7.3", logfile=tmp_path / "sub" / "run.log")
    log.info("Katz nodes=5 alpha=0.1")
    assert "Katz nodes=5 alpha=0.1" in (tmp_path / "sub" / "run.log").read_text()
    assert "7.3" in (tmp_path / "sub" / "run.log").read_text()
```

**实现：**

```python
"""结构化日志配置。所有节的 __main__ demo 都通过此模块初始化 logger。"""
from __future__ import annotations
import logging
import sys
from pathlib import Path

FORMAT = "%(asctime)s [%(module)s|%(levelname)-7s] %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"


def setup_logging(module="main", level=logging.INFO, logfile=None) -> logging.Logger:
    logger = logging.getLogger(module)
    logger.setLevel(level)
    logger.propagate = False
    logger.handlers.clear()
    formatter = logging.Formatter(FORMAT.replace("%(module)s", module), DATE_FMT)
    sh = logging.StreamHandler(sys.stdout); sh.setFormatter(formatter)
    logger.addHandler(sh)
    if logfile is not None:
        path = Path(logfile); path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(path, encoding="utf-8"); fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
```

- [ ] 步骤：写测试 → 运行失败 → 写实现 → 运行通过 → Commit `feat(netlab): add structured logging setup`

---

## Task 3: netlab.plotting

**Files:** Create `netlab/plotting.py`; Test `tests/test_plotting.py`

**Interface:**
- `configure() -> None`（应用中文字体回退、dpi=300、grid、tight_layout）
- `new_figure(title: str, title_key: str = "", figsize=(8.,5.)) -> (fig, ax)`
- `save_fig(fig, section_key: str, name: str, dpi=300, as_pdf=False) -> Path` → `outputs/<section>/<name>_<dpi>dpi.png`

**实现要点：**

```python
FONT_FALLBACK = ["PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC",
                 "WenQuanYi Micro Hei", "SimHei", "sans-serif"]
OUTPUT_DIR = Path("outputs")

def configure():
    matplotlib.rcParams.update({
        "figure.dpi": 300, "savefig.dpi": 300,
        "font.family": "sans-serif", "font.sans-serif": FONT_FALLBACK,
        "axes.grid": True, "grid.alpha": 0.3, "figure.tight_layout": True})

def new_figure(title, title_key="", figsize=(8.0, 5.0)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(f"{title}  [{title_key}]" if title_key else title, fontsize=12)
    return fig, ax

def save_fig(fig, section_k, name, dpi=300, as_pdf=False):
    d = OUTPUT_DIR / section_k; d.mkdir(parents=True, exist_ok=True)
    png = d / f"{name}_{dpi}dpi.png"; fig.savefig(png, dpi=dpi)
    if as_pdf: fig.savefig(d / f"{name}.pdf", dpi=dpi)
    plt.close(fig)
    return png
```

测试在 `tests/test_plotting.py` 顶部 `matplotlib.use("Agg")`，monkeypatch `plotting.OUTPUT_DIR` 指向 `tmp_path`，断言 PNG 存在。失败→实现→通过→提交 `feat(netlab): add unified plotting helpers`。

---

## Task 3: netlab.graph_utils

**Files:** Create `netlab/graph_utils.py`; Test `tests/test_graph_utils.py`

**Interface:**
- `adjacency_matrix(G) -> np.ndarray`（按排序节点）
- `degree_sequence(G) -> list[int]`
- `reference_tolerance() -> float`（返回 `1e-6`）

**实现：**

```python
def adjacency_matrix(G):
    import numpy as np
    return nx.to_numpy_array(G, nodelist=sorted(G.nodes()))

def degree_sequence(G):
    order = sorted(G.nodes()); return [G.degree(n) for n in order]

def reference_tolerance(): return 1e-6
```

测试断言 `adjacency_matrix` 等于 `nx.to_numpy_array(nodelist=sorted(...))`、`degree_sequence(nx.path_graph(4)) == [1,2,2,1]`。→ 通过 → 提交。

---

## Task 4: tests/conftest.py（节加载器 + fixtures）

**Files:** Create `tests/conftest.py`; Test `tests/test_conftest.py`

**Interface:** `load_section(rel_path: str) -> module`（仓库根相对路径）；fixtures `known_graph`（9 节点 11 边固定图）、`simple_graph`（`nx.path_graph(4)`）。

**conftest.py：**

```python
import importlib.util, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def load_section(rel_path):
    full = (PROJECT_ROOT / rel_path).resolve()
    if not full.exists(): raise FileNotFoundError(full)
    spec = importlib.util.spec_from_file_location(full.stem, full)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

import pytest, networkx as nx

@pytest.fixture
def known_graph():
    G = nx.Graph()
    G.add_edges_from([(0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(4,5),(4,6),(5,7),(6,7),(7,8)])
    return G

@pytest.fixture
def simple_graph(): return nx.path_graph(4)
```

`tests/test_conftest.py` 用一个临时 `.py` 文件测 `load_section`（写 `VALUE=42`，读取断言 42），不依赖任何试点节。→ 通过 → 提交。

---

## Task 5: netlab.generate（生成器）+ main.py 薄包装

**Files:** Create `netlab/generate.py`; Modify `main.py`

**做法：**
1. 把 `main.py` 顶部 `structure` 字典原样复制到 `netlab/generate.py` 为 `STRUCTURE`。
2. 实现（模仿现有递归规则 `replace(" ","_").replace("-","_")`）：

```python
ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT/"docs"/"sections"; TESTS_DIR = ROOT/"tests"

def _san(s): return s.replace(" ", "_").replace("-", "_")

def walk():
    for part, chaps in STRUCTURE.items():
        pd = _san(part)
        for chap, kids in chaps.items():
            cd = _san(chap)
            for kid in kids:
                sd = _san(kid)
                yield part, pdf, pd, sd
```

（***关键***：先读取现有 `main.py`，按其真实嵌套结构迭代。上面为示意；实现时以实际 `STRUCTURE` 嵌套为准。`children` 是叶子（无子 dict）。）

`gen_doc_skeletons()` — 对每个 `docs/sections/<pd>/<cd>/<sd>.md` 若不存在则写骨架（概述/核心概念与公式/代码说明/运行/可视化/测试/延伸实验，各配 `<!-- 待填充 -->`）。**绝不覆盖已存在富文档。**

`gen_test_skeletons()` — 对每个 `tests/<pd>/<cd>/test_<sd>.py` 若不存在则写骨架（`load_section` 占位）。**绝不覆盖。**

`gen_readme()` — 每个节写 `<part>/<chap>/<kid>` 链接其源码与 `docs/sections/.../X.md`，顶部加快速开始（`pip install -e .[dev]`、`python -m netlab.demos 7.3`、`python -m pytest`）。

`main() -> None` 依次调用并打印统计。`main.py` 改为薄包装 import 并调用 `netlab.generate.main()`。

- [ ] 步骤 1：读 `main.py` 拷 structure
- [ ] 步骤 2：实现 `generate.py`
- [ ] 步骤 3：改写 `main.py`
- [ ] 步骤 4：`python main.py` → 生成成功、不覆盖已有
- [ ] 步骤 5：校验 README 链接可解析（写 python 脚本遍历 `./...` 路径存在性，输出 `bad links: []`）
- [ ] 步骤 6：提交

---

## Task 6: netlab.demos（统一运行入口）

**Files:** Create `netlab/demos.py`; Test `tests/test_demos.py`

```python
SECTION_PATHS = {
    "7.3":  "第Ⅱ部分_网络理论基础/第7章_测度与参数/7.3_Katz中心性/7.3_Katz中心性.py",
    "10.3": "第Ⅲ部分_计算机算法/第10章_网络基础算法/10.3_最短路径和广度优先搜索/10.3_最短路径和广度优先搜索.py",
    "14.2": "第Ⅳ部分_网络模型/第14章_网络生成模型/14.2_Barabási_Albert模型/14.2_Barabási_Albert模型.py",
    "17.3": "第Ⅴ部分_网络过程/第17章_传染病的网络模型/17.3_SIR模型/17.3_SIR模型.py",
    "6.13": "第Ⅱ部分_网络理论基础/第6章_网络的数学基础/6.13_图拉普拉斯矩阵/6.13_图拉普拉斯矩阵.py",
}
```

- `run(key: str) -> int`：`importlib` 加载 `SECTION_PATHS[key]`，调用 `module.main()`；未知键抛 `KeyError`。
- `run_demo(key) = run(key)`。
- `python -m netlab.demos <key>` 入口。

`tests/test_demos.py`：断言 `"7.3" in SECTION_PATHS`；`pytest.raises(KeyError): run_demo("99")`。→ red → 实现 → 通过 → 提交 `feat(netlab): unified demo entry point`。

---

## Task 7–11: 五个试点节

每个试点节 7 步流程：写失败测试 → 运行失败 → **从附录读取完整实现** → 测试通过 → `python -m netlab.demos <key>` 运行 demo 并验证 `outputs/<key>/*.png` 与 `run.log` 生成 → 写富文档（按 8 节模板） → `python main.py` 校验链接 → Commit。

**试点 1 — 7.3 Katz中心性** (`key=7.3`)：`katz_centrality(adj, alpha)`, `normalize(x)`, `main()`。测试：与 `np.linalg.solve(I - alpha*A.T, beta*1)` 参考一致（容差 1e-6）；`normalize` 和=1。可视化：`new_figure("Katz中心性", "7.3")`，节点大小∝中心性，`spring_layout(seed=42)`，保存 `katz_300dpi.png`。**完整代码见附录 Task 7。**

**试点 7bis. 10.3 最短路径和广度优先搜索** (`key=10.3`)：`bfs_distance(G, source)`, `shortest_path(G, source, target)`, `main()`。测试：`bfs_distance` 等于 `nx.single_source_shortest_path_length`；`shortest_path` 端点正确且为合法路径。可视化高亮路径。**完整代码见附录。**

**试点 8. 14.2 Barabási-Albert模型** (`key=14.2`)：`barabasi_albert(m0, m, n, seed)`（优先连接，`random.Random(seed)`，避免重边/自环）、`degree_distribution(G)`。测试：`n=200` 连通、边数≈；度分布归一化。可视化：log-log 度分布叠加幂律线。**完整代码见附录。**

**试点 9. 17.3 SIR模型** (`key=17.3`)：`sir_simulate(pop, beta, gamma, t_max, i0=1, seed=42) -> (t, S, I, R)`。测试：S+I+R 守恒、初态 S=pop-i0,I=i0、S 单调递减。可视化 S/I/R 时间序列。**完整代码见附录。**

**试点 10. 6.13 图拉普拉斯矩阵** (`key=6.13`)：`laplacian(adj)`, `fiedler(evals)`, `main()`。测试：等于 `nx.laplacian_matrix`、L·1=0、对称；`eigvalsh` 二次特征值。可视化特征值谱 + spring 布局按 Fiedler 向量着色。**完整代码见附录。**

每个试点提交信息形如 `feat(<key>): <名字> implementation, tests, docs`。

---

## Task 11: CI（.github/workflows）+ 最终校验

**Files:** Create `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "${{ matrix.python-version }}" }
      - run: python -m pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy netlab
      - run: python -m pytest
```

- [ ] Step 1: 写 `ci.yml`
- [ ] Step 2: 本地跑 `ruff check .`、`mypy netlab`、`python -m pytest`（使用 Agg），修到全绿
- [ ] Step 3: 校验 README/文档链接（脚本遍历 `]`(path) exists）
- [ ] Step 4: 提交 `ci: add GitHub Actions workflow + final lint/format/link checks`

---

## Self-Review 记录（实现者无需执行）

计划覆盖 spec 全部要求：§1 阶段策略→Task 7–10+后续；§2 混合（手写+参考验证）→各试点测试；§3 架构（netlab+镜像树+loader）→Task1–5；§4 日志→Task2；§5 测试→Task4、各试点测试；§6 可视化→netlab.plotting+各试点 viz；§7 每节文档→generate 骨架+试点富文档；§8 工具/CI→Task1/11；§9 试点扩展工作流→Task7–11。

> **实现者注意：**上文中几处占位（`pdf`/`md` 等拼写、`类似 Task N` 的简述）以附录**完整源码**为准——真正执行的代码与测试全部在 `docs/superpowers/plans/2026-08-17-enhance-pilot-appendix.md`。本文件不包含可执行占位符。