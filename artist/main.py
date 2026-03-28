"""Main orchestrator: runs all 4 stages of the artist project."""

import os
import sys
import json
import time

from stylus_format import Drawing, Stroke, StylusEvent, save_drawing
from tool_profiles import list_tools
from renderer import render_drawing
from student import (
    draw_line, draw_circle, draw_rectangle, draw_pressure_ramp,
    draw_hatching, draw_s_curve, draw_filled_circle, take_lesson,
)
from course import get_curriculum, evaluate_lesson, redesign_lesson
from assessor import assess_coverage
from skills import init_skills, load_skills, learn_from_assessment


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


# ================================================================
# STAGE 1: Build and test the drawing engine
# ================================================================

def stage1_build_engine():
    """Generate test drawings to verify and refine the rendering engine."""
    print("=" * 60)
    print("STAGE 1: Building and testing the drawing engine")
    print("=" * 60)

    out = os.path.join(OUTPUT_DIR, "stage1")
    ensure_dir(out)

    # Test 1: Line sampler - all tools
    print("\n  [1/5] Line sampler (all tools)...")
    _make_line_sampler(out)

    # Test 2: Pressure test
    print("  [2/5] Pressure variation test...")
    _make_pressure_test(out)

    # Test 3: Color test
    print("  [3/5] Color palette test...")
    _make_color_test(out)

    # Test 4: Shape test
    print("  [4/5] Shape test...")
    _make_shape_test(out)

    # Test 5: Complete scene test
    print("  [5/5] Complete scene test...")
    _make_scene_test(out)

    print(f"\n  Stage 1 complete. Outputs saved to {out}/")


def _make_line_sampler(out):
    strokes = []
    tools = list_tools()
    y = 50
    for tool in tools:
        strokes.append(draw_line(50, y, 750, y, tool=tool, pressure=0.6, num_events=40))
        y += 80
    d = Drawing(width=800, height=y + 30, strokes=strokes)
    save_drawing(d, os.path.join(out, "line_sampler.json"))
    img = render_drawing(d, apply_paper=True)
    img.convert("RGB").save(os.path.join(out, "line_sampler.png"))


def _make_pressure_test(out):
    strokes = []
    for i, tool in enumerate(["pen", "pencil", "brush", "charcoal"]):
        y = 60 + i * 100
        strokes.append(draw_pressure_ramp(50, y, 750, y, tool=tool, num_events=50))
    d = Drawing(width=800, height=460, strokes=strokes)
    save_drawing(d, os.path.join(out, "pressure_test.json"))
    img = render_drawing(d, apply_paper=True)
    img.convert("RGB").save(os.path.join(out, "pressure_test.png"))


def _make_color_test(out):
    strokes = []
    colors = ["red", "blue", "green", "orange", "purple", "brown", "cyan", "pink"]
    for i, color in enumerate(colors):
        y = 40 + i * 55
        strokes.append(draw_line(50, y, 500, y, tool="brush", color=color, pressure=0.7, num_events=30))
    d = Drawing(width=560, height=40 + len(colors) * 55, strokes=strokes)
    save_drawing(d, os.path.join(out, "color_test.json"))
    img = render_drawing(d, apply_paper=True)
    img.convert("RGB").save(os.path.join(out, "color_test.png"))


def _make_shape_test(out):
    strokes = []
    strokes.append(draw_circle(150, 150, 80, tool="pen", pressure=0.6))
    strokes.append(draw_rectangle(300, 70, 160, 160, tool="pen", pressure=0.6))
    strokes.extend(draw_hatching(550, 70, 150, 150, angle_deg=45, spacing=8, tool="pencil", pressure=0.4))
    strokes.extend(draw_filled_circle(150, 380, 70, tool="brush", color="blue", pressure=0.5))
    strokes.append(draw_s_curve(320, 300, 500, 400, amplitude=50, tool="pen", pressure=0.5))
    d = Drawing(width=750, height=480, strokes=strokes)
    save_drawing(d, os.path.join(out, "shape_test.json"))
    img = render_drawing(d, apply_paper=True)
    img.convert("RGB").save(os.path.join(out, "shape_test.png"))


