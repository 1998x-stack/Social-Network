# 试点节完整源码附录（Pilot Source Appendix）

> 这是 `2026-08-17-enhance-professional-codebase.md` 的配套文件。Tasks 7–11 及各节测试的**权威完整源码**都列于此。实现者逐节按此落地。
> 所有相对路径均相对于仓库根。所有节脚本「导入时无副作用」；demo 放 `if __name__ == "__main__":`。
> 图件必须落到 `outputs/<key>/`；用 `netlab.plotting` 的 `configure/new_figure/save_fig`；日志用 `setup_logging(module=<key>, logfile="outputs/<key>/run.log")`。

---

## A. 权威 `netlab/generate.py`（Task 5）

```python
"""从 STRUCTURE 重新生成 README 索引、文档骨架、测试骨架。

原则：只写不存在的文件，绝不覆盖已有实现/富文档。
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs" / "sections"
TESTS_DIR = ROOT / "tests"

# ---- 原 main.py 的 structure 原样复制于此（实现时完整拷贝）----
STRUCTURE = {
    "第Ⅰ部分 网络的实证研究": {
        "第2章 技术网络": {
            "2.1 Internet": {},
            # ... 每个节一个 key: {} ...
        },
        # ...
    },
    # ...
}


def _san(s: str) -> str:
    return s.replace(" ", "_").replace("-", "_")


def walk():
    for part, chapters in STRUCTURE.items():
        pd = _san(part)
        for chap, sections in chapters.items():
            cd = _san(chap)
            for kid in sections:
                sd = _san(kid)
                yield part, chap, kid, pd, cd, sd


def gen_doc_skeletons() -> int:
    n = 0
    for part, chap, kid, pd, cd, sd in walk():
        doc = DOCS_DIR / pd / cd / f"{sd}.md"
        if doc.exists():
            continue
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(
            f"# {kid}\n\n## 概述\n<!-- 待填充 -->\n\n"
            f"## 核心概念与公式\n<!-- 待填充 -->\n\n"
            f"## 代码说明\n<!-- 待填充 -->\n\n"
            f"## 运行\n`python -m netlab.demos {kid.split(' ')[0]}`\n\n"
            f"## 可视化\n<!-- 待填充 -->\n\n"
            f"## 测试\n<!-- 待填充 -->\n\n"
            f"## 延伸实验\n<!-- 待填充 -->\n",
            encoding="utf-8",
        )
        n += 1
    return n


def gen_test_skeletons() -> int:
    n = 0
    for part, chap, kid, pd, cd, sd in walk():
        t = TESTS_DIR / pd / cd / f"test_{sd}.py"
        if t.exists():
            continue
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(
            f'"""占位：{kid}"""\n'
            f"from tests.conftest import load_section\n\n"
            f'def test_skeleton_placeholder():\n'
            f'    sec = load_section("{pd}/{cd}/{sd}/{sd}.py")\n'
            f"    assert sec is not None\n",
            encoding="utf-8",
        )
        n += 1
    return n


def gen_readme() -> None:
    links = []
    for part, chap, kid, pd, cd, sd in walk():
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
```

> **STRUCTURE 占位说明**：本文件中 `STRUCTURE` 仅示意。实现时必须把 `main.py` **完整** structure 字典原样拷贝进来（4 部分/19 章/124 节）。`walk()` 依赖「每章 dict 的键即叶子节」。

`main.py` 改写为：

```python
"""兼容入口。"""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from netlab.generate import main
if __name__ == "__main__":
    main()
```

---

## B. Task 7 — 7.3 Katz中心性

### `第Ⅱ_部分_网络理论基础/第7章_测度与参数/7.3_Katz中心性/7.3_Katz中心性.py`

