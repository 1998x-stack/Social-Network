"""占位：3.4 来自于档案或第三方的数据"""
from tests.conftest import load_section

def test_skeleton_placeholder():
    sec = load_section("第Ⅰ部分_网络的实证研究/第3章_社会网络/3.4_来自于档案或第三方的数据/3.4_来自于档案或第三方的数据.py")
    assert sec is not None
