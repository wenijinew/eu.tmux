"""Tests for peelee color conversion functions (used by eu.tmux)."""

from peelee.peelee import hex2hls, hls2hex, rgb2hex


class TestHex2Hls:
    def test_black(self):
        h, l, s = hex2hls("#000000")
        assert l == 0.0

    def test_white(self):
        h, l, s = hex2hls("#FFFFFF")
        assert l == 1.0

    def test_red(self):
        h, l, s = hex2hls("#FF0000")
        assert h == 0.0
        assert s == 1.0

    def test_returns_tuple(self):
        assert len(hex2hls("#AABBCC")) == 3


class TestHls2Hex:
    def test_black(self):
        assert hls2hex((0.0, 0.0, 0.0)) == "#000000"

    def test_white(self):
        assert hls2hex((0.0, 1.0, 0.0)) == "#FFFFFF"

    def test_roundtrip(self):
        original = "#3A7B5C"
        hls = hex2hls(original)
        result = hls2hex(hls)
        for i in range(1, 7, 2):
            assert abs(int(result[i:i+2], 16) - int(original[i:i+2], 16)) <= 1


class TestRgb2Hex:
    def test_int_tuple(self):
        assert rgb2hex((255, 0, 128)) == "#FF0080"

    def test_float_tuple(self):
        result = rgb2hex((1.0, 0.0, 0.5))
        assert result in ("#FF007F", "#FF0080")

    def test_black(self):
        assert rgb2hex((0, 0, 0)) == "#000000"