```python
# 7.3 Katz中心性
"""
Lecture: 第Ⅱ部分 网络理论基础/第7章 测度与参数/7.3 Katz中心性
Content: 7.3 Katz中心性

Katz 中心性：x = beta (I - alpha A^T)^-1 1，alpha < 1/最大特征值保证收敛。
"""
from __future__ import annotations

import logging

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from netlab import setup_logging, configure, new_figure, save_fig

log = logging.getLogger("7.3")


def katz_centrality(adj: np.ndarray, alpha: float, beta: float = 1.0) -> np.ndarray:
    n = adj.shape[0]
    return np.linalg.solve(np.eye(n) - alpha * adj.T, np.full(n, beta))


def normalize(x: np.ndarray) -> np.ndarray:
    s = x.sum()
    return x / s if s != 0 else np.zeros_like(x)


def viz(adj: np.ndarray):
    configure()
    x = normalize(katz_centrality(adj, 0.1))
    G = nx.from_numpy_array(adj)
    fig, ax = new_figure("Katz中心性", "7.3")
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(G, pos, ax=ax, node_size=300 + 3500 * x,
                     node_color=list(x), cmap=plt.cm.viridis, with_labels=True)
    return save_fig(fig, "7.3", "katz")


def main() -> None:
    setup_logging(module="7.3", logfile="outputs/7.3/run.log")
    adj = np.array([[0,1,1,0,0],[1,0,1,1,0],[1,1,0,0,1],
                    [0,1,0,0,1],[0,0,1,1,0]])
    alpha = 0.2
    x = normalize(katz_centrality(adj, alpha))
    log.info("katz alpha=%s values=%s", alpha, x.round(4).tolist())
    png = viz(adj)
    log.info("figure saved=%s", png)


if __name__ == "__main__":
    main()
```

### `tests/第Ⅱ部分_网络理论基础/第7章_测度与参数/test_7.3_Katz中心性.py`

```python
import numpy as np
import networkx as nx
from tests.conftest import load_section

SEC = load_section(
    "第Ⅱ部分_网络理论基础/第7章_测度与参数/7.3_Katz中心性/7.3_Katz中心性.py"
)


def test_katz_matches_reference(known_graph):
    nodelist = sorted(known_graph.nodes())
    adj = nx.to_numpy_array(known_graph, nodelist=nodelist)
    alpha = 0.1
    got = SEC.katz_centrality(adj, alpha)
    I = np.eye(adj.shape[0])
    ref = np.linalg.solve(I - alpha * adj.T, np.full(adj.shape[0], 1.0))
    ref = ref / ref.sum()
    assert np.allclose(got, ref, atol=1e-6)


def test_normalize_sums_to_one():
    x = np.array([1.0, 2.0, 3.0])
    assert np.allclose(SEC.normalize(x), x / x.sum())
```

### Doc（`docs/sections/第Ⅱ部分_网络理论基础/第7章_测度与参数/7.3_Katz中心性.md`）

```markdown
# 7.3 Katz中心性

## 概述
Katz 中心性在度中心性基础上引入全局信息：每个节点的分数=自身基础权重加其邻居分数之和（衰减因子 alpha）。适合有向/有影响力传播的网络。

## 核心概念与公式
x = β(I − αAᵀ)⁻¹·1，收敛需 α·ρ(A) < 1。

## 代码说明
- `katz_centrality(adj, alpha, beta=1.0)`：直接解线性方程组（复杂度 O(n³)）。
- `normalize(x)`：归一化到和为 1。
- `main()`：5 节点示例 + 日志 + 图件。

## 运行
`python -m netlab.demos 7.3`，日志写 `outputs/7.3/run.log`，图见下方。

## 可视化
![Katz](./outputs/7.3/katz_300dpi.png)（节点大小∝Katz中心性）

## 测试
- `test_katz_matches_reference`：与解析解一致。
- `test_normalize_sums_to_one`。

## 延伸实验
把 alpha 增大到接近 1/ρ(A) 观察发散；换成有向图比较不对称性。
```

> 图中相对路径在文档中写 `outputs/...`，CI/渲染时若仓库根相对，则保留相对链接。

---

## Task 7bis. — 10.3 最短路径和广度优先搜索

### `第Ⅲ部分_计算机算法/第10章_网络基础算法/10.3_最短路径和广度优先搜索/10.3_最短路径和广度优先搜索.py`

