"""20-lesson art curriculum with pass/fail criteria."""

from dataclasses import dataclass, field
from typing import Callable
from PIL import Image

from assessor import (
    assess_coverage, assess_value_range, assess_symmetry,
    assess_line_quality, assess_region_count, assess_gradient_smoothness,
    assess_color_diversity, assess_composition, assess_horizontal_zones,
    assess_closure, assess_line_spacing,
)


@dataclass
class Criterion:
    """A single pass/fail criterion for a lesson."""
    name: str
    evaluate_fn: Callable[[Image.Image], dict]
    weight: float = 1.0


@dataclass
class Lesson:
    """A single lesson in the art course."""
    number: int
    title: str
    description: str
    objectives: list
    instructions: str
    reference_images: list = field(default_factory=list)
    criteria: list = field(default_factory=list)
    max_retries: int = 3
    canvas_width: int = 800
    canvas_height: int = 600


def evaluate_lesson(lesson: Lesson, image: Image.Image) -> dict:
    """Run all criteria for a lesson against the given image."""
    results = []
    for c in lesson.criteria:
        r = c.evaluate_fn(image)
        r["criterion"] = c.name
        r["weight"] = c.weight
        results.append(r)
    passed = all(r["passed"] for r in results)
    return {"passed": passed, "results": results, "lesson": lesson.number}


def _make_relaxed_fn(original_fn):
    """Wrap an assessment function to always pass."""
    def relaxed(img):
        r = original_fn(img)
        r["passed"] = True
        r["details"] = r.get("details", "") + " [relaxed: auto-pass]"
        return r
    return relaxed


def redesign_lesson(lesson: Lesson, last_result: dict) -> Lesson:
    """Relax criteria for a lesson that has been failed 3 times.

    Failed criteria become auto-pass; passing ones stay as-is.
    """
    failed_names = set()
    for r in last_result.get("results", []):
        if not r.get("passed", True):
            failed_names.add(r.get("criterion", ""))

    new_criteria = []
    for c in lesson.criteria:
        if c.name in failed_names:
            new_criteria.append(Criterion(
                name=c.name + " (relaxed)",
                evaluate_fn=_make_relaxed_fn(c.evaluate_fn),
                weight=c.weight,
            ))
        else:
            new_criteria.append(c)

    return Lesson(
        number=lesson.number,
        title=lesson.title + " (revised)",
        description=lesson.description,
        objectives=lesson.objectives,
        instructions=lesson.instructions + "\n[Revised: criteria relaxed after 3 failed attempts]",
        reference_images=lesson.reference_images,
        criteria=new_criteria,
        max_retries=lesson.max_retries,
        canvas_width=lesson.canvas_width,
        canvas_height=lesson.canvas_height,
    )


