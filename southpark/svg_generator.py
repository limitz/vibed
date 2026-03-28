"""SVG generator module for South Park scene.

Generates an SVG image of Eric Cartman throwing up on his mom
in his bedroom, with Kenny laughing.

Style: South Park construction-paper cutout aesthetic — flat colors,
thick black outlines, huge heads, tiny limbs, simple shapes.
Eyes touching/overlapping in the middle is the signature look.
"""


def generate_bedroom_background() -> str:
    """Generate SVG elements for Cartman's bedroom."""
    return """
    <!-- Back wall -->
    <rect x="0" y="0" width="800" height="430" fill="#7B6B9E"/>

    <!-- Floor -->
    <rect x="0" y="430" width="800" height="170" fill="#9B7F57"/>
    <!-- Floor board lines -->
    <line x1="0" y1="470" x2="800" y2="470" stroke="#8A6E46" stroke-width="1"/>
    <line x1="0" y1="510" x2="800" y2="510" stroke="#8A6E46" stroke-width="1"/>
    <line x1="0" y1="550" x2="800" y2="550" stroke="#8A6E46" stroke-width="1"/>
    <line x1="100" y1="430" x2="100" y2="470" stroke="#8A6E46" stroke-width="0.5"/>
    <line x1="300" y1="430" x2="300" y2="470" stroke="#8A6E46" stroke-width="0.5"/>
    <line x1="500" y1="430" x2="500" y2="470" stroke="#8A6E46" stroke-width="0.5"/>
    <line x1="700" y1="430" x2="700" y2="470" stroke="#8A6E46" stroke-width="0.5"/>
    <line x1="200" y1="470" x2="200" y2="510" stroke="#8A6E46" stroke-width="0.5"/>
    <line x1="400" y1="470" x2="400" y2="510" stroke="#8A6E46" stroke-width="0.5"/>
    <line x1="600" y1="470" x2="600" y2="510" stroke="#8A6E46" stroke-width="0.5"/>

    <!-- Baseboard -->
    <rect x="0" y="420" width="800" height="14" fill="#5C4A2E" stroke="#4A3820" stroke-width="1"/>

    <!-- Window -->
    <rect x="30" y="60" width="160" height="210" fill="#1A1A3A" stroke="#5C4A2E" stroke-width="12"/>
    <line x1="110" y1="60" x2="110" y2="270" stroke="#5C4A2E" stroke-width="6"/>
    <line x1="30" y1="165" x2="190" y2="165" stroke="#5C4A2E" stroke-width="6"/>
    <!-- Crescent moon -->
    <circle cx="80" cy="115" r="24" fill="#FFFFCC" opacity="0.9"/>
    <circle cx="90" cy="108" r="20" fill="#1A1A3A"/>
    <!-- Stars -->
    <circle cx="155" cy="100" r="2" fill="#FFFFDD"/>
    <circle cx="60" cy="215" r="2" fill="#FFFFDD"/>
    <circle cx="170" cy="140" r="1.5" fill="#FFFFDD"/>

    <!-- Curtains -->
    <path d="M22,55 L22,275 Q35,270 28,200 Q22,140 35,100 Q42,70 22,55 Z" fill="#8B4040" stroke="#222" stroke-width="1.5" opacity="0.85"/>
    <path d="M198,55 L198,275 Q185,270 192,200 Q198,140 185,100 Q178,70 198,55 Z" fill="#8B4040" stroke="#222" stroke-width="1.5" opacity="0.85"/>

    <!-- Terrance & Phillip poster -->
    <rect x="500" y="55" width="95" height="125" fill="#E8D44D" stroke="#222" stroke-width="3" rx="2"/>
    <text x="547" y="78" text-anchor="middle" font-size="8" font-family="Arial" fill="#222" font-weight="bold">TERRANCE</text>
    <text x="547" y="89" text-anchor="middle" font-size="8" font-family="Arial" fill="#222" font-weight="bold">&amp;</text>
    <text x="547" y="100" text-anchor="middle" font-size="8" font-family="Arial" fill="#222" font-weight="bold">PHILLIP</text>
    <!-- T&P faces -->
    <circle cx="532" cy="125" r="11" fill="#FDD9A0" stroke="#222" stroke-width="1.5"/>
    <circle cx="562" cy="125" r="11" fill="#FDD9A0" stroke="#222" stroke-width="1.5"/>
    <circle cx="529" cy="123" r="3" fill="#FFF" stroke="#222" stroke-width="0.5"/>
    <circle cx="535" cy="123" r="3" fill="#FFF" stroke="#222" stroke-width="0.5"/>
    <circle cx="559" cy="123" r="3" fill="#FFF" stroke="#222" stroke-width="0.5"/>
    <circle cx="565" cy="123" r="3" fill="#FFF" stroke="#222" stroke-width="0.5"/>
    <circle cx="530" cy="124" r="1.5" fill="#222"/>
    <circle cx="534" cy="124" r="1.5" fill="#222"/>
    <circle cx="560" cy="124" r="1.5" fill="#222"/>
    <circle cx="564" cy="124" r="1.5" fill="#222"/>
    <line x1="532" y1="136" x2="532" y2="162" stroke="#222" stroke-width="2"/>
    <line x1="562" y1="136" x2="562" y2="162" stroke="#222" stroke-width="2"/>

    <!-- Bed -->
    <rect x="5" y="320" width="210" height="110" fill="#3366CC" stroke="#222" stroke-width="3" rx="3"/>
    <rect x="5" y="290" width="210" height="35" fill="#2255AA" stroke="#222" stroke-width="3" rx="3"/>
    <rect x="15" y="295" width="190" height="4" fill="#1A44AA" rx="2"/>
    <!-- Pillow -->
    <ellipse cx="55" cy="340" rx="40" ry="18" fill="#FFFFFF" stroke="#CCC" stroke-width="2"/>
    <path d="M55,325 L55,355" fill="none" stroke="#EEE" stroke-width="1"/>
    <!-- Blanket fold -->
    <path d="M8,365 Q110,355 213,365" fill="none" stroke="#2244AA" stroke-width="2"/>
    <!-- Clyde Frog -->
    <ellipse cx="168" cy="345" rx="18" ry="12" fill="#44AA44" stroke="#222" stroke-width="2"/>
    <circle cx="161" cy="337" r="4.5" fill="#FFFFFF" stroke="#222" stroke-width="1"/>
    <circle cx="175" cy="337" r="4.5" fill="#FFFFFF" stroke="#222" stroke-width="1"/>
    <circle cx="161" cy="338" r="2.5" fill="#000"/>
    <circle cx="175" cy="338" r="2.5" fill="#000"/>
    <path d="M164,348 Q168,352 172,348" fill="none" stroke="#228822" stroke-width="1.5"/>

    <!-- Nightstand -->
    <rect x="225" y="345" width="55" height="85" fill="#5C4A2E" stroke="#222" stroke-width="2.5"/>
    <rect x="232" y="370" width="41" height="2" fill="#4A3820"/>
    <circle cx="252" cy="385" r="3" fill="#DAA520" stroke="#222" stroke-width="1"/>
    <!-- Lamp -->
    <rect x="244" y="318" width="16" height="27" fill="#8B7355" stroke="#222" stroke-width="2"/>
    <polygon points="228,318 272,318 280,295 220,295" fill="#FFDD44" stroke="#222" stroke-width="2"/>

    <!-- Toys on floor -->
    <circle cx="670" cy="562" r="10" fill="#FF4444" stroke="#222" stroke-width="1.5"/>
    <circle cx="695" cy="568" r="7" fill="#44CC44" stroke="#222" stroke-width="1.5"/>
    """


