"""Tests for course module."""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PIL import Image
from course import get_curriculum, evaluate_lesson, redesign_lesson, Lesson, Criterion


class TestCurriculum:
    def test_has_20_lessons(self):
        curriculum = get_curriculum()
        assert len(curriculum) == 20

    def test_sequential_numbering(self):
        curriculum = get_curriculum()
        for i, lesson in enumerate(curriculum):
            assert lesson.number == i + 1

    def test_all_have_titles(self):
        for lesson in get_curriculum():
            assert lesson.title
            assert len(lesson.title) > 2

    def test_all_have_descriptions(self):
        for lesson in get_curriculum():
            assert lesson.description
            assert len(lesson.description) > 10

    def test_all_have_objectives(self):
        for lesson in get_curriculum():
            assert len(lesson.objectives) >= 2

    def test_all_have_instructions(self):
        for lesson in get_curriculum():
            assert lesson.instructions
            assert len(lesson.instructions) > 20

    def test_all_have_criteria(self):
        for lesson in get_curriculum():
            assert len(lesson.criteria) >= 2

    def test_criteria_are_callable(self):
        white = Image.new("RGB", (200, 150), (255, 255, 255))
        for lesson in get_curriculum():
            for c in lesson.criteria:
                r = c.evaluate_fn(white)
                assert "passed" in r
                assert "score" in r

    def test_canvas_dimensions_positive(self):
        for lesson in get_curriculum():
            assert lesson.canvas_width > 0
            assert lesson.canvas_height > 0


class TestEvaluateLesson:
    def test_returns_dict(self):
        lesson = get_curriculum()[0]
        white = Image.new("RGB", (200, 150), (255, 255, 255))
        result = evaluate_lesson(lesson, white)
        assert "passed" in result
        assert "results" in result
        assert "lesson" in result

    def test_blank_image_fails_most_lessons(self):
        white = Image.new("RGB", (200, 150), (255, 255, 255))
        failures = 0
        for lesson in get_curriculum():
            result = evaluate_lesson(lesson, white)
            if not result["passed"]:
                failures += 1
        # A blank image should fail most lessons
        assert failures >= 15


class TestRedesignLesson:
    def test_redesign_preserves_number(self):
        lesson = get_curriculum()[0]
        fake_result = {"passed": False, "results": []}
        revised = redesign_lesson(lesson, fake_result)
        assert revised.number == lesson.number

    def test_redesign_marks_revised(self):
        lesson = get_curriculum()[0]
        revised = redesign_lesson(lesson, {"passed": False, "results": []})
        assert "revised" in revised.title.lower() or "revised" in revised.instructions.lower()

    def test_redesign_keeps_criteria_count(self):
        lesson = get_curriculum()[0]
        revised = redesign_lesson(lesson, {"passed": False, "results": []})
        assert len(revised.criteria) == len(lesson.criteria)
