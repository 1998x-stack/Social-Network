import pytest

from netlab import demos


def test_known_keys_registered():
    for key in ("7.3", "10.3", "14.2", "17.3", "6.13"):
        assert key in demos.SECTION_PATHS


def test_unknown_key_raises():
    with pytest.raises(KeyError):
        demos.run_demo("99.99")