def generate_cartman() -> str:
    """Generate SVG elements for Eric Cartman throwing up.

    South Park style: huge round head, eyes touching in middle,
    very fat body, cyan/teal hat with yellow band and pom-pom.
    Feet planted at floor level y=430.
    """
    return """
    <g transform="translate(360, 235)">
      <!-- Shadow -->
      <ellipse cx="5" cy="198" rx="55" ry="10" fill="#000" opacity="0.15"/>

      <!-- BODY - very fat, red jacket -->
      <ellipse cx="0" cy="120" rx="58" ry="52" fill="#D01010" stroke="#222" stroke-width="3"/>
      <!-- Yellow zipper -->
      <line x1="0" y1="72" x2="0" y2="165" stroke="#FFD700" stroke-width="3"/>
      <!-- Buttons -->
      <circle cx="0" cy="90" r="3.5" fill="#FFD700" stroke="#222" stroke-width="1"/>
      <circle cx="0" cy="110" r="3.5" fill="#FFD700" stroke="#222" stroke-width="1"/>
      <circle cx="0" cy="130" r="3.5" fill="#FFD700" stroke="#222" stroke-width="1"/>
      <!-- Jacket collar / neckline -->
      <path d="M-28,72 Q0,80 28,72" fill="#D01010" stroke="#222" stroke-width="2"/>

      <!-- HEAD - huge, tilted forward (vomiting) -->
      <g transform="rotate(12, 0, 10)">
        <!-- Head -->
        <circle cx="0" cy="10" r="50" fill="#FDD9A0" stroke="#222" stroke-width="3"/>

        <!-- Double chin -->
        <path d="M-28,48 Q0,62 28,48" fill="#FDD9A0" stroke="#E8C080" stroke-width="1.5"/>

        <!-- HAT - cyan beanie sitting on top half of head -->
        <path d="M-50,5 A50,50 0 0,1 50,5 L48,0 Q48,-48 0,-50 Q-48,-48 -48,0 Z" fill="#00B4D8" stroke="#222" stroke-width="3"/>
        <!-- Yellow band - thick and prominent -->
        <rect x="-50" y="-3" width="100" height="12" fill="#FFD700" stroke="#222" stroke-width="2.5"/>
        <!-- Pom-pom -->
        <circle cx="0" cy="-50" r="11" fill="#FFD700" stroke="#222" stroke-width="2.5"/>

        <!-- EYES - signature South Park: large ovals, touching/overlapping at center -->
        <ellipse cx="-13" cy="8" rx="15" ry="16" fill="#FFFFFF" stroke="#222" stroke-width="2.5"/>
        <ellipse cx="13" cy="8" rx="15" ry="16" fill="#FFFFFF" stroke="#222" stroke-width="2.5"/>
        <!-- Pupils -->
        <circle cx="-9" cy="11" r="6" fill="#222"/>
        <circle cx="17" cy="11" r="6" fill="#222"/>

        <!-- Eyebrows - distressed -->
        <line x1="-28" y1="-5" x2="-4" y2="-13" stroke="#222" stroke-width="3.5"/>
        <line x1="4" y1="-13" x2="28" y2="-5" stroke="#222" stroke-width="3.5"/>

        <!-- Nose - tiny -->
        <circle cx="0" cy="18" r="2.5" fill="#E8C080"/>

        <!-- MOUTH - wide open for vomiting -->
        <ellipse cx="2" cy="35" rx="22" ry="16" fill="#8B0000" stroke="#222" stroke-width="2.5"/>
        <!-- Throat darkness -->
        <ellipse cx="2" cy="35" rx="14" ry="9" fill="#500000"/>
        <!-- Teeth top -->
        <rect x="-14" y="22" width="7" height="6" fill="#FFF" stroke="#222" stroke-width="0.7" rx="1"/>
        <rect x="-5" y="22" width="7" height="6" fill="#FFF" stroke="#222" stroke-width="0.7" rx="1"/>
        <rect x="4" y="22" width="7" height="6" fill="#FFF" stroke="#222" stroke-width="0.7" rx="1"/>
        <!-- Teeth bottom -->
        <rect x="-10" y="44" width="6" height="5" fill="#FFF" stroke="#222" stroke-width="0.7" rx="1"/>
        <rect x="-2" y="44" width="6" height="5" fill="#FFF" stroke="#222" stroke-width="0.7" rx="1"/>
      </g>

      <!-- ARMS -->
      <!-- Left arm (holding stomach) -->
      <path d="M-52,95 L-68,115 L-42,125" fill="none" stroke="#D01010" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="-42" cy="125" r="9" fill="#FDD9A0" stroke="#222" stroke-width="2"/>
      <!-- Right arm (reaching toward mom) -->
      <path d="M52,90 L82,100 L98,92" fill="none" stroke="#D01010" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="98" cy="92" r="9" fill="#FDD9A0" stroke="#222" stroke-width="2"/>

      <!-- LEGS - short, stumpy -->
      <rect x="-28" y="163" width="22" height="26" fill="#5C4033" stroke="#222" stroke-width="2.5" rx="2"/>
      <rect x="6" y="163" width="22" height="26" fill="#5C4033" stroke="#222" stroke-width="2.5" rx="2"/>
      <!-- Shoes -->
      <ellipse cx="-17" cy="192" rx="17" ry="8" fill="#222" stroke="#111" stroke-width="2"/>
      <ellipse cx="17" cy="192" rx="17" ry="8" fill="#222" stroke="#111" stroke-width="2"/>
    </g>
    """


