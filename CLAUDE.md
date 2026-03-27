# CLAUDE.md

## Language

All code in this repo should be Python, unless otherwise specified.

## Structure

Each subfolder contains a `PROMPT.md` with instructions on what to code in that folder.

## Workflow

1. Split the application into a few modules. 
2. For each modules define the features the module exposes
3. Define a clear interface between the modules and create stub code for all modules
4. Attend to each module separately. Write unittests before implementing the features. Make sure the unittests fail before implementing.
5. Start implementing each module, verify that they work.
6. Combine the modules into an application. Test the application thoroughly.
7. If anything fails unexpectedly, first coved it in a new unittest. Verify that the test fails, then update the code. Verify again.

## Documentation

When work on a subfolder is completed:

1. **Screenshot**: Generate a `screenshot.png` in the project subfolder by writing a Python script (`screenshot.py`) that uses Pillow. The screenshot must be a faithful reproduction of what the user actually sees when running the application — replicate the exact same rendering logic (characters, colors, layout) used by the real renderer. For terminal apps, build the same text buffer the renderer produces and draw it character-by-character in a monospace font on a black background. Do not stylize, embellish, or use graphical elements that aren't in the actual output. Set up a realistic mid-action demo state programmatically — don't rely on a live terminal.

2. **Project README**: Create a `README.md` in the subfolder summarizing the work done. Include the screenshot (`![Screenshot](screenshot.png)`), your model name and version number (e.g. Claude Opus 4.6, `claude-opus-4-6`), and take credit for the implementation.

3. **Main README**: Add a subsection for the project under the `## Projects` heading in the root `README.md`. Include a brief description and the screenshot (`![Project Name](subfolder/screenshot.png)`).