```python
# 10.3 最短路径和广度优先搜索
"""
Lecture: 第Ⅲ部分 计算机算法/第10章 网络基础算法/10.3 最短路径和广度优先搜索
Content: 10.3 最短路径和广度优先搜索

BFS 在无权图上逐层推进求最短距离；由前驱回溯得最短路径。复杂度 O(V+E)。
"""
from __future__ import annotations

import logging

import networkx as nx
import matplotlib.pyplot as plt

from netlab import setup_logging, configure, new_figure, save_fig

log = logging.getLogger("10.3")


def bfs_distance(G, source: int) -> dict:
    dist = {source: 0}
    frontier = [source]
    while frontier:
        nxt = []
        for u in frontier:
            for v in G.neighbors(u):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    nxt.append(v)
        frontier = nxt
    return dist


def shortest_path(G, source: int, target: int) -> list:
    if target not in bfs_distance(G, source):
        raise ValueError(f"target {target} 不可达")
    prev = {source: None}
    frontier = [source]
    while frontier:
        nxt = []
        for u in frontier:
            for v in G.neighbors(u):
                if v not in prev:
                    prev[v] = u
                    nxt.append(v)
        frontier = nxt
    path, node = [], target
    while node is not None:
        path.append(node)
        node = prev[node]
    return path[::-1]


def viz(G, source: int, target: int):
    configure()
    dist = bfs_distance(G, source)
    fig, ax = new_figure("BFS最短路径", "10.3")
    pos = nx.spring_layout(G, seed=42)
    colors = [dist.get(n, -1) for n in G.nodes()]
    nx.draw_networkx(G, pos, ax=ax, node_color=colors, cmap=plt.cm.turbo, with_labels=True)
    path = shortest_path(G, source, target)
    edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges, edge_color="red", width=3)
    return save_fig(fig, "10.3", "bfs")


def main():
    setup_logging(module="10.3", logfile="outputs/10.3/run.log")
    G = nx.convert_node_labels_to_integers(nx.grid_2d_graph(3, 5).to_undirected())
    source, target = 0, G.number_of_nodes() - 1
    dist = bfs_distance(G, source)
    log.info("bfs nodes=%s max_dist=%s", G.number_of_nodes(), max(dist.values()))
    path = shortest_path(G, source, target)
    log.info("path=%s len=%s", path, len(path))
    png = viz(G, source, target)
    log.info("figure saved=%s", png)


if __name__ == "__main__":
    main()
```

### `tests/第Ⅲ部分_计算机算法/第10章_网络基础算法/test_10.3_最短路径和广度优先搜索.py`

```python
import networkx as nx
from tests.conftest import load_section

SEC = load_section(
    "第Ⅲ部分_计算机算法/第10章_网络基础算法/"
    "10.3_最短路径和广度优先搜索/10.3_最短路径和广度优先搜索.py"
)


def test_bfs_distance_matches_networkx(known_graph):
    got = SEC.bfs_distance(known_graph, 0)
    ref = nx.single_source_shortest_path_length(known_graph, 0)
    assert got == ref


def test_shortest_path_valid(known_graph):
    path = SEC.shortest_path(known_graph, 0, 8)
    assert path[0] == 0 and path[-1] == 8
    assert all(known_graph.has_edge(a, b) for a, b in zip(path, path[1:]))
```

---

## Task 8. — 14.2 Barabási-Albert模型

### `第Ⅳ部分_网络模型/第14章_网络生成模型/14.2_Barabási_Albert模型/14.2_Barabási_Albert模型.py`

```python
# 14.2 Barabási-Albert模型
"""
Lecture: 第Ⅳ部分 网络模型/第14章 网络生成模型/14.2 Barabási-Albert模型
Content: 14.2 Barabási-Albert模型

优先连接：新节点以与度成正比概率连到已有节点 → 无标度（幂律）度分布。
"""
from __future__ import annotations

import logging
import random
from collections import Counter

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from netlab import setup_logging, configure, new_figure, save_fig

log = logging.getLogger("14.2")


def barabasi_albert(m0: int, m: int, n: int, seed: int = 42) -> nx.Graph:
    rng = random.Random(seed)
    G = nx.complete_graph(m0)
    for _ in range(m0, n):
        nodes = list(G.nodes())
        weights = [G.degree(u) for u in nodes]
        chosen, tries = set(), 0
        while len(chosen) < m and tries < 20 * m:
            chosen.add(rng.choices(nodes, weights=weights, k=1)[0])
            tries += 1
        new = len(nodes)
        G.add_node(new)
        for t in chosen:
            G.add_edge(new, t)
    return G


def degree_distribution(G) -> tuple:
    degs = list(dict(G.degree()).values())
    cnt = Counter(degs)
    ks = sorted(cnt)
    return ks, [cnt[k] / len(degs) for k in ks]


def viz(G):
    configure()
    ks, freqs = degree_distribution(G)
    fig, ax = new_figure("BA度分布(对数-对数)", "14.2")
    ax.loglog(ks, freqs, "o", label="模拟")
    if len(ks) >= 2:
        ax.loglog([ks[0], ks[-1]], [freqs[0], freqs[-1]], "--",
                  color="gray", label="幂律参考")
    ax.set_xlabel("k"); ax.set_ylabel("P(k)"); ax.legend()
    return save_fig(fig, "14.2", "degree")


def main() -> None:
    setup_logging(module="14.2", logfile="outputs/14.2/run.log")
    G = barabasi_albert(5, 2, 1000, seed=42)
    log.info("ba nodes=%s edges=%s connected=%s", G.number_of_nodes(),
             G.number_of_edges(), nx.is_connected(G))
    png = viz(G)
    log.info("figure saved=%s", png)


if __name__ == "__main__":
    main()
```

