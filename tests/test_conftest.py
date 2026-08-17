from tests.conftest import load_section


def test_load_section_loads_any_file(tmp_path):
    demo = tmp_path / "带点号.py"
    demo.write_text("VALUE = 42\n")
    mod = load_section(str(demo))
    assert mod.VALUE == 42