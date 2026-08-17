"""占位：3.6 小世界实验"""
from tests.conftest import load_section

def test_skeleton_placeholder():
    sec = load_section("第Ⅰ部分_网络的实证研究/第3章_社会网络/3.6_小世界实验/3.6_小世界实验.py")
    assert sec is not None