### 测试 `tests/第Ⅳ.../test_14.2_Barabási_Albert模型.py`

```python
import networkx as nx
import pytest
from tests.conftest import load_section

SEC = load_section(
    "第Ⅳ部分_网络模型/第14章_网络生成模型/14.2_Barabási_Albert模型/14.2_Barabási_Albert模型.py"
)


def test_ba_connected_and_size():
    G = SEC.barabasi_albert(5, 2, 200, seed=1)
    assert G.number_of_nodes() == 200
    assert nx.is_connected(G)


def test_ba_degree_sum_even():
    G = SEC.barabasi_albert(3, 2, 50, seed=2)
    assert sum(dict(G.degree()).values()) % 2 == 0


def test_degree_distribution_normalized():
    ks, freqs = SEC.degree_distribution(nx.path_graph(4))
    assert sum(freqs) == 1.0
```

---

## Task 9. — 17.3 SIR模型

### `.../17.3_SIR模型/17.3_SIR模型.py`

```python
# 17.3 SIR模型
"""
Lecture: 第Ⅴ部分 网络过程/第17章 传染病的网络模型/17.3 SIR模型
Content: 17.3 SIR模型

SIR：S→I(传染率 beta)，I→R(康复率 gamma)。S+I+R 守恒。
"""
from __future__ import annotations

import logging

import numpy as np
import matplotlib.pyplot as plt

from netlab import setup_logging, configure, new_figure, save_fig

log = logging.getLogger("17.3")


def sir_simulate(pop, beta, gamma, t_max, i0=1, seed=42):
    rng = np.random.default_rng(seed)
    S, I, R = [pop - i0], [i0], [0]
    s, i, r = pop - i0, i0, 0
    for _ in range(t_max):
        p_inf = 0.0 if i == 0 else 1 - np.exp(-beta * i / pop)
        inf_new = int(rng.binomial(s, p_inf)) if s > 0 else 0
        rec_new = int(rng.binomial(i, gamma)) if i > 0 else 0
        s -= inf_new
        i = i + inf_new - rec_new
        r += rec_new
        S.append(s); I.append(i); R.append(r)
    return np.arange(t_max + 1), np.array(S), np.array(I), np.array(R)


def viz(t, S, I, R):
    configure()
    fig, ax = new_figure("SIR传播", "17.3")
    ax.plot(t, S, label="S"); ax.plot(t, I, label="I"); ax.plot(t, R, label="R")
    ax.set_xlabel("时间"); ax.set_ylabel("人数"); ax.legend()
    return save_fig(fig, "17.3", "sir")


def main() -> None:
    setup_logging(module="17.3", logfile="outputs/17.3/run.log")
    t, S, I, R = sir_simulate(1000, 0.3, 0.1, 300)
    log.info("sir peak_I=%s at_t=%s", int(I.max()), int(t[I.argmax()]))
    png = viz(t, S, I, R)
    log.info("figure saved=%s", png)


if __name__ == "__main__":
    main()
```

### 测试 `tests/第17.../test_17.3_SIR模型.py`