def generate_liane_cartman() -> str:
    """Generate SVG elements for Liane Cartman (Cartman's mom).

    South Park style: touching eyes, prominent eyelashes (female marker),
    brown fluffy hair, red dress, lipstick. Taller/slimmer than Cartman.
    """
    return """
    <g transform="translate(545, 230)">
      <!-- Shadow -->
      <ellipse cx="0" cy="203" rx="38" ry="8" fill="#000" opacity="0.15"/>

      <!-- BODY - simple A-line dress, taller than Cartman -->
      <path d="M-25,65 L-38,170 L38,170 L25,65 Z" fill="#CC3333" stroke="#222" stroke-width="3"/>
      <!-- V-neckline -->
      <path d="M-18,65 L0,80 L18,65" fill="#FDD9A0" stroke="#222" stroke-width="2"/>
      <!-- Necklace -->
      <path d="M-14,68 Q0,76 14,68" fill="none" stroke="#DAA520" stroke-width="2"/>
      <circle cx="0" cy="76" r="3.5" fill="#DAA520" stroke="#222" stroke-width="1"/>

      <!-- HEAD -->
      <circle cx="0" cy="18" r="44" fill="#FDD9A0" stroke="#222" stroke-width="3"/>

      <!-- HAIR - Liane's big brown fluffy hair -->
      <path d="M-46,14 Q-55,-25 -28,-40 Q0,-52 28,-40 Q55,-25 46,14" fill="#7B3F00" stroke="#222" stroke-width="2.5"/>
      <ellipse cx="-36" cy="12" rx="17" ry="32" fill="#7B3F00" stroke="#222" stroke-width="2"/>
      <ellipse cx="36" cy="12" rx="17" ry="32" fill="#7B3F00" stroke="#222" stroke-width="2"/>
      <!-- Hair flip on top -->
      <path d="M-22,-40 Q-12,-55 0,-46 Q12,-55 22,-40" fill="#7B3F00" stroke="#222" stroke-width="2"/>
      <!-- Hair shine -->
      <path d="M-15,-35 Q-10,-30 -5,-35" fill="none" stroke="#9B5F20" stroke-width="1.5" opacity="0.5"/>

      <!-- EYES - South Park touching style, wide with shock -->
      <ellipse cx="-12" cy="10" rx="13" ry="15" fill="#FFFFFF" stroke="#222" stroke-width="2.5"/>
      <ellipse cx="12" cy="10" rx="13" ry="15" fill="#FFFFFF" stroke="#222" stroke-width="2.5"/>
      <!-- Pupils -->
      <circle cx="-12" cy="13" r="5" fill="#222"/>
      <circle cx="12" cy="13" r="5" fill="#222"/>

      <!-- Eyelashes - 3 per eye, the female character marker -->
      <line x1="-25" y1="2" x2="-29" y2="-3" stroke="#222" stroke-width="2.5"/>
      <line x1="-21" y1="-2" x2="-24" y2="-8" stroke="#222" stroke-width="2.5"/>
      <line x1="-15" y1="-4" x2="-17" y2="-10" stroke="#222" stroke-width="2.5"/>
      <line x1="25" y1="2" x2="29" y2="-3" stroke="#222" stroke-width="2.5"/>
      <line x1="21" y1="-2" x2="24" y2="-8" stroke="#222" stroke-width="2.5"/>
      <line x1="15" y1="-4" x2="17" y2="-10" stroke="#222" stroke-width="2.5"/>

      <!-- Eyebrows -->
      <path d="M-24,-6 Q-12,-14 -3,-8" fill="none" stroke="#5C3010" stroke-width="2.5"/>
      <path d="M3,-8 Q12,-14 24,-6" fill="none" stroke="#5C3010" stroke-width="2.5"/>

      <!-- Nose -->
      <circle cx="0" cy="22" r="2.5" fill="#E8C080"/>

      <!-- MOUTH - horrified O -->
      <ellipse cx="0" cy="35" rx="12" ry="10" fill="#8B0000" stroke="#222" stroke-width="2.5"/>
      <!-- Lipstick - top lip -->
      <path d="M-14,33 Q-8,28 0,31 Q8,28 14,33" fill="#CC4466" stroke="#222" stroke-width="1"/>
      <!-- Bottom lip -->
      <path d="M-10,40 Q0,46 10,40" fill="#CC4466" stroke="#222" stroke-width="1"/>

      <!-- ARMS - raised in horror -->
      <path d="M-25,75 L-55,48 L-62,25" fill="none" stroke="#FDD9A0" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="-62" cy="25" r="8" fill="#FDD9A0" stroke="#222" stroke-width="2"/>
      <!-- Fingers spread -->
      <line x1="-62" y1="25" x2="-72" y2="17" stroke="#FDD9A0" stroke-width="4" stroke-linecap="round"/>
      <line x1="-62" y1="25" x2="-67" y2="14" stroke="#FDD9A0" stroke-width="4" stroke-linecap="round"/>
      <line x1="-62" y1="25" x2="-59" y2="14" stroke="#FDD9A0" stroke-width="4" stroke-linecap="round"/>
      <line x1="-62" y1="25" x2="-54" y2="18" stroke="#FDD9A0" stroke-width="4" stroke-linecap="round"/>

      <path d="M25,75 L55,48 L62,28" fill="none" stroke="#FDD9A0" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="62" cy="28" r="8" fill="#FDD9A0" stroke="#222" stroke-width="2"/>
      <line x1="62" y1="28" x2="72" y2="20" stroke="#FDD9A0" stroke-width="4" stroke-linecap="round"/>
      <line x1="62" y1="28" x2="67" y2="17" stroke="#FDD9A0" stroke-width="4" stroke-linecap="round"/>
      <line x1="62" y1="28" x2="59" y2="17" stroke="#FDD9A0" stroke-width="4" stroke-linecap="round"/>
      <line x1="62" y1="28" x2="54" y2="21" stroke="#FDD9A0" stroke-width="4" stroke-linecap="round"/>

      <!-- LEGS -->
      <rect x="-14" y="166" width="12" height="28" fill="#FDD9A0" stroke="#222" stroke-width="2" rx="2"/>
      <rect x="2" y="166" width="12" height="28" fill="#FDD9A0" stroke="#222" stroke-width="2" rx="2"/>
      <!-- Shoes (matching dress) -->
      <ellipse cx="-8" cy="196" rx="12" ry="6" fill="#CC3333" stroke="#222" stroke-width="2"/>
      <ellipse cx="8" cy="196" rx="12" ry="6" fill="#CC3333" stroke="#222" stroke-width="2"/>

      <!-- Vomit splatters on dress -->
      <ellipse cx="-3" cy="95" rx="22" ry="15" fill="#8BAD2A" opacity="0.85" stroke="#6B8D10" stroke-width="1.5"/>
      <ellipse cx="14" cy="115" rx="15" ry="11" fill="#9BBD3A" opacity="0.8" stroke="#6B8D10" stroke-width="1"/>
      <ellipse cx="-8" cy="135" rx="12" ry="8" fill="#7B9D1A" opacity="0.75"/>
      <circle cx="10" cy="82" r="7" fill="#ABCD4A" opacity="0.75"/>
      <!-- Drip on face -->
      <path d="M18,40 Q20,50 17,58" fill="none" stroke="#8BAD2A" stroke-width="4" stroke-linecap="round" opacity="0.75"/>
      <circle cx="17" cy="60" r="3" fill="#8BAD2A" opacity="0.7"/>
    </g>
    """