def _make_scene_test(out):
    """A small scene combining multiple techniques."""
    strokes = []
    # Ground
    strokes.append(draw_line(0, 400, 800, 400, tool="pen", pressure=0.4))
    strokes.extend(draw_hatching(0, 400, 800, 100, angle_deg=0, spacing=4, tool="pencil", pressure=0.2))
    # Sun
    strokes.append(draw_circle(650, 80, 40, tool="brush", color="orange", pressure=0.7))
    strokes.extend(draw_filled_circle(650, 80, 38, tool="brush", color="yellow", pressure=0.4))
    # House
    strokes.append(draw_rectangle(200, 280, 180, 120, tool="pen", pressure=0.6))
    # Roof
    from student import draw_triangle
    strokes.append(draw_triangle(190, 280, 390, 280, 290, 210, tool="pen", pressure=0.6))
    strokes.extend(draw_hatching(200, 280, 180, 120, angle_deg=0, spacing=5, tool="pencil", pressure=0.3))
    # Door
    strokes.append(draw_rectangle(270, 340, 40, 60, tool="pen", pressure=0.5))
    # Tree
    strokes.append(draw_line(550, 400, 550, 300, tool="pencil", color="brown", pressure=0.6))
    strokes.append(draw_circle(550, 270, 40, tool="pencil", color="green", pressure=0.5))
    strokes.extend(draw_filled_circle(550, 270, 38, tool="pencil", color=(30, 120, 30), pressure=0.4, fill_spacing=3))

    d = Drawing(width=800, height=500, strokes=strokes)
    save_drawing(d, os.path.join(out, "scene_test.json"))
    img = render_drawing(d, apply_paper=True)
    img.convert("RGB").save(os.path.join(out, "scene_test.png"))


# ================================================================
# STAGE 2: Design the curriculum
# ================================================================

def stage2_design_course():
    """Generate and save the 20-lesson curriculum."""
    print("\n" + "=" * 60)
    print("STAGE 2: Designing the art course")
    print("=" * 60)

    out = os.path.join(OUTPUT_DIR, "stage2")
    ensure_dir(out)

    curriculum = get_curriculum()
    curriculum_data = []
    for lesson in curriculum:
        curriculum_data.append({
            "number": lesson.number,
            "title": lesson.title,
            "description": lesson.description,
            "objectives": lesson.objectives,
            "instructions": lesson.instructions,
            "canvas_width": lesson.canvas_width,
            "canvas_height": lesson.canvas_height,
            "criteria": [c.name for c in lesson.criteria],
            "reference_images": lesson.reference_images,
        })

    with open(os.path.join(out, "curriculum.json"), "w") as f:
        json.dump(curriculum_data, f, indent=2)

    # Print curriculum summary
    for lesson in curriculum:
        print(f"  Lesson {lesson.number:2d}: {lesson.title}")
        print(f"            Criteria: {', '.join(c.name for c in lesson.criteria)}")

    print(f"\n  Stage 2 complete. Curriculum saved to {out}/curriculum.json")


# ================================================================
# STAGE 3: Take the course
# ================================================================

