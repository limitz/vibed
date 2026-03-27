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

When work on a subfolder is completed, create a `README.md` in that subfolder summarizing the work done. Include your model name and version number (e.g. Claude Opus 4.6, `claude-opus-4-6`) and take credit for the implementation.
