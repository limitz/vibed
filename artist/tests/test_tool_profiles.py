"""Tests for tool_profiles module."""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tool_profiles import get_profile, list_tools, ToolProfile


class TestGetProfile:
    def test_all_tools_return_profile(self):
        for tool in list_tools():
            p = get_profile(tool)
            assert isinstance(p, ToolProfile)
            assert p.name == tool

    def test_unknown_tool_raises(self):
        with pytest.raises(ValueError, match="Unknown tool"):
            get_profile("crayon")

    def test_base_width_positive(self):
        for tool in list_tools():
            assert get_profile(tool).base_width > 0

    def test_edge_softness_in_range(self):
        for tool in list_tools():
            p = get_profile(tool)
            assert 0.0 <= p.edge_softness <= 1.0

    def test_angle_sensitivity_in_range(self):
        for tool in list_tools():
            p = get_profile(tool)
            assert 0.0 <= p.angle_sensitivity <= 1.0


class TestPressureCurves:
    def test_width_fn_returns_float(self):
        for tool in list_tools():
            p = get_profile(tool)
            for pressure in [0.0, 0.25, 0.5, 0.75, 1.0]:
                result = p.pressure_width_fn(pressure)
                assert isinstance(result, float)
                assert result > 0

    def test_opacity_fn_returns_float(self):
        for tool in list_tools():
            p = get_profile(tool)
            for pressure in [0.0, 0.25, 0.5, 0.75, 1.0]:
                result = p.pressure_opacity_fn(pressure)
                assert isinstance(result, float)
                assert 0.0 <= result <= 1.0

    def test_pen_high_opacity(self):
        p = get_profile("pen")
        assert p.pressure_opacity_fn(0.0) >= 0.8

    def test_pencil_low_opacity_at_zero(self):
        p = get_profile("pencil")
        assert p.pressure_opacity_fn(0.0) < 0.3

    def test_brush_wide_width_range(self):
        p = get_profile("brush")
        w_min = p.pressure_width_fn(0.0)
        w_max = p.pressure_width_fn(1.0)
        assert w_max / w_min > 3.0

    def test_marker_constant_opacity(self):
        p = get_profile("marker")
        assert p.pressure_opacity_fn(0.0) == p.pressure_opacity_fn(1.0)


class TestListTools:
    def test_returns_list(self):
        tools = list_tools()
        assert isinstance(tools, list)
        assert len(tools) >= 6

    def test_contains_expected_tools(self):
        tools = list_tools()
        for expected in ["pen", "pencil", "brush", "charcoal", "marker", "eraser"]:
            assert expected in tools
