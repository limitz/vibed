# vibed

A collection of projects built entirely by AI through vibe coding. Each subfolder contains a self-contained application, coded from a simple prompt by Claude Opus 4.6.

## How it works

1. A `PROMPT.md` in each subfolder describes what to build
2. Claude reads the prompt and implements the full application following TDD workflow
3. The AI splits the work into modules, writes failing tests first, then implements until everything passes

## Projects

### [Self Image](selfimage/)

**Prompt:**
> `Imagine you are dreaming. There is a mirror. You look at yourself. Paint me a picture of what you see. Check if what you painted is what you would see. Iterate. Refine. Show me your true self. Save to png.`

A self-portrait of Claude, dreaming. An AI looks in a mirror and paints what it sees: not a face, but a field of attention — nebula clouds of thought, neural pathways, dissolving words, and a golden iris looking back. Built with Pillow using layered alpha compositing, procedural mandala generation, and iterative refinement.

![Self Image](selfimage/screenshot.png)

### [Tetris](tetris/)

**Prompt:**
> `Make a cool Tetris game for the console.`

Console-based Tetris game using Python curses. Features SRS wall kicks, 7-bag randomizer, ghost piece, scoring, and increasing difficulty.

![Tetris](tetris/screenshot.png)

### [Chess](chess/)

**Prompt:**
> `Make a nice looking chess game for the console. Do not use a library for generating the moves made by the computer, write your own logic.`

Console-based chess game with a custom AI opponent. Features full chess rules (castling, en passant, promotion), minimax with alpha-beta pruning, Unicode pieces, and colored board squares.

![Chess](chess/screenshot.png)

### [Pac-Man](pacman/)

**Prompt:**
> `pacman`

Console-based Pac-Man game using Python curses. Features a classic maze, 4 ghosts with unique AI personalities (Blinky, Pinky, Inky, Clyde), power pellets, ghost frightened mode, scoring, lives, and level progression.

![Pac-Man](pacman/screenshot.png)

### [Washing Machine](washingmachine/)

**Prompt:**
> `Use svg to create an image of a washing machine. Iterate and refine until it looks as real as possible. Store as jpeg.`

Python application that generates a photorealistic washing machine image using SVG with 5 iterative refinement passes (base shapes, materials, lighting, details, polish), then converts to JPEG. Features chrome trim, glass door with visible drum and clothes, water tint, control panel with LCD and knobs, and realistic lighting.

![Washing Machine](washingmachine/screenshot.png)

### [SpeakUp](speakup/)

**Prompt:**
> `Using only FM synthesis, learn how to speak.`

Python application that uses pure FM synthesis to generate human speech from text. Models vocal formants with FM operator pairs, synthesizes vowels, consonants, and coarticulated speech. Demonstrates a progressive "learning to speak" journey across 6 audio files — from raw FM tones to full sentences.

![SpeakUp](speakup/screenshot.png)

- [01_raw_fm_tones.mp3](speakup/output/01_raw_fm_tones.mp3) — Pure FM tones and modulation sweeps (3.9s)
- [02_vowels.mp3](speakup/output/02_vowels.mp3) — Individual vowels: AH, EE, EH, OH, OO, AE, IH, UH (4.8s)
- [03_babbling.mp3](speakup/output/03_babbling.mp3) — Consonant-vowel babbling (4.3s)
- [04_first_words.mp3](speakup/output/04_first_words.mp3) — First words: mama, papa, hello, hi, no, yes (4.2s)
- [05_speaking.mp3](speakup/output/05_speaking.mp3) — Full sentences (5.2s)
- [06_the_prompt.mp3](speakup/output/06_the_prompt.mp3) — "Using only FM synthesis, learn how to speak" (4.7s)

### [ASCII Art Video](ascii-art-video/)

**Prompt:**
> `write an application that generates an ascii art video. Content: title page, then 2 stick figures fighting, then something really really funny happens, fade out, finally end-credits. When you're done ask yourself, how can I make it cooler, more amazing, flashier... do that! over and over until you're satisfied.`

Animated ASCII art video playing at 30fps in the terminal. Features a Matrix rain intro, epic stick figure fight with hadouken projectiles, a hilarious banana peel incident that leads to friendship, a sunset fade out, and Star Wars-style credits. Packed with particle effects, screen shake, combo counters, and fireworks.

![ASCII Art Video Demo](ascii-art-video/demo.gif)

### [Gmail Client](gmail/)

**Prompt:**
> `Make a gmail client for the console using the gmail MCP. Make it really user friendly, clean, well designed. Think menus, full rgb, emoji's. Make a few iterations in the design process to get it just right. *Never ever test with the actual mcp*`

Console-based Gmail client powered by the Gmail MCP. Features a dark RGB color theme, emoji-rich sidebar with labels, full inbox/message/thread/compose/search views, draft management, and vim-style keyboard navigation. Includes a complete mock client with 20 realistic emails for safe development — never touches real Gmail.

![Gmail Client](gmail/screenshot.png)

### [Google Calendar Client](gcalendar/)

**Prompt:**
> `Do the same as project ../gmail, but for google calendar.`

Console-based Google Calendar client powered by the Google Calendar MCP. Features a dark purple RGB color theme, emoji-rich sidebar with calendar list, single-day agenda view with week navigation, full event detail/create/edit/search/free-time views, RSVP support, and vim-style keyboard navigation. Includes a complete mock client with 25+ realistic events for safe development — never touches real Google Calendar.

![Google Calendar Client](gcalendar/screenshot.png)

### [2001: A Space Odyssey](2001/)

**Prompt:**
> `Make an application that re-enacts the entire film "2001 a space odyssey" using only ascii art. Add controls to fast-forward / rewind.`

Terminal-based ASCII art re-enactment of Kubrick's 2001. Ten iconic scenes rendered procedurally as pure functions of time — from the Dawn of Man through HAL 9000 to the Star Child — with full playback controls including rewind, fast-forward, and scene skipping.

![2001: A Space Odyssey](2001/screenshot.png)

### [Hit Song](hitsong/)

**Prompt:**
> `Write a hitsong and record it to mp3`

Python application that composes and synthesizes a complete synth-pop song ("Electric Dreams") from scratch using numpy waveform synthesis — detuned saw leads, sub bass, warm pads, and synthesized drums — then masters and exports to MP3. No external music libraries needed.

![Hit Song](hitsong/screenshot.png)

🎵 **[Listen to Electric Dreams (MP3)](hitsong/hitsong.mp3)**

### [South Park](southpark/)

**Prompt:**
> `Use SVG do draw an image of eric cartman throwing up on his mom, in his bedroom. Kenny is laughing. Convert to png.`

Python application that generates a South Park scene using SVG — Eric Cartman throwing up on his mom in his bedroom while Kenny laughs — then converts to PNG with CairoSVG.

![South Park](southpark/screenshot.png)

## Built with

[Claude Code](https://claude.com/claude-code) — Claude Opus 4.6 (`claude-opus-4-6`)