def generate_kenny() -> str:
    """Generate SVG elements for Kenny laughing.

    South Park style: completely enclosed in orange parka,
    very tight hood showing only eyes through tiny opening.
    Smaller/shorter than Cartman.
    """
    return """
    <g transform="translate(710, 300)">
      <!-- Shadow -->
      <ellipse cx="0" cy="138" rx="30" ry="6" fill="#000" opacity="0.15"/>

      <!-- BODY - orange parka -->
      <ellipse cx="0" cy="78" rx="30" ry="42" fill="#F58220" stroke="#222" stroke-width="3"/>
      <!-- Parka quilting -->
      <path d="M-28,62 Q0,57 28,62" fill="none" stroke="#D06A10" stroke-width="1.5"/>
      <path d="M-30,78 Q0,73 30,78" fill="none" stroke="#D06A10" stroke-width="1.5"/>
      <path d="M-28,94 Q0,89 28,94" fill="none" stroke="#D06A10" stroke-width="1.5"/>
      <!-- Zipper -->
      <line x1="0" y1="40" x2="0" y2="115" stroke="#DAA520" stroke-width="2"/>

      <!-- HEAD/HOOD - tight circle -->
      <circle cx="0" cy="10" r="34" fill="#F58220" stroke="#222" stroke-width="3"/>

      <!-- Hood fur/fabric trim ring -->
      <ellipse cx="0" cy="10" rx="17" ry="18" fill="none" stroke="#E0C880" stroke-width="4"/>

      <!-- Face opening - very small -->
      <ellipse cx="0" cy="10" rx="14" ry="15" fill="#FDD9A0" stroke="#222" stroke-width="2"/>

      <!-- Drawstrings -->
      <path d="M-8,24 L-13,35" fill="none" stroke="#DAA520" stroke-width="2" stroke-linecap="round"/>
      <path d="M8,24 L13,35" fill="none" stroke="#DAA520" stroke-width="2" stroke-linecap="round"/>
      <circle cx="-14" cy="36" r="2.5" fill="#DAA520" stroke="#222" stroke-width="0.5"/>
      <circle cx="14" cy="36" r="2.5" fill="#DAA520" stroke="#222" stroke-width="0.5"/>

      <!-- EYES - happy/laughing squint (upside-down U) -->
      <path d="M-8,7 Q-5,2 -2,7" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>
      <path d="M2,7 Q5,2 8,7" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>

      <!-- Blush -->
      <circle cx="-7" cy="13" r="3.5" fill="#F0A0A0" opacity="0.5"/>
      <circle cx="7" cy="13" r="3.5" fill="#F0A0A0" opacity="0.5"/>

      <!-- ARMS -->
      <!-- Left arm pointing at Cartman -->
      <path d="M-28,62 L-50,45 L-68,35" fill="none" stroke="#F58220" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
      <ellipse cx="-70" cy="33" rx="10" ry="8" fill="#F58220" stroke="#222" stroke-width="2"/>
      <!-- Right arm on belly -->
      <path d="M26,72 L36,88 L22,94" fill="none" stroke="#F58220" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
      <ellipse cx="20" cy="96" rx="10" ry="8" fill="#F58220" stroke="#222" stroke-width="2"/>

      <!-- LEGS -->
      <rect x="-14" y="113" width="12" height="22" fill="#F58220" stroke="#222" stroke-width="2" rx="2"/>
      <rect x="2" y="113" width="12" height="22" fill="#F58220" stroke="#222" stroke-width="2" rx="2"/>
      <!-- Shoes -->
      <ellipse cx="-8" cy="137" rx="11" ry="5.5" fill="#222" stroke="#111" stroke-width="2"/>
      <ellipse cx="8" cy="137" rx="11" ry="5.5" fill="#222" stroke="#111" stroke-width="2"/>

      <!-- Shaking lines (laughing hard) -->
      <line x1="-38" y1="5" x2="-42" y2="3" stroke="#222" stroke-width="1.5" opacity="0.5"/>
      <line x1="-38" y1="15" x2="-43" y2="15" stroke="#222" stroke-width="1.5" opacity="0.5"/>
      <line x1="38" y1="5" x2="42" y2="3" stroke="#222" stroke-width="1.5" opacity="0.5"/>
      <line x1="38" y1="15" x2="43" y2="15" stroke="#222" stroke-width="1.5" opacity="0.5"/>
    </g>
    """


