# 17.3 SIR模型
"""
Lecture: 第Ⅴ部分 网络过程/第17章 传染病的网络模型/17.3 SIR模型
Content: 17.3 SIR模型

SIR：S→I(传染率 beta)，I→R(康复率 gamma)。S+I+R 守恒。
"""
from __future__ import annotations

import logging

import numpy as np

from netlab import configure, new_figure, save_fig, setup_logging

log = logging.getLogger("17.3")


def sir_simulate(pop, beta, gamma, t_max, i0=1, seed=42):
    """随机 SIR，返回 (t, S, I, R) 各 shape (t_max+1,)。"""
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
        S.append(s)
        I.append(i)
        R.append(r)
    return np.arange(t_max + 1), np.array(S), np.array(I), np.array(R)


def viz(t, S, I, R):
    """绘制 S/I/R 随时间变化的曲线。"""
    configure()
    fig, ax = new_figure("SIR传播", "17.3")
    ax.plot(t, S, label="S")
    ax.plot(t, I, label="I")
    ax.plot(t, R, label="R")
    ax.set_xlabel("时间")
    ax.set_ylabel("人数")
    ax.legend()
    return save_fig(fig, "17.3", "sir")


def main() -> None:
    setup_logging(module="17.3", logfile="outputs/17.3/run.log")
    t, S, I, R = sir_simulate(1000, 0.3, 0.1, 300)
    log.info("sir peak_I=%s at_t=%s", int(I.max()), int(t[I.argmax()]))
    png = viz(t, S, I, R)
    log.info("figure saved=%s", png)


if __name__ == "__main__":
    main()