"""SVG generator for a photorealistic washing machine image."""

VALID_PASSES = ("base", "materials", "lighting", "details", "polish")


def generate_washing_machine_svg(width: int = 800, height: int = 900) -> str:
    """Generate complete SVG markup of a washing machine with all refinement passes applied."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
</defs>
</svg>'''
    for pass_name in VALID_PASSES:
        svg = refine_svg(svg, pass_name)
    return svg


def refine_svg(svg: str, pass_name: str) -> str:
    """Apply a named refinement pass to an existing SVG string."""
    if pass_name not in VALID_PASSES:
        raise ValueError(f"Invalid pass name: {pass_name}. Must be one of {VALID_PASSES}")

    dispatch = {
        "base": _apply_base,
        "materials": _apply_materials,
        "lighting": _apply_lighting,
        "details": _apply_details,
        "polish": _apply_polish,
    }
    return dispatch[pass_name](svg)


def _insert_before_close(svg: str, content: str) -> str:
    """Insert content before the closing </svg> tag."""
    return svg.replace("</svg>", f"{content}\n</svg>")


def _insert_into_defs(svg: str, content: str) -> str:
    """Insert content into the <defs> section."""
    return svg.replace("</defs>", f"{content}\n</defs>")


def _apply_base(svg: str) -> str:
    """Pass 1: Add base shapes - body, door, control panel, feet."""
    elements = '''
<!-- Background wall -->
<rect x="0" y="0" width="800" height="900" fill="#e8e4e0"/>
<rect x="0" y="720" width="800" height="180" fill="#c8c0b8"/>

<!-- Machine body -->
<rect id="body" x="150" y="120" width="500" height="580" rx="12" ry="12" fill="#f0f0f0" stroke="#cccccc" stroke-width="1"/>

<!-- Control panel area -->
<rect id="panel" x="150" y="120" width="500" height="110" rx="12" ry="0" fill="#e0e0e0"/>
<line x1="150" y1="230" x2="650" y2="230" stroke="#bbb" stroke-width="1"/>

<!-- Door outer ring -->
<circle id="door-frame" cx="400" cy="470" r="175" fill="none" stroke="#999" stroke-width="20"/>

<!-- Door glass -->
<circle id="door-glass" cx="400" cy="470" r="155" fill="#1a2a3a" fill-opacity="0.3"/>

<!-- Door inner circle (drum view) -->
<circle id="drum" cx="400" cy="470" r="140" fill="#111" fill-opacity="0.15"/>

<!-- Feet -->
<rect x="175" y="695" width="40" height="15" rx="3" fill="#888"/>
<rect x="585" y="695" width="40" height="15" rx="3" fill="#888"/>
'''
    return _insert_before_close(svg, elements)


def _apply_materials(svg: str) -> str:
    """Pass 2: Add gradients for realistic materials."""
    defs = '''
<!-- Body gradient: brushed metal with horizontal sheen -->
<linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#ffffff"/>
  <stop offset="15%" stop-color="#f8f8f8"/>
  <stop offset="40%" stop-color="#f2f2f2"/>
  <stop offset="60%" stop-color="#eaeaea"/>
  <stop offset="85%" stop-color="#e0e0e0"/>
  <stop offset="100%" stop-color="#d5d5d5"/>
</linearGradient>

<!-- Side sheen for 3D depth -->
<linearGradient id="bodySideGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#ffffff" stop-opacity="0.3"/>
  <stop offset="15%" stop-color="#ffffff" stop-opacity="0"/>
  <stop offset="85%" stop-color="#000000" stop-opacity="0"/>
  <stop offset="100%" stop-color="#000000" stop-opacity="0.08"/>
</linearGradient>

<!-- Panel gradient -->
<linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#e8e8e8"/>
  <stop offset="100%" stop-color="#d0d0d0"/>
</linearGradient>

<!-- Chrome ring gradient - more contrast for metallic look -->
<linearGradient id="chromeGrad" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="#d0d0d0"/>
  <stop offset="15%" stop-color="#f8f8f8"/>
  <stop offset="35%" stop-color="#ffffff"/>
  <stop offset="50%" stop-color="#a0a0a0"/>
  <stop offset="65%" stop-color="#cccccc"/>
  <stop offset="80%" stop-color="#f0f0f0"/>
  <stop offset="100%" stop-color="#b8b8b8"/>
</linearGradient>

<!-- Glass radial gradient - more transparent to show drum/clothes -->
<radialGradient id="glassGrad" cx="0.4" cy="0.35" r="0.65">
  <stop offset="0%" stop-color="#6699bb" stop-opacity="0.08"/>
  <stop offset="40%" stop-color="#4488aa" stop-opacity="0.15"/>
  <stop offset="75%" stop-color="#2a5577" stop-opacity="0.25"/>
  <stop offset="100%" stop-color="#1a3344" stop-opacity="0.45"/>
</radialGradient>

<!-- Water tint gradient for drum -->
<radialGradient id="waterGrad" cx="0.5" cy="0.6" r="0.5">
  <stop offset="0%" stop-color="#88bbdd" stop-opacity="0.12"/>
  <stop offset="100%" stop-color="#6699bb" stop-opacity="0.06"/>
</radialGradient>

<!-- Rubber seal gradient -->
<radialGradient id="rubberGrad" cx="0.5" cy="0.5" r="0.5">
  <stop offset="85%" stop-color="#444"/>
  <stop offset="95%" stop-color="#333"/>
  <stop offset="100%" stop-color="#222"/>
</radialGradient>

<!-- Door handle gradient -->
<linearGradient id="handleGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#ddd"/>
  <stop offset="30%" stop-color="#fff"/>
  <stop offset="50%" stop-color="#bbb"/>
  <stop offset="100%" stop-color="#999"/>
</linearGradient>

<!-- Knob gradient -->
<radialGradient id="knobGrad" cx="0.35" cy="0.35" r="0.65">
  <stop offset="0%" stop-color="#ffffff"/>
  <stop offset="50%" stop-color="#d0d0d0"/>
  <stop offset="100%" stop-color="#999999"/>
</radialGradient>

<!-- Wall gradient -->
<linearGradient id="wallGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#f0ece8"/>
  <stop offset="100%" stop-color="#e0dcd6"/>
</linearGradient>

<!-- Floor gradient -->
<linearGradient id="floorGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#c8c0b8"/>
  <stop offset="100%" stop-color="#b8b0a8"/>
</linearGradient>
'''
    svg = _insert_into_defs(svg, defs)

    # Apply gradients to existing shapes
    svg = svg.replace('fill="#e8e4e0"', 'fill="url(#wallGrad)"')
    svg = svg.replace('fill="#c8c0b8"', 'fill="url(#floorGrad)"')
    svg = svg.replace('id="body" x="150" y="120" width="500" height="580" rx="12" ry="12" fill="#f0f0f0"',
                       'id="body" x="150" y="120" width="500" height="580" rx="12" ry="12" fill="url(#bodyGrad)"')
    svg = svg.replace('id="panel" x="150" y="120" width="500" height="110" rx="12" ry="0" fill="#e0e0e0"',
                       'id="panel" x="150" y="120" width="500" height="110" rx="12" ry="0" fill="url(#panelGrad)"')
    svg = svg.replace('id="door-frame" cx="400" cy="470" r="175" fill="none" stroke="#999" stroke-width="20"',
                       'id="door-frame" cx="400" cy="470" r="175" fill="none" stroke="url(#chromeGrad)" stroke-width="22"')
    svg = svg.replace('id="door-glass" cx="400" cy="470" r="155" fill="#1a2a3a" fill-opacity="0.3"',
                       'id="door-glass" cx="400" cy="470" r="155" fill="url(#glassGrad)"')

    return svg


def _apply_lighting(svg: str) -> str:
    """Pass 3: Add shadows, highlights, and reflections."""
    defs = '''
<!-- Drop shadow filter -->
<filter id="dropShadow" x="-10%" y="-10%" width="130%" height="130%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="8" result="blur"/>
  <feOffset dx="5" dy="8" result="offsetBlur"/>
  <feFlood flood-color="#000000" flood-opacity="0.25" result="color"/>
  <feComposite in="color" in2="offsetBlur" operator="in" result="shadow"/>
  <feMerge>
    <feMergeNode in="shadow"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>

<!-- Soft inner glow for glass -->
<filter id="glassInnerShadow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="12" result="blur"/>
  <feOffset dx="0" dy="0"/>
  <feFlood flood-color="#000" flood-opacity="0.3"/>
  <feComposite in2="blur" operator="in"/>
</filter>

<!-- Subtle body highlight filter -->
<filter id="softGlow">
  <feGaussianBlur stdDeviation="3" result="blur"/>
  <feComposite in="SourceGraphic" in2="blur" operator="over"/>
</filter>
'''
    svg = _insert_into_defs(svg, defs)

    # Apply drop shadow to body
    svg = svg.replace('id="body"', 'id="body" filter="url(#dropShadow)"')

    lighting_elements = '''
<!-- Floor shadow (ellipse under machine) -->
<ellipse cx="400" cy="715" rx="260" ry="12" fill="#000" fill-opacity="0.15"/>

<!-- Body side sheen overlay for 3D depth -->
<rect x="150" y="120" width="500" height="580" rx="12" ry="12" fill="url(#bodySideGrad)"/>

<!-- Body left edge highlight -->
<rect x="152" y="122" width="3" height="576" rx="1" fill="#ffffff" fill-opacity="0.6"/>

<!-- Body top edge highlight -->
<rect x="152" y="121" width="496" height="2" rx="1" fill="#ffffff" fill-opacity="0.5"/>

<!-- Panel bottom shadow -->
<rect x="155" y="228" width="490" height="4" fill="#000" fill-opacity="0.08"/>

<!-- Glass reflection arc -->
<path d="M 310 390 Q 350 360, 420 370 Q 460 375, 480 400" fill="none" stroke="#ffffff" stroke-width="8" stroke-opacity="0.25" stroke-linecap="round"/>
<path d="M 325 400 Q 360 375, 415 383 Q 445 388, 465 408" fill="none" stroke="#ffffff" stroke-width="4" stroke-opacity="0.15" stroke-linecap="round"/>

<!-- Small specular highlight on glass -->
<ellipse cx="350" cy="400" rx="15" ry="8" fill="#ffffff" fill-opacity="0.2" transform="rotate(-25 350 400)"/>

<!-- Chrome ring highlight -->
<path d="M 240 400 A 175 175 0 0 1 400 295" fill="none" stroke="#ffffff" stroke-width="3" stroke-opacity="0.4" stroke-linecap="round"/>

<!-- Right body shadow -->
<rect x="646" y="122" width="3" height="576" rx="1" fill="#000" fill-opacity="0.1"/>
'''
    return _insert_before_close(svg, lighting_elements)


def _apply_details(svg: str) -> str:
    """Pass 4: Add door handle, knobs, display, drawer, drum pattern, clothes."""
    defs = '''
<!-- Clip path for drum contents -->
<clipPath id="drumClip">
  <circle cx="400" cy="470" r="140"/>
</clipPath>

<!-- Display text glow -->
<filter id="displayGlow">
  <feGaussianBlur stdDeviation="1.5" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
'''
    svg = _insert_into_defs(svg, defs)

    detail_elements = '''
<!-- Door handle -->
<g id="door-handle">
  <rect x="540" y="455" width="45" height="14" rx="7" fill="url(#handleGrad)" stroke="#aaa" stroke-width="0.5"/>
  <rect x="543" y="458" width="39" height="2" rx="1" fill="#fff" fill-opacity="0.3"/>
  <!-- Handle mount points -->
  <circle cx="548" cy="462" r="3" fill="#bbb" stroke="#999" stroke-width="0.5"/>
  <circle cx="578" cy="462" r="3" fill="#bbb" stroke="#999" stroke-width="0.5"/>
</g>

<!-- Control panel details -->
<g id="panel-details">
  <!-- Detergent drawer -->
  <rect x="170" y="140" width="80" height="30" rx="3" fill="#d8d8d8" stroke="#bbb" stroke-width="0.5"/>
  <rect x="195" y="152" width="30" height="4" rx="2" fill="#ccc"/>

  <!-- LCD display -->
  <g id="display">
    <rect x="320" y="145" width="100" height="40" rx="4" fill="#1a1a2a"/>
    <rect x="322" y="147" width="96" height="36" rx="3" fill="#111122"/>
    <text x="370" y="172" text-anchor="middle" font-family="monospace" font-size="18" fill="#00ccff" filter="url(#displayGlow)">60°C</text>
    <text x="370" y="178" text-anchor="middle" font-family="monospace" font-size="7" fill="#0088aa">COTTON</text>
  </g>

  <!-- Control knobs -->
  <g id="knob1" transform="translate(480, 165)">
    <circle r="18" fill="url(#knobGrad)" stroke="#aaa" stroke-width="1"/>
    <circle r="14" fill="none" stroke="#ccc" stroke-width="0.5"/>
    <line x1="0" y1="-14" x2="0" y2="-8" stroke="#666" stroke-width="2" stroke-linecap="round"/>
    <!-- Tick marks -->
    <line x1="-12" y1="-8" x2="-9" y2="-6" stroke="#999" stroke-width="0.5"/>
    <line x1="12" y1="-8" x2="9" y2="-6" stroke="#999" stroke-width="0.5"/>
    <line x1="-14" y1="0" x2="-10" y2="0" stroke="#999" stroke-width="0.5"/>
    <line x1="14" y1="0" x2="10" y2="0" stroke="#999" stroke-width="0.5"/>
  </g>

  <g id="knob2" transform="translate(540, 165)">
    <circle r="15" fill="url(#knobGrad)" stroke="#aaa" stroke-width="1"/>
    <circle r="11" fill="none" stroke="#ccc" stroke-width="0.5"/>
    <line x1="5" y1="-10" x2="3" y2="-6" stroke="#666" stroke-width="2" stroke-linecap="round"/>
  </g>

  <g id="knob3" transform="translate(600, 165)">
    <circle r="15" fill="url(#knobGrad)" stroke="#aaa" stroke-width="1"/>
    <circle r="11" fill="none" stroke="#ccc" stroke-width="0.5"/>
    <line x1="-5" y1="-10" x2="-3" y2="-6" stroke="#666" stroke-width="2" stroke-linecap="round"/>
  </g>

  <!-- Power button -->
  <circle cx="270" cy="165" r="10" fill="#333" stroke="#555" stroke-width="1"/>
  <path d="M 270 157 L 270 162" stroke="#0f0" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M 264 160 A 8 8 0 1 0 276 160" fill="none" stroke="#0f0" stroke-width="1" stroke-linecap="round"/>

  <!-- Status LED -->
  <circle cx="295" cy="190" r="3" fill="#00ff44" fill-opacity="0.8"/>
  <circle cx="295" cy="190" r="5" fill="#00ff44" fill-opacity="0.15"/>
</g>

<!-- Drum pattern (perforated holes visible through glass) -->
<g clip-path="url(#drumClip)" opacity="0.35">
  <!-- Drum holes in concentric rings -->
  <g fill="#222" stroke="#333" stroke-width="0.3">
    <!-- Inner ring -->
    <circle cx="370" cy="430" r="3"/><circle cx="390" cy="425" r="3"/>
    <circle cx="410" cy="425" r="3"/><circle cx="430" cy="430" r="3"/>
    <circle cx="440" cy="450" r="3"/><circle cx="440" cy="470" r="3"/>
    <circle cx="440" cy="490" r="3"/><circle cx="430" cy="510" r="3"/>
    <circle cx="410" cy="515" r="3"/><circle cx="390" cy="515" r="3"/>
    <circle cx="370" cy="510" r="3"/><circle cx="360" cy="490" r="3"/>
    <circle cx="360" cy="470" r="3"/><circle cx="360" cy="450" r="3"/>
    <!-- Middle ring -->
    <circle cx="340" cy="420" r="2.5"/><circle cx="365" cy="405" r="2.5"/>
    <circle cx="395" cy="400" r="2.5"/><circle cx="425" cy="405" r="2.5"/>
    <circle cx="450" cy="420" r="2.5"/><circle cx="460" cy="445" r="2.5"/>
    <circle cx="465" cy="470" r="2.5"/><circle cx="460" cy="495" r="2.5"/>
    <circle cx="450" cy="520" r="2.5"/><circle cx="425" cy="535" r="2.5"/>
    <circle cx="395" cy="540" r="2.5"/><circle cx="365" cy="535" r="2.5"/>
    <circle cx="340" cy="520" r="2.5"/><circle cx="330" cy="495" r="2.5"/>
    <circle cx="325" cy="470" r="2.5"/><circle cx="330" cy="445" r="2.5"/>
    <!-- Outer ring -->
    <circle cx="310" cy="410" r="2"/><circle cx="340" cy="390" r="2"/>
    <circle cx="370" cy="380" r="2"/><circle cx="400" cy="378" r="2"/>
    <circle cx="430" cy="380" r="2"/><circle cx="460" cy="390" r="2"/>
    <circle cx="480" cy="410" r="2"/><circle cx="490" cy="440" r="2"/>
    <circle cx="492" cy="470" r="2"/><circle cx="490" cy="500" r="2"/>
    <circle cx="480" cy="530" r="2"/><circle cx="460" cy="550" r="2"/>
    <circle cx="430" cy="560" r="2"/><circle cx="400" cy="562" r="2"/>
    <circle cx="370" cy="560" r="2"/><circle cx="340" cy="550" r="2"/>
    <circle cx="310" cy="530" r="2"/><circle cx="300" cy="500" r="2"/>
    <circle cx="298" cy="470" r="2"/><circle cx="300" cy="440" r="2"/>
  </g>

  <!-- Drum center cross / lifter bars -->
  <rect x="395" y="410" width="10" height="120" rx="2" fill="#2a2a2a" opacity="0.4"/>
  <rect x="340" y="465" width="120" height="10" rx="2" fill="#2a2a2a" opacity="0.4"/>

  <!-- Clothes hint - colored blobs visible through glass (more visible) -->
  <ellipse cx="365" cy="495" rx="40" ry="22" fill="#cc3333" fill-opacity="0.35" transform="rotate(-15 365 495)"/>
  <ellipse cx="425" cy="445" rx="30" ry="35" fill="#3344cc" fill-opacity="0.3" transform="rotate(20 425 445)"/>
  <ellipse cx="380" cy="455" rx="22" ry="18" fill="#ffffff" fill-opacity="0.25" transform="rotate(-5 380 455)"/>
  <ellipse cx="420" cy="505" rx="25" ry="14" fill="#33aa44" fill-opacity="0.28" transform="rotate(10 420 505)"/>
  <ellipse cx="350" cy="465" rx="18" ry="25" fill="#ddaa22" fill-opacity="0.2" transform="rotate(-30 350 465)"/>

  <!-- Water tint at bottom of drum -->
  <circle cx="400" cy="470" r="138" fill="url(#waterGrad)"/>

  <!-- Foam/suds hints at water line -->
  <ellipse cx="360" cy="530" rx="30" ry="6" fill="#ffffff" fill-opacity="0.12"/>
  <ellipse cx="410" cy="535" rx="20" ry="4" fill="#ffffff" fill-opacity="0.1"/>
  <ellipse cx="440" cy="528" rx="15" ry="5" fill="#ffffff" fill-opacity="0.08"/>
</g>

<!-- Rubber door seal (dark ring over chrome) -->
<circle cx="400" cy="470" r="163" fill="none" stroke="#333" stroke-width="6" stroke-opacity="0.5"/>

<!-- Door hinge hints (left side) -->
<circle cx="230" cy="440" r="4" fill="#bbb" stroke="#999" stroke-width="0.5"/>
<circle cx="230" cy="500" r="4" fill="#bbb" stroke="#999" stroke-width="0.5"/>

<!-- Brand logo area -->
<text x="400" y="218" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="bold" fill="#999" letter-spacing="4">VIBED</text>
'''
    return _insert_before_close(svg, detail_elements)


def _apply_polish(svg: str) -> str:
    """Pass 5: Final micro-details - edge bevels, ambient occlusion, glass inner shadow."""
    polish_elements = '''
<!-- Edge bevels on body -->
<rect x="150" y="698" width="500" height="2" rx="1" fill="#000" fill-opacity="0.1"/>
<rect x="648" y="120" width="2" height="580" fill="#000" fill-opacity="0.05"/>

<!-- Bottom body edge -->
<rect x="152" y="696" width="496" height="2" rx="1" fill="#bbb"/>

<!-- Ambient occlusion in door corners -->
<circle cx="400" cy="470" r="155" fill="none" stroke="#000" stroke-width="2" stroke-opacity="0.08"/>

<!-- Glass inner shadow ring (darker edge) -->
<circle cx="400" cy="470" r="150" fill="none" stroke="#000" stroke-width="8" stroke-opacity="0.06"/>
<circle cx="400" cy="470" r="145" fill="none" stroke="#000" stroke-width="4" stroke-opacity="0.04"/>

<!-- Secondary glass reflection (bottom) -->
<path d="M 340 530 Q 380 545, 440 535 Q 460 530, 470 520" fill="none" stroke="#ffffff" stroke-width="3" stroke-opacity="0.08" stroke-linecap="round"/>

<!-- Subtle panel screws -->
<circle cx="160" cy="130" r="2" fill="#ccc" stroke="#bbb" stroke-width="0.3"/>
<circle cx="640" cy="130" r="2" fill="#ccc" stroke="#bbb" stroke-width="0.3"/>
<circle cx="160" cy="220" r="2" fill="#ccc" stroke="#bbb" stroke-width="0.3"/>
<circle cx="640" cy="220" r="2" fill="#ccc" stroke="#bbb" stroke-width="0.3"/>

<!-- Wall-floor junction shadow -->
<rect x="0" y="718" width="800" height="4" fill="#000" fill-opacity="0.05"/>

<!-- Machine-floor contact shadow -->
<rect x="170" y="708" width="460" height="3" fill="#000" fill-opacity="0.12" rx="1"/>

<!-- Very subtle wall texture hints -->
<line x1="50" y1="0" x2="50" y2="720" stroke="#000" stroke-opacity="0.015" stroke-width="1"/>
<line x1="200" y1="0" x2="200" y2="720" stroke="#000" stroke-opacity="0.01" stroke-width="1"/>
<line x1="600" y1="0" x2="600" y2="720" stroke="#000" stroke-opacity="0.01" stroke-width="1"/>
<line x1="750" y1="0" x2="750" y2="720" stroke="#000" stroke-opacity="0.015" stroke-width="1"/>
'''
    return _insert_before_close(svg, polish_elements)