def stage3_take_course():
    """Take all 20 lessons, retrying and redesigning as needed.

    After each attempt (pass or fail), the student learns from the assessment
    results and updates skills.md. Skills accumulate across all lessons.
    """
    print("\n" + "=" * 60)
    print("STAGE 3: Taking the art course")
    print("=" * 60)

    out = os.path.join(OUTPUT_DIR, "stage3")
    ensure_dir(out)

    # Initialize fresh skills for the course
    init_skills()
    print("  Initialized skills.md")

    curriculum = get_curriculum()
    results_log = []

    for lesson in curriculum:
        print(f"\n  --- Lesson {lesson.number}: {lesson.title} ---")
        current_lesson = lesson
        passed = False

        for attempt in range(1, current_lesson.max_retries + 1):
            print(f"    Attempt {attempt}/{current_lesson.max_retries}...", end=" ")

            drawing = take_lesson(current_lesson.number,
                                  current_lesson.canvas_width,
                                  current_lesson.canvas_height,
                                  attempt=attempt)
            img = render_drawing(drawing, apply_paper=True)
            result = evaluate_lesson(current_lesson, img)

            fname = f"lesson_{lesson.number:02d}_attempt_{attempt}"
            img.convert("RGB").save(os.path.join(out, fname + ".png"))
            save_drawing(drawing, os.path.join(out, fname + ".json"))

            # LEARN from this attempt (pass or fail)
            learn_from_assessment(lesson.number, lesson.title,
                                  result["passed"], result["results"], attempt)

            if result["passed"]:
                print("PASSED!")
                for r in result["results"]:
                    print(f"      {r['criterion']}: {r['details']}")
                results_log.append({
                    "lesson": lesson.number, "title": lesson.title,
                    "attempt": attempt, "passed": True,
                    "results": [{k: v for k, v in r.items() if k != "evaluate_fn"}
                                for r in result["results"]],
                })
                passed = True
                break
            else:
                print("FAILED")
                for r in result["results"]:
                    status = "PASS" if r["passed"] else "FAIL"
                    print(f"      [{status}] {r['criterion']}: {r['details']}")
                results_log.append({
                    "lesson": lesson.number, "title": lesson.title,
                    "attempt": attempt, "passed": False,
                    "results": [{k: v for k, v in r.items() if k != "evaluate_fn"}
                                for r in result["results"]],
                })

        if not passed:
            print(f"    Redesigning lesson {lesson.number}...")
            current_lesson = redesign_lesson(current_lesson, result)

            for attempt in range(1, 4):
                print(f"    Revised attempt {attempt}/3...", end=" ")
                drawing = take_lesson(lesson.number,
                                      current_lesson.canvas_width,
                                      current_lesson.canvas_height,
                                      attempt=10 + attempt)
                img = render_drawing(drawing, apply_paper=True)
                result = evaluate_lesson(current_lesson, img)

                fname = f"lesson_{lesson.number:02d}_revised_{attempt}"
                img.convert("RGB").save(os.path.join(out, fname + ".png"))

                # Learn from revised attempt too
                learn_from_assessment(lesson.number, lesson.title + " (revised)",
                                      result["passed"], result["results"], 10 + attempt)

                if result["passed"]:
                    print("PASSED! (revised)")
                    results_log.append({
                        "lesson": lesson.number, "title": current_lesson.title,
                        "attempt": f"revised_{attempt}", "passed": True,
                        "results": [{k: v for k, v in r.items() if k != "evaluate_fn"}
                                    for r in result["results"]],
                    })
                    passed = True
                    break
                else:
                    print("FAILED")
                    results_log.append({
                        "lesson": lesson.number, "title": current_lesson.title,
                        "attempt": f"revised_{attempt}", "passed": False,
                        "results": [{k: v for k, v in r.items() if k != "evaluate_fn"}
                                    for r in result["results"]],
                    })

        if not passed:
            print(f"    WARNING: Lesson {lesson.number} not passed after all attempts.")

    # Save results log (convert numpy types for JSON)
    def _json_safe(obj):
        if hasattr(obj, 'item'):  # numpy scalar
            return obj.item()
        raise TypeError(f"Not JSON serializable: {type(obj)}")

    with open(os.path.join(out, "results.json"), "w") as f:
        json.dump(results_log, f, indent=2, default=_json_safe)

    passed_count = len(set(r["lesson"] for r in results_log if r["passed"]))
    print(f"\n  Stage 3 complete. Passed {passed_count}/20 lessons.")
    print(f"  Results saved to {out}/results.json")
    return passed_count


# ================================================================
# STAGE 4: Create a masterpiece
# ================================================================

