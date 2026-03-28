# CLAUDE.md

## Language

All code in this repo should be Python, unless otherwise specified.

## Structure

Each subfolder contains a `PROMPT.md` with instructions on what to code in that folder.

## Rules

* Never use any other application folders as reference when implementing a new application, unless explicitly mentioned.

## Workflow

1. Split the application into a few modules. 
2. For each modules define the features the module exposes
3. Define a clear interface between the modules and create stub code for all modules. 
4. Attend to each module separately. Write unittests before implementing the features. Update the code to return (invalid) dummy data, then make sure the unittests fail before implementing the actual code.
5. Start implementing each module, verify that they work.
6. Combine the modules into an application. Test the application thoroughly.
7. If anything fails unexpectedly, first coved it in a new unittest. Verify that the test fails, then update the code. Verify again.

## Documentation

When work on a subfolder is completed:

1. **Screenshot**: Generate a `screenshot.png` in the project subfolder by writing a Python script (`screenshot.py`) that uses Pillow. The screenshot must look like a photo of the running application — if someone compared the screenshot to the real app, they should be indistinguishable.

   For terminal/curses apps this means:
   - First, build the exact text buffer (a 2D grid of characters with foreground/background colors) that the renderer's `draw()` method would produce. Call the same logic or replicate it line-by-line — do NOT approximate or re-interpret the layout.
   - Then render that buffer to an image by drawing each character cell individually: monospace font, fixed-width cells, foreground color on top of a filled background rectangle, black terminal background.
   - Each cell must have the same dimensions. The result should look like a terminal emulator window, not a graphical UI.
   - Do NOT use large graphical squares, scaled-up piece icons, thick borders, drop shadows, or any visual element that doesn't exist in the terminal output. If the terminal shows 3-character-wide cells in a monospace font, the screenshot must show exactly that.
   - Set up a realistic mid-action demo state programmatically — don't rely on a live terminal.

2. **Project README**: Create a `README.md` in the subfolder summarizing the work done. Feature the text in PROMPT.md below the title, inside a codebox. Include the screenshot (`![Screenshot](screenshot.png)`), your model name and version number (e.g. Claude Opus 4.6, `claude-opus-4-6`), and take credit for the implementation.

3. **Main README**: Add a subsection for the project under the `## Projects` heading in the root `README.md`. Include the prompt text as a blockquote with inline code (e.g. `> \`prompt text\``), a brief description, and the screenshot (`![Project Name](subfolder/screenshot.png)`).
