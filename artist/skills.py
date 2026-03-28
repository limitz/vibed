"""Persistent skill system: reads/writes skills.md to accumulate drawing knowledge."""

import os
import re

SKILLS_PATH = os.path.join(os.path.dirname(__file__), "output", "skills.md")


def _ensure_dir():
    os.makedirs(os.path.dirname(SKILLS_PATH), exist_ok=True)


def init_skills():
    """Create a fresh skills.md with initial defaults."""
    _ensure_dir()
    content = """# Drawing Skills

## Tool Defaults
- pen_pressure: 0.6
- pencil_pressure: 0.5
- brush_pressure: 0.5
- charcoal_pressure: 0.5
- marker_pressure: 0.5

## Spacing
- hatching_spacing: 6.0
- crosshatch_spacing: 6.0
- fill_spacing: 2.0
- gradient_spacing: 3.0

## Stroke Settings
- events_per_line: 20
- events_per_curve: 40
- events_per_circle: 60
- jitter: 0.3

## Techniques Learned
(none yet)

## Lesson Log
(none yet)
"""
    with open(SKILLS_PATH, "w") as f:
        f.write(content)
    return load_skills()


def load_skills() -> dict:
    """Load skills from skills.md into a dictionary of parameters."""
    if not os.path.exists(SKILLS_PATH):
        return init_skills()

    with open(SKILLS_PATH, "r") as f:
        content = f.read()

    skills = {
        "pen_pressure": 0.6,
        "pencil_pressure": 0.5,
        "brush_pressure": 0.5,
        "charcoal_pressure": 0.5,
        "marker_pressure": 0.5,
        "hatching_spacing": 6.0,
        "crosshatch_spacing": 6.0,
        "fill_spacing": 2.0,
        "gradient_spacing": 3.0,
        "events_per_line": 20,
        "events_per_curve": 40,
        "events_per_circle": 60,
        "jitter": 0.3,
        "techniques": [],
        "raw": content,
    }

    # Parse numeric values from markdown
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("- ") and ":" in line:
            parts = line[2:].split(":")
            key = parts[0].strip()
            val_str = parts[1].strip()
            # Extract the number (might have annotations after it)
            match = re.match(r"([\d.]+)", val_str)
            if match and key in skills:
                try:
                    skills[key] = float(match.group(1))
                except ValueError:
                    pass

    # Parse techniques
    in_techniques = False
    for line in content.split("\n"):
        if "## Techniques Learned" in line:
            in_techniques = True
            continue
        if line.startswith("## ") and in_techniques:
            break
        if in_techniques and line.strip().startswith("- "):
            skills["techniques"].append(line.strip()[2:])

    return skills


def learn_from_assessment(lesson_number: int, lesson_title: str,
                          passed: bool, results: list, attempt: int):
    """Analyze assessment results and update skills.md with new knowledge."""
    _ensure_dir()
    skills = load_skills()

    new_techniques = []
    param_updates = {}

    for r in results:
        criterion = r.get("criterion", "")
        detail = r.get("details", "")
        score = r.get("score", 0)
        did_pass = r.get("passed", False)

        if not did_pass:
            # Learn from failure
            if "coverage" in criterion.lower():
                # Coverage too low or too high
                if "target:" in detail:
                    match = re.search(r"Coverage:\s*([\d.]+)%.*target:\s*(\d+)-(\d+)", detail)
                    if match:
                        actual = float(match.group(1))
                        target_min = float(match.group(2))
                        target_max = float(match.group(3))
                        if actual < target_min:
                            # Need more ink: increase pressure, decrease spacing
                            for tool in ["pencil_pressure", "pen_pressure", "brush_pressure", "charcoal_pressure"]:
                                new_val = min(0.95, skills[tool] + 0.08)
                                param_updates[tool] = new_val
                            for sp in ["hatching_spacing", "crosshatch_spacing", "fill_spacing"]:
                                new_val = max(1.5, skills[sp] - 0.8)
                                param_updates[sp] = new_val
                            new_techniques.append(
                                f"L{lesson_number}: coverage was {actual:.1f}%, needed {target_min}%+ → "
                                f"increased pressures, decreased spacing"
                            )
                        elif actual > target_max:
                            for tool in ["pencil_pressure", "pen_pressure"]:
                                new_val = max(0.15, skills[tool] - 0.05)
                                param_updates[tool] = new_val
                            for sp in ["hatching_spacing", "crosshatch_spacing"]:
                                new_val = min(15, skills[sp] + 1.0)
                                param_updates[sp] = new_val
                            new_techniques.append(
                                f"L{lesson_number}: coverage was {actual:.1f}%, needed <{target_max}% → "
                                f"decreased pressures, increased spacing"
                            )

            elif "value range" in criterion.lower():
                match = re.search(r"Value range:\s*(\d+).*target >= (\d+)", detail)
                if match:
                    actual = float(match.group(1))
                    target = float(match.group(2))
                    if actual < target:
                        new_techniques.append(
                            f"L{lesson_number}: value range {actual:.0f} too narrow (need {target:.0f}) → "
                            f"use wider pressure range in shading"
                        )

            elif "region" in criterion.lower():
                match = re.search(r"Regions:\s*(\d+).*target:\s*(\d+)-(\d+)", detail)
                if match:
                    actual = int(match.group(1))
                    tmin = int(match.group(2))
                    tmax = int(match.group(3))
                    if actual > tmax:
                        for sp in ["hatching_spacing", "fill_spacing"]:
                            new_val = max(1.0, skills[sp] - 1.0)
                            param_updates[sp] = new_val
                        new_techniques.append(
                            f"L{lesson_number}: {actual} regions (too many, max {tmax}) → "
                            f"decreased spacing for connected strokes"
                        )

            elif "symmetry" in criterion.lower():
                new_techniques.append(
                    f"L{lesson_number}: symmetry too low → mirror strokes more carefully"
                )

            elif "smoothness" in criterion.lower() or "banding" in criterion.lower():
                param_updates["events_per_line"] = min(60, skills["events_per_line"] + 5)
                param_updates["gradient_spacing"] = max(1.5, skills["gradient_spacing"] - 0.5)
                new_techniques.append(
                    f"L{lesson_number}: gradient not smooth → more events per stroke, finer spacing"
                )

        else:
            # Learn from success — record what worked
            if "coverage" in criterion.lower() and score > 0:
                new_techniques.append(
                    f"L{lesson_number}: coverage {score:.1f}% ✓ (current settings work for this range)"
                )

    # Apply updates to skills.md
    if param_updates or new_techniques:
        _update_skills_file(param_updates, new_techniques,
                            lesson_number, lesson_title, passed, attempt)


def _update_skills_file(param_updates: dict, new_techniques: list,
                        lesson_number: int, lesson_title: str,
                        passed: bool, attempt: int):
    """Rewrite skills.md with updated parameters and techniques."""
    if not os.path.exists(SKILLS_PATH):
        init_skills()

    with open(SKILLS_PATH, "r") as f:
        content = f.read()

    # Update parameter values in-place
    for key, value in param_updates.items():
        pattern = rf"(- {re.escape(key)}:\s*)[\d.]+"
        replacement = rf"\g<1>{value:.2f}"
        content = re.sub(pattern, replacement, content)

    # Add new techniques
    if new_techniques:
        tech_marker = "## Techniques Learned"
        if tech_marker in content:
            idx = content.index(tech_marker) + len(tech_marker)
            # Find end of the line
            nl = content.index("\n", idx)
            insert_text = "\n" + "\n".join(f"- {t}" for t in new_techniques)
            # Remove "(none yet)" if present
            content = content.replace("(none yet)\n\n## Lesson Log", "\n## Lesson Log")
            # Insert after header
            if tech_marker in content:
                idx = content.index(tech_marker) + len(tech_marker)
                nl = content.index("\n", idx)
                content = content[:nl] + insert_text + content[nl:]

    # Add lesson log entry
    status = "PASSED" if passed else "FAILED"
    log_entry = f"\n- Lesson {lesson_number} ({lesson_title}): {status} on attempt {attempt}"
    log_marker = "## Lesson Log"
    if log_marker in content:
        content = content.replace("(none yet)", "")
        idx = content.index(log_marker) + len(log_marker)
        nl = content.index("\n", idx)
        content = content[:nl] + log_entry + content[nl:]

    with open(SKILLS_PATH, "w") as f:
        f.write(content)


def get_tool_pressure(skills: dict, tool: str) -> float:
    """Get the current learned pressure for a tool."""
    key = f"{tool}_pressure"
    return skills.get(key, 0.5)


def get_spacing(skills: dict, kind: str = "hatching") -> float:
    """Get the current learned spacing for a type of fill."""
    key = f"{kind}_spacing"
    return skills.get(key, 6.0)