def generate_vomit() -> str:
    """Generate SVG elements for the vomit stream from Cartman to his mom."""
    return """
    <g opacity="0.9">
      <!-- Main vomit arc -->
      <path d="M415,290 C440,295 470,310 500,325 Q520,335 540,345"
            fill="none" stroke="#8BAD2A" stroke-width="26" stroke-linecap="round"/>
      <path d="M420,285 C445,290 475,308 505,322 Q522,330 535,340"
            fill="none" stroke="#9BBD3A" stroke-width="17" stroke-linecap="round"/>
      <path d="M423,292 C448,298 475,313 502,326"
            fill="none" stroke="#ABCD4A" stroke-width="10" stroke-linecap="round"/>

      <!-- Chunks -->
      <circle cx="445" cy="305" r="6" fill="#7B9D1A" stroke="#6B8D10" stroke-width="1.5"/>
      <circle cx="475" cy="318" r="5" fill="#ABCD4A" stroke="#8BAD2A" stroke-width="1"/>
      <circle cx="502" cy="330" r="7" fill="#8BAD2A" stroke="#6B8D10" stroke-width="1.5"/>
      <rect x="458" y="310" width="8" height="8" fill="#7B9D1A" rx="2" opacity="0.8"/>
      <circle cx="490" cy="322" r="4" fill="#CBDD6A" opacity="0.8"/>

      <!-- Splatter droplets -->
      <circle cx="435" cy="320" r="5" fill="#8BAD2A"/>
      <circle cx="458" cy="338" r="4" fill="#9BBD3A"/>
      <circle cx="485" cy="348" r="6" fill="#7B9D1A"/>
      <circle cx="510" cy="352" r="3.5" fill="#ABCD4A"/>
      <circle cx="442" cy="342" r="3" fill="#8BAD2A" opacity="0.7"/>
      <circle cx="468" cy="355" r="2.5" fill="#9BBD3A" opacity="0.6"/>
      <circle cx="520" cy="342" r="4" fill="#8BAD2A" opacity="0.7"/>

      <!-- Drip drops -->
      <path d="M465,342 L463,360 L467,360 Z" fill="#8BAD2A" opacity="0.7"/>
      <path d="M492,345 L490,365 L494,365 Z" fill="#9BBD3A" opacity="0.6"/>
      <path d="M452,348 L450,362 L454,362 Z" fill="#7B9D1A" opacity="0.5"/>

      <!-- Floor puddle -->
      <ellipse cx="482" cy="432" rx="55" ry="15" fill="#8BAD2A" opacity="0.6" stroke="#6B8D10" stroke-width="1"/>
      <ellipse cx="462" cy="436" rx="30" ry="9" fill="#9BBD3A" opacity="0.5"/>
      <ellipse cx="512" cy="430" rx="22" ry="7" fill="#7B9D1A" opacity="0.4"/>
      <circle cx="445" cy="432" r="5" fill="#ABCD4A" opacity="0.35"/>
      <circle cx="520" cy="435" r="4" fill="#ABCD4A" opacity="0.3"/>
    </g>
    """


