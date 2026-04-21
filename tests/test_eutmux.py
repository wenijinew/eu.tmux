"""Tests for eutmux.py — theme classes and utility functions."""

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from eutmux import get, Theme, ThemeComponent, ThemeStatusLeft, ThemeStatusRight, ThemeWindow, Constructor, EMPTY


# --- get() helper ---

class TestGet:
    def test_returns_value(self):
        assert get({"k": "v"}, "k", "default") == "v"

    def test_returns_default_when_none(self):
        assert get({"k": None}, "k", "default") == "default"

    def test_returns_default_when_empty(self):
        assert get({"k": "  "}, "k", "default") == "default"

    def test_returns_default_when_missing(self):
        assert get({}, "k", "default") == "default"

    def test_preserves_whitespace_value(self):
        assert get({"k": " x "}, "k", "default") == " x "


# --- ThemeComponent ---

MOCK_STATUS_LINE = {
    "foreground": "#FFFFFF",
    "background": "#000000",
    "left_icon": "",
    "left_decorator": "",
    "style": "nobold",
}

MOCK_SECTION = {
    "fg_format": "#AAAAAA",
    "bg_format": "#333333",
    "fg_icon": "#BBBBBB",
    "bg_icon": "#444444",
    "fg_decorator": "#CCCCCC",
    "bg_decorator": "#555555",
    "icon": "⚡",
    "decorator": "",
    "style": "bold",
}


class TestThemeComponent:
    def test_load_common(self):
        tc = ThemeComponent()
        tc._load_common(MOCK_SECTION, MOCK_STATUS_LINE)
        assert tc.fg_icon == "#BBBBBB"
        assert tc.style == "bold"

    def test_common_dict_keys(self):
        tc = ThemeComponent()
        tc._load_common(MOCK_SECTION, MOCK_STATUS_LINE)
        d = tc._common_dict()
        assert set(d.keys()) == {"fg_icon", "bg_icon", "fg_decorator", "bg_decorator", "icon", "decorator", "style"}

    def test_falls_back_to_status_line(self):
        tc = ThemeComponent()
        tc._load_common({}, MOCK_STATUS_LINE)
        assert tc.fg_icon == "#FFFFFF"
        assert tc.icon == ""


# --- Theme classes ---

MOCK_THEME_CONFIG = {
    "status_line": MOCK_STATUS_LINE,
    "status_left": MOCK_SECTION,
    "status_right": MOCK_SECTION,
    "window": {
        "active": MOCK_SECTION,
        "inactive": MOCK_SECTION,
    },
}


class TestTheme:
    def test_creates_all_sections(self):
        theme = Theme(MOCK_THEME_CONFIG)
        assert theme.status_left is not None
        assert theme.status_right is not None
        assert "active" in theme.window
        assert "inactive" in theme.window

    def test_dict_access(self):
        theme = Theme(MOCK_THEME_CONFIG)
        assert theme.get("terminal") == MOCK_THEME_CONFIG.get("terminal")
        assert theme.get("status_line") == MOCK_STATUS_LINE


class TestThemeStatusLeft:
    def test_has_fg_bg_format(self):
        tsl = ThemeStatusLeft(MOCK_THEME_CONFIG)
        assert tsl.fg_format is not None
        assert tsl.bg_format is not None

    def test_dict_access(self):
        tsl = ThemeStatusLeft(MOCK_THEME_CONFIG)
        assert tsl.get("style") == "bold"


class TestThemeWindow:
    def test_has_window_fields(self):
        section = {**MOCK_SECTION, "fg_window": "#AAAAAA", "bg_window": "#333333",
                   "fg_window_index": "#BBBBBB", "bg_window_index": "#444444"}
        tw = ThemeWindow(MOCK_STATUS_LINE, section)
        assert tw.fg_window == "#AAAAAA"
        assert tw.bg_window == "#333333"