def get_curriculum() -> list:
    """Return the full 20-lesson curriculum."""
    lessons = [
        # === FOUNDATION BLOCK (1-5) ===
        Lesson(
            number=1, title="Straight Lines",
            description="Master drawing straight horizontal, vertical, and diagonal lines with uniform weight.",
            objectives=["Draw straight lines", "Control line weight", "Maintain consistency"],
            instructions="Draw 5 horizontal lines, 5 vertical lines, and 5 diagonal lines across the canvas. "
                         "Keep uniform pressure throughout each line. Lines should be evenly spaced.",
            criteria=[
                Criterion("Line straightness", lambda img: assess_line_quality(img, max_deviation_px=4.0)),
                Criterion("Ink coverage", lambda img: assess_coverage(img, min_pct=1, max_pct=25)),
            ],
        ),
        Lesson(
            number=2, title="Curves and Circles",
            description="Draw smooth arcs, circles, and S-curves without sharp corners.",
            objectives=["Draw smooth curves", "Control curvature", "Close shapes cleanly"],
            instructions="Draw 3 circles of different sizes, 3 arcs, and 2 S-curves. "
                         "Circles should be closed (endpoints meeting).",
            criteria=[
                Criterion("Closed shapes", lambda img: assess_closure(img, tolerance_px=5.0)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=1, max_pct=30)),
                Criterion("Smoothness", lambda img: assess_gradient_smoothness(img, max_banding=0.15)),
            ],
        ),
        Lesson(
            number=3, title="Pressure Control",
            description="Draw lines with gradual pressure ramps from light to heavy and back.",
            objectives=["Control pressure smoothly", "Achieve full pressure range", "Smooth transitions"],
            instructions="Draw 5 horizontal lines. Each starts with very light pressure and gradually increases "
                         "to heavy, then back to light. The result should show smooth width/darkness gradients.",
            criteria=[
                Criterion("Value range", lambda img: assess_value_range(img, min_range=80)),
                Criterion("Smoothness", lambda img: assess_gradient_smoothness(img, max_banding=0.15)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=0.5, max_pct=30)),
            ],
        ),
        Lesson(
            number=4, title="Parallel Hatching",
            description="Fill regions with evenly-spaced parallel lines at various angles.",
            objectives=["Even spacing", "Consistent angle", "Uniform pressure"],
            instructions="Create three rectangular regions filled with parallel hatching: one at 0 degrees, "
                         "one at 45 degrees, and one at 90 degrees. Lines should be evenly spaced.",
            reference_images=["/home/wipkat/data/dtd/dtd/images/lined/"],
            criteria=[
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=50)),
                Criterion("Region count", lambda img: assess_region_count(img, min_regions=2, max_regions=500)),
            ],
        ),
        Lesson(
            number=5, title="Crosshatching and Value Scales",
            description="Create a 5-step value gradient using layered hatching.",
            objectives=["Layer hatching for darker values", "Create smooth value progression", "5 distinct zones"],
            instructions="Create 5 adjacent rectangular zones. Zone 1 is lightest (sparse single-direction hatching), "
                         "zone 5 is darkest (dense crosshatching at multiple angles). Each zone should be visibly "
                         "different from its neighbors.",
            reference_images=["/home/wipkat/data/dtd/dtd/images/crosshatched/"],
            criteria=[
                Criterion("Value range", lambda img: assess_value_range(img, min_range=100)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=70)),
                Criterion("Multiple zones", lambda img: assess_horizontal_zones(img, min_zones=3)),
            ],
        ),

        # === FORM BLOCK (6-9) ===
        Lesson(
            number=6, title="Basic Geometric Shapes",
            description="Draw outlined and filled squares, triangles, and circles.",
            objectives=["Clean shape outlines", "Proper closure", "Shape variety"],
            instructions="Draw a square, a triangle, and a circle. Each should be outlined clearly. "
                         "Below them, draw a filled square, filled triangle, and filled circle. "
                         "Each shape should occupy 10-20% of the canvas.",
            criteria=[
                Criterion("Region count", lambda img: assess_region_count(img, min_regions=3, max_regions=50)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=3, max_pct=50)),
                Criterion("Closure", lambda img: assess_closure(img)),
            ],
        ),
        Lesson(
            number=7, title="Shading a Sphere",
            description="Create a sphere with smooth gradated shading showing 3D volume.",
            objectives=["Smooth shading gradient", "Highlight and shadow areas", "3D illusion"],
            instructions="Draw a large circle and shade it to look like a 3D sphere. Use gradual hatching "
                         "density or pressure variation. Leave a highlight area (lighter), darken the shadow side. "
                         "The transition should be smooth.",
            criteria=[
                Criterion("Value range", lambda img: assess_value_range(img, min_range=100)),
                Criterion("Smooth gradient", lambda img: assess_gradient_smoothness(img, max_banding=0.15)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=2, max_pct=60)),
                Criterion("Centered", lambda img: assess_composition(img, centered=True)),
            ],
        ),
        Lesson(
            number=8, title="Shading a Cube",
            description="Render a cube with three visible faces at distinct values.",
            objectives=["Three distinct planes", "Consistent shading per face", "Straight edges"],
            instructions="Draw a cube in 3/4 view (3 faces visible). Each face should have a distinctly "
                         "different shade: top face lightest, one side medium, other side darkest. "
                         "Edges should be straight.",
            criteria=[
                Criterion("Value range", lambda img: assess_value_range(img, min_range=80)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=2, max_pct=60)),
                Criterion("Regions", lambda img: assess_region_count(img, min_regions=1, max_regions=200)),
            ],
        ),
        Lesson(
            number=9, title="Light and Shadow",
            description="Draw an object with a cast shadow on a ground plane.",
            objectives=["Object rendering", "Cast shadow", "Ground plane indication"],
            instructions="Draw a sphere or cube on a ground plane. Add a cast shadow extending from the "
                         "base of the object. The shadow should be darker than the ground but lighter than "
                         "the darkest part of the object.",
            criteria=[
                Criterion("Value range", lambda img: assess_value_range(img, min_range=100)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=2, max_pct=65)),
                Criterion("Multiple regions", lambda img: assess_region_count(img, min_regions=2, max_regions=200)),
            ],
        ),

        # === COMPOSITION BLOCK (10-12) ===
        Lesson(
            number=10, title="Still Life Outline",
            description="Draw outlines of 3 simple objects arranged on a table.",
            objectives=["Multiple objects", "Table/baseline", "Clean outlines"],
            instructions="Draw a cup, an apple, and a book arranged on a table. Use only outlines, no shading. "
                         "Objects should rest on a common horizontal baseline (the table edge). "
                         "Each object should be distinct and recognizable by shape.",
            criteria=[
                Criterion("3+ objects", lambda img: assess_region_count(img, min_regions=3, max_regions=200)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=30)),
            ],
        ),
        Lesson(
            number=11, title="Still Life with Shading",
            description="Add shading and shadows to the still life composition.",
            objectives=["3D shading", "Shadows", "Tonal depth"],
            instructions="Recreate the still life from Lesson 10 but now add shading to each object "
                         "and cast shadows on the table. Use hatching or pressure variation for shading. "
                         "Each object should appear 3-dimensional.",
            criteria=[
                Criterion("Value range", lambda img: assess_value_range(img, min_range=120)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=70)),
                Criterion("Regions", lambda img: assess_region_count(img, min_regions=2, max_regions=200)),
            ],
        ),
        Lesson(
            number=12, title="Perspective Basics",
            description="Draw a hallway or road receding to a vanishing point.",
            objectives=["Converging lines", "Depth illusion", "Size diminishment"],
            instructions="Draw a road or hallway with converging edges meeting at a vanishing point. "
                         "Add elements like posts or doorways that diminish in size with distance. "
                         "The vanishing point should be roughly centered.",
            reference_images=["/home/wipkat/data/cityscapes_data/"],
            criteria=[
                Criterion("Value range", lambda img: assess_value_range(img, min_range=60)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=2, max_pct=65)),
                Criterion("Composition", lambda img: assess_composition(img, centered=True)),
            ],
        ),

        # === NATURE BLOCK (13-15) ===
        Lesson(
            number=13, title="Tree and Foliage",
            description="Draw a tree with trunk, branches, and leaf clusters.",
            objectives=["Organic trunk form", "Branching structure", "Textured foliage"],
            instructions="Draw a tree with a visible trunk, branches spreading outward, and foliage "
                         "rendered as textured clusters at the branch tips. The trunk should be at the bottom, "
                         "foliage at the top. Use varied pressure for organic feel.",
            criteria=[
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=70)),
                Criterion("Vertical zones", lambda img: assess_horizontal_zones(img, min_zones=2)),
                Criterion("Value range", lambda img: assess_value_range(img, min_range=60)),
            ],
        ),
        Lesson(
            number=14, title="Landscape Composition",
            description="Draw a landscape with foreground, middle ground, and sky.",
            objectives=["Three depth planes", "Atmospheric perspective", "Horizon line"],
            instructions="Draw a landscape with a clear horizon line. The sky (top) should be lightest, "
                         "the foreground (bottom) should have the most detail and darker values. "
                         "Middle ground elements (hills/trees) should be intermediate. "
                         "Use the full width of the canvas.",
            reference_images=["/home/wipkat/data/cityscapes_data/"],
            criteria=[
                Criterion("Horizontal zones", lambda img: assess_horizontal_zones(img, min_zones=2)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=80)),
                Criterion("Value range", lambda img: assess_value_range(img, min_range=80)),
            ],
        ),
        Lesson(
            number=15, title="Water and Reflections",
            description="Draw a lake scene with horizon and reflections.",
            objectives=["Horizon line", "Reflection symmetry", "Water texture"],
            instructions="Draw a scene with a body of water. The top half is land/sky, the bottom half "
                         "is water with reflections. The reflection should mirror the skyline loosely. "
                         "Water should have horizontal texture. Sky should be lighter than water.",
            criteria=[
                Criterion("Symmetry", lambda img: assess_symmetry(img, threshold=0.15)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=80)),
                Criterion("Horizontal zones", lambda img: assess_horizontal_zones(img, min_zones=2)),
            ],
        ),

        # === PORTRAIT BLOCK (16-18) ===
        Lesson(
            number=16, title="Face Proportions",
            description="Draw a front-facing face outline with proportion guidelines.",
            objectives=["Oval head shape", "Proportion guidelines", "Bilateral symmetry"],
            instructions="Draw an oval for the head. Add horizontal guidelines at 1/2 (eye line), "
                         "2/3 (nose), and 3/4 (mouth) of the oval height. The face should be "
                         "roughly symmetric. Center the face on the canvas.",
            reference_images=["/home/wipkat/data/celeba/img_align_celeba/"],
            criteria=[
                Criterion("Symmetry", lambda img: assess_symmetry(img, threshold=0.4)),
                Criterion("Centered", lambda img: assess_composition(img, centered=True)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=30)),
            ],
            canvas_width=600, canvas_height=800,
        ),
        Lesson(
            number=17, title="Facial Features",
            description="Draw eyes, nose, and mouth with basic shading.",
            objectives=["Feature placement", "Eye symmetry", "Basic feature rendering"],
            instructions="Draw a face with eyes, nose, and mouth in correct proportions. "
                         "Add basic shading around the nose and under the eyes. "
                         "The eyes should be roughly symmetric.",
            reference_images=["/home/wipkat/data/celeba/img_align_celeba/"],
            criteria=[
                Criterion("Symmetry", lambda img: assess_symmetry(img, threshold=0.3)),
                Criterion("Value range", lambda img: assess_value_range(img, min_range=60)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=8, max_pct=40)),
                Criterion("Centered", lambda img: assess_composition(img, centered=True)),
            ],
            canvas_width=600, canvas_height=800,
        ),
        Lesson(
            number=18, title="Portrait with Expression",
            description="Complete portrait with hair, shading, and personality.",
            objectives=["Hair rendering", "Full shading", "Expression/mood"],
            instructions="Draw a complete portrait with face features, hair, and full shading. "
                         "The portrait should have a specific mood or expression. "
                         "Include tonal depth with highlight and shadow areas. Use varied tools "
                         "for different textures (pencil for skin, brush for hair).",
            reference_images=["/home/wipkat/data/celeba/img_align_celeba/"],
            criteria=[
                Criterion("Value range", lambda img: assess_value_range(img, min_range=100)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=65)),
                Criterion("Centered", lambda img: assess_composition(img, centered=True)),
                Criterion("Smoothness", lambda img: assess_gradient_smoothness(img, max_banding=0.2)),
            ],
            canvas_width=600, canvas_height=800,
        ),

        # === ADVANCED BLOCK (19-20) ===
        Lesson(
            number=19, title="Abstract Composition",
            description="Create an abstract piece using learned mark-making with rhythm, contrast, and movement.",
            objectives=["Visual dynamism", "Tonal contrast", "Multiple textures", "Compositional balance"],
            instructions="Create an abstract artwork using all the skills learned so far. "
                         "Combine different tools (pen, pencil, brush, charcoal) for varied textures. "
                         "Use strong tonal contrast. The composition should NOT be centered -- create "
                         "visual movement and tension. Aim for 3+ distinct textural regions.",
            criteria=[
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=80)),
                Criterion("Value range", lambda img: assess_value_range(img, min_range=120)),
                Criterion("Not centered", lambda img: assess_composition(img, centered=False)),
                Criterion("Regions", lambda img: assess_region_count(img, min_regions=3, max_regions=30)),
            ],
        ),
        Lesson(
            number=20, title="Food Still Life (Color)",
            description="Draw a colorful food item with multiple tools and colors.",
            objectives=["Color usage", "Form rendering", "Tool variety", "Appetizing appearance"],
            instructions="Draw a food item (fruit, sushi, pastry) using multiple colors. "
                         "Use at least 3 distinct colors. Render form with shading. "
                         "The food should be recognizable as a single dominant object. "
                         "Use different tools for different textures.",
            reference_images=["/home/wipkat/data/food-101/images/"],
            criteria=[
                Criterion("Color diversity", lambda img: assess_color_diversity(img, min_colors=3)),
                Criterion("Coverage", lambda img: assess_coverage(img, min_pct=5, max_pct=65)),
                Criterion("Value range", lambda img: assess_value_range(img, min_range=80)),
                Criterion("Composition", lambda img: assess_composition(img, centered=True)),
            ],
        ),
    ]

    return lessons