def generate_scene(width: int = 800, height: int = 600) -> str:
    """Generate the complete SVG scene.

    Returns:
        Complete SVG string.
    """
    bedroom = generate_bedroom_background()
    cartman = generate_cartman()
    liane = generate_liane_cartman()
    kenny = generate_kenny()
    vomit = generate_vomit()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <!-- Background -->
  <rect x="0" y="0" width="{width}" height="{height}" fill="#7B6B9E"/>

  {bedroom}
  {vomit}
  {liane}
  {cartman}
  {kenny}

  <!-- Speech bubble - Cartman -->
  <g transform="translate(295, 175)">
    <ellipse cx="0" cy="0" rx="55" ry="25" fill="white" stroke="#222" stroke-width="2.5"/>
    <polygon points="18,23 35,48 5,23" fill="white" stroke="#222" stroke-width="2.5"/>
    <polygon points="18,23 33,46 7,23" fill="white"/>
    <text x="0" y="7" text-anchor="middle" font-size="15" font-family="Arial Black, Arial" fill="#222" font-weight="bold">BLAARGH!</text>
  </g>

  <!-- Speech bubble - Mom -->
  <g transform="translate(605, 160)">
    <ellipse cx="0" cy="0" rx="52" ry="26" fill="white" stroke="#222" stroke-width="2.5"/>
    <polygon points="-10,24 -25,50 0,24" fill="white" stroke="#222" stroke-width="2.5"/>
    <polygon points="-10,24 -23,48 -2,24" fill="white"/>
    <text x="0" y="-3" text-anchor="middle" font-size="13" font-family="Arial Black, Arial" fill="#222" font-weight="bold">Oh no,</text>
    <text x="0" y="14" text-anchor="middle" font-size="13" font-family="Arial Black, Arial" fill="#222" font-weight="bold">Eric!</text>
  </g>

  <!-- Kenny speech bubble (muffled) -->
  <g transform="translate(710, 250)">
    <ellipse cx="0" cy="0" rx="42" ry="20" fill="white" stroke="#222" stroke-width="2"/>
    <polygon points="0,18 -10,38 10,18" fill="white" stroke="#222" stroke-width="2"/>
    <polygon points="0,18 -8,36 8,18" fill="white"/>
    <text x="0" y="6" text-anchor="middle" font-size="12" font-family="Arial Black, Arial" fill="#222" font-weight="bold">Mmph!</text>
  </g>
</svg>"""
