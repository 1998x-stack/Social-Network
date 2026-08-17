import matplotlib

matplotlib.use("Agg")  # 无窗口 backend


from netlab import plotting


def test_configure_sets_dpi():
    plotting.configure()
    import matplotlib as mpl

    assert mpl.rcParams["figure.dpi"] == 300


def test_save_fig_creates_png(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "OUTPUT_DIR", tmp_path)
    fig, ax = plotting.new_figure("测试标题", title_key="test")
    ax.plot([1, 2, 3])
    out = plotting.save_fig(fig, "7.3", "katz")
    assert out.exists()
    assert out.suffix == ".png"
    assert "7.3" in str(out)