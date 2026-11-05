"""Regression coverage for non-destructive README generation."""
from pathlib import Path

import pytest

from netlab import generate


def test_default_preserves_readme(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    readme = tmp_path / "README.md"
    original = b"# Curated README\n\nManual setup and evidence.\n"
    readme.write_bytes(original)
    monkeypatch.setattr(generate, "ROOT", tmp_path)
    monkeypatch.setattr(generate, "gen_doc_skeletons", lambda: 0)
    monkeypatch.setattr(generate, "gen_test_skeletons", lambda: 0)
    generate.main([])
    assert readme.read_bytes() == original


def test_explicit_overwrite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("curated", encoding="utf-8")
    monkeypatch.setattr(generate, "ROOT", tmp_path)
    monkeypatch.setattr(generate, "gen_doc_skeletons", lambda: 0)
    monkeypatch.setattr(generate, "gen_test_skeletons", lambda: 0)
    monkeypatch.setattr(generate, "walk", lambda: iter(()))
    generate.main(["--overwrite-readme"])
    assert readme.read_text(encoding="utf-8").startswith("# 网络的实证研究")


def test_unknown_flag_fails_before_writes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("unchanged", encoding="utf-8")
    monkeypatch.setattr(generate, "ROOT", tmp_path)
    with pytest.raises(SystemExit) as exc:
        generate.main(["--not-a-real-flag"])
    assert exc.value.code == 2
    assert readme.read_text(encoding="utf-8") == "unchanged"
