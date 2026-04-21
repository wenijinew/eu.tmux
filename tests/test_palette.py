"""Tests for palette.py color conversion functions."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from palette import hex2hls, hls2hex, rgb2hex


class TestHex2Hls:
    """Test hex to HLS conversion."""

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

    def test_strips_hash(self):
        result = hex2hls("#AABBCC")
        assert len(result) == 3


class TestHls2Hex:
    """Test HLS to hex conversion."""

    def test_black(self):
        assert hls2hex((0.0, 0.0, 0.0)) == "#000000"

    def test_white(self):
        assert hls2hex((0.0, 1.0, 0.0)) == "#FFFFFF"

    def test_roundtrip(self):
        original = "#3A7B5C"
        hls = hex2hls(original)
        result = hls2hex(hls)
        # Allow ±1 per channel due to float rounding
        for i in range(1, 7, 2):
            assert abs(int(result[i:i+2], 16) - int(original[i:i+2], 16)) <= 1


class TestRgb2Hex:
    """Test RGB to hex conversion."""

    def test_int_tuple(self):
        assert rgb2hex((255, 0, 128)) == "#FF0080"

    def test_float_tuple(self):
        result = rgb2hex((1.0, 0.0, 0.5))
        assert result in ("#FF007F", "#FF0080")  # float rounding

    def test_black(self):
        assert rgb2hex((0, 0, 0)) == "#000000"
