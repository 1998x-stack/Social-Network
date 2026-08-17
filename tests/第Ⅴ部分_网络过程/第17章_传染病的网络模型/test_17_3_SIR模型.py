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