```python
import numpy as np
from tests.conftest import load_section

SEC = load_section(
    "第Ⅴ部分_网络过程/第17章_传染病的网络模型/17.3_SIR模型/17.3_SIR模型.py"
)


def test_conservation():
    t, S, I, R = SEC.sir_simulate(500, 0.2, 0.1, 200)
    assert np.allclose(S + I + R, 500.0)


def test_initial_state():
    t, S, I, R = SEC.sir_simulate(500, 0.2, 0.1, 5)
    assert S[0] == 499 and I[0] == 1 and R[0] == 0


def test_s_non_increasing():
    t, S, I, R = SEC.sir_simulate(500, 0.2, 0.1, 50)
    assert np.all(np.diff(S) <= 1e-9)
```

> 图例里 `peak_I` 那行的 argmax 写法别扭，可简化为 `int(t[I.argmax()])`。

---

## Task 10. — 6.13 图拉普拉斯矩阵

```python
# 6.13 图拉普拉斯矩阵
"""
Lecture: 第Ⅱ部分 网络理论基础/第6章 网络的数学基础/6.13 图拉普拉斯矩阵
Content: 6.13 图拉普拉斯矩阵

L = D - A。L·1 = 0；Fiedler 值（第二小特征值）衡量连通性。
"""
from __future__ import annotations

import logging

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from netlab import setup_logging, configure, new_figure, save_fig

log = logging.getLogger("6.13")


def laplacian(adj: np.ndarray) -> np.ndarray:
    n = adj.shape[0]
    return np.diag(adj.sum(axis=1)) - adj


def fiedler(evals: np.ndarray) -> float:
    return float(evals[1])


def viz(adj: np.ndarray):
    configure()
    L = laplacian(adj)
    evals = np.linalg.eigvalsh(L)
    fig, ax = new_figure("拉普拉斯特征值谱", "6.13")
    ax.plot(range(len(evals)), evals, "o-")
    ax.set_xlabel("index"); ax.set_ylabel("λ")
    p1 = save_fig(fig, "6.13", "eigs")
    _, vecs = np.linalg.eigh(L)
    fied = vecs[:, 1]
    G = nx.from_numpy_array(adj)
    fig2, ax2 = new_figure("Fiedler 向量着色", "6.13")
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(G, pos, ax=ax2, node_color=list(fied),
                     cmap=plt.cm.coolwarm, with_labels=True)
    p2 = save_fig(fig2, "6.13", "fiedler")
    return p1, p2


def main() -> None:
    setup_logging(module="6.13", logfile="outputs/6.13/run.log")
    adj = np.array([[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]])
    L = laplacian(adj)
    evals = np.linalg.eigvalsh(L)
    log.info("laplacian evals=%s fiedler=%s", evals.round(4).tolist(), fiedler(evals))
    p1, p2 = viz(adj)
    log.info("figures saved=%s %s", p1, p2)


if __name__ == "__main__":
    main()
```

### 测试 `tests/test_6.13_图拉普拉斯矩阵.py`

```python
import numpy as np
import networkx as nx
import pytest
from tests.conftest import load_section

SEC = load_section(
    "第Ⅱ部分_网络理论基础/第6章_网络的数学基础/6.13_图拉普拉斯矩阵/6.13_图拉普拉斯矩阵.py"
)


def test_laplacian_matches_networkx(known_graph):
    nl = sorted(known_graph.nodes())
    adj = nx.to_numpy_array(known_graph, nodelist=nl)
    ref = nx.laplacian_matrix(known_graph, nodelist=nl).toarray()
    assert np.allclose(SEC.laplacian(adj), ref)


def test_row_sum_zero_and_symmetry(known_graph):
    nl = sorted(known_graph.nodes())
    adj = nx.to_numpy_array(known_graph, nodelist=nl)
    L = SEC.laplacian(adj)
    assert np.allclose(L @ np.ones(L.shape[0]), 0)
    assert np.allclose(L, L.T)


def test_fiedler_single_edge():
    L = SEC.laplacian(np.array([[0, 1], [1, 0]]))
    assert SEC.fiedler(np.linalg.eigvalsh(L)) == pytest.approx(2.0)
```

---

## 说明

- 上文可能有排版造成的零散笔误（如 `p1`/`p2`、某句里的 emoji 符等），实现者以「能跑通、测试全绿、demo 存图、文档链接可解析」为验收，正确缩进与名称以逻辑为准。
- 每个试点跑 `python -m netlab.demos <key>` 验证；`python -m pytest` 全绿；`ruff check .`、`mypy netlab` 通过。