def stage4_masterpiece():
    """Create a final work of art combining all learned skills."""
    print("\n" + "=" * 60)
    print("STAGE 4: Creating the masterpiece")
    print("=" * 60)

    out = os.path.join(OUTPUT_DIR)
    ensure_dir(out)

    import numpy as np
    np.random.seed(2026)

    strokes = []
    W, H = 1920, 1080

    # === A sunset landscape over water ===
    # This combines: perspective, atmosphere, color, reflection, nature, composition

    # --- Sky gradient (warm sunset tones) ---
    for y in range(0, int(H * 0.42), 3):
        t = y / (H * 0.42)
        # Sunset: top is deep blue/purple, horizon is warm orange/red
        r = int(30 + t * 200)
        g = int(20 + t * 100)
        b = int(120 - t * 80)
        pressure = 0.25 + t * 0.15
        strokes.append(draw_line(0, y, W, y, tool="brush", color=(r, g, b),
                                 pressure=pressure, num_events=25))

    # --- Sun (golden disc near horizon) ---
    sun_cx, sun_cy = W * 0.55, H * 0.35
    sun_r = 45
    from student import draw_filled_circle, draw_arc, draw_curve
    strokes.extend(draw_filled_circle(sun_cx, sun_cy, sun_r,
                                      tool="brush", color=(255, 200, 50),
                                      pressure=0.5, fill_spacing=2))
    # Sun glow
    for r_off in range(5):
        gr = sun_r + 10 + r_off * 12
        strokes.append(draw_circle(sun_cx, sun_cy, gr,
                                   tool="brush", color=(255, 180, 40),
                                   pressure=0.08, num_events=40))

    # --- Clouds (wispy, warm-lit) ---
    cloud_specs = [
        (W * 0.15, H * 0.15, 120, 15), (W * 0.35, H * 0.10, 150, 18),
        (W * 0.70, H * 0.18, 130, 14), (W * 0.85, H * 0.12, 100, 12),
        (W * 0.50, H * 0.22, 110, 16),
    ]
    for ccx, ccy, cw, ch in cloud_specs:
        for i in range(8):
            y_off = np.random.normal(0, ch * 0.4)
            x_off = np.random.normal(0, cw * 0.3)
            strokes.append(draw_line(ccx + x_off - cw * 0.3, ccy + y_off,
                                     ccx + x_off + cw * 0.3, ccy + y_off,
                                     tool="brush", color=(240, 170, 120),
                                     pressure=0.15, num_events=12))

    # --- Distant mountains (silhouette) ---
    mountain_y = H * 0.38
    # Mountain ridge line
    ridge_pts = [(0, mountain_y + 20)]
    x = 0
    while x < W:
        x += np.random.uniform(30, 80)
        peak_h = np.random.uniform(20, 80)
        ridge_pts.append((x, mountain_y - peak_h))
        x += np.random.uniform(30, 80)
        ridge_pts.append((x, mountain_y + np.random.uniform(-10, 15)))
    ridge_pts.append((W, mountain_y + 15))

    # Fill mountains as dark silhouette
    horizon_y = H * 0.43
    for i in range(len(ridge_pts) - 1):
        x1, y1 = ridge_pts[i]
        x2, y2 = ridge_pts[i + 1]
        # Fill from ridge to horizon
        min_y = min(y1, y2)
        for fy in range(int(min_y), int(horizon_y), 2):
            # Interpolate x at this y
            strokes.append(draw_line(x1, fy, x2, fy,
                                     tool="brush", color=(40, 25, 50),
                                     pressure=0.5, num_events=8))

    # Mountain highlights (sunset catching peaks)
    for px, py in ridge_pts[1::2]:
        if py < mountain_y:
            strokes.append(draw_line(px - 15, py + 2, px + 5, py + 8,
                                     tool="brush", color=(180, 100, 60),
                                     pressure=0.2, num_events=6))

    # --- Water ---
    water_top = horizon_y + 2
    for y in range(int(water_top), H, 2):
        t = (y - water_top) / (H - water_top)
        # Water reflects sky colors but darker
        r = int(20 + (1 - t) * 120)
        g = int(30 + (1 - t) * 60)
        b = int(60 + (1 - t) * 40)
        pressure = 0.2 + t * 0.15
        strokes.append(draw_line(0, y, W, y, tool="brush", color=(r, g, b),
                                 pressure=pressure, num_events=20))

    # Sun reflection on water (golden streak)
    reflect_cx = sun_cx
    for y in range(int(water_top + 5), int(H * 0.85), 4):
        t = (y - water_top) / (H * 0.85 - water_top)
        width = 15 + t * 60  # Widens toward viewer
        wave = np.sin(y * 0.05) * (5 + t * 15)
        pressure = 0.35 * (1 - t * 0.5)
        strokes.append(draw_line(reflect_cx - width / 2 + wave, y,
                                 reflect_cx + width / 2 + wave, y,
                                 tool="brush", color=(255, 190, 60),
                                 pressure=pressure, num_events=8))

    # Water ripples (subtle horizontal lines)
    for i in range(40):
        ry = np.random.uniform(water_top + 20, H - 20)
        rx = np.random.uniform(50, W - 50)
        rw = np.random.uniform(40, 150)
        strokes.append(draw_line(rx, ry, rx + rw, ry + np.random.normal(0, 1),
                                 tool="pencil", color=(60, 70, 90),
                                 pressure=0.15, num_events=10))

    # --- Foreground: dark silhouette of reeds/grass on left ---
    for i in range(25):
        gx = np.random.uniform(20, W * 0.15)
        gy = H
        gh = np.random.uniform(60, 200)
        sway = np.random.normal(0, 10)
        strokes.append(draw_line(gx, gy, gx + sway, gy - gh,
                                 tool="pen", color=(15, 10, 20), pressure=0.6, num_events=12))

    # A few reeds on right too
    for i in range(15):
        gx = np.random.uniform(W * 0.88, W - 20)
        gy = H
        gh = np.random.uniform(40, 150)
        strokes.append(draw_line(gx, gy, gx + np.random.normal(0, 8), gy - gh,
                                 tool="pen", color=(15, 10, 20), pressure=0.5, num_events=10))

    # --- Small boat silhouette on water ---
    boat_cx = W * 0.35
    boat_y = H * 0.62
    # Hull
    strokes.append(draw_curve(
        [(boat_cx - 40, boat_y), (boat_cx - 35, boat_y + 12),
         (boat_cx, boat_y + 15), (boat_cx + 35, boat_y + 12),
         (boat_cx + 40, boat_y)],
        tool="pen", color=(20, 15, 25), pressure=0.7, num_events=25))
    # Fill hull
    for yo in range(0, 14, 2):
        hw = 38 * (1 - yo / 15)
        strokes.append(draw_line(boat_cx - hw, boat_y + yo,
                                 boat_cx + hw, boat_y + yo,
                                 tool="pen", color=(20, 15, 25), pressure=0.6, num_events=8))
    # Mast
    strokes.append(draw_line(boat_cx, boat_y, boat_cx, boat_y - 60,
                             tool="pen", color=(20, 15, 25), pressure=0.5, num_events=10))
    # Small flag/sail
    strokes.append(draw_curve(
        [(boat_cx, boat_y - 55), (boat_cx + 25, boat_y - 45),
         (boat_cx + 20, boat_y - 30), (boat_cx, boat_y - 25)],
        tool="brush", color=(30, 20, 35), pressure=0.4, num_events=15))

    # --- Birds (V shapes in distance) ---
    for bx, by in [(W * 0.3, H * 0.1), (W * 0.33, H * 0.12), (W * 0.28, H * 0.08),
                   (W * 0.65, H * 0.14), (W * 0.68, H * 0.16)]:
        wing = np.random.uniform(8, 15)
        strokes.append(draw_line(bx - wing, by + 3, bx, by, tool="pen", color=(30, 20, 40), pressure=0.3, num_events=5))
        strokes.append(draw_line(bx, by, bx + wing, by + 3, tool="pen", color=(30, 20, 40), pressure=0.3, num_events=5))

    # Create and render
    drawing = Drawing(width=W, height=H, strokes=strokes)
    print("  Rendering masterpiece...")
    img = render_drawing(drawing, apply_paper=True)

    # Save
    png_path = os.path.join(out, "masterpiece.png")
    img.convert("RGB").save(png_path, quality=95)
    save_drawing(drawing, os.path.join(out, "masterpiece.json"))

    print(f"  Masterpiece saved to {png_path}")
    print(f"  Canvas: {W}x{H}, Strokes: {len(strokes)}")

    # Quick quality check
    r = assess_coverage(img, min_pct=30, max_pct=95)
    print(f"  Coverage: {r['score']:.1f}%")

    return png_path


# ================================================================
# Main entry point
# ================================================================

def main():
    start = time.time()

    stage1_build_engine()
    stage2_design_course()
    passed = stage3_take_course()
    masterpiece_path = stage4_masterpiece()

    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print(f"All stages complete in {elapsed:.1f}s")
    print(f"Lessons passed: {passed}/20")
    print(f"Masterpiece: {masterpiece_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
