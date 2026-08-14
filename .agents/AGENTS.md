# Local Notes for GameBoyWorlds

## Debug Mode
You MUST ALWAYS ensure `debug_mode: true` is set in `configs/project_vars.yaml` before running a game in dev mode to test or capture screens. If `debug_mode` is false, the emulator will instantly crash on boot because it strictly verifies that all targets defined in `parsers.py` have matching `.npy` files on disk!

## `c` Command Bug
CRITICAL WARNING: When using the `c` command to capture a bounding box (e.g., `c car_area,next_to_car`), do NOT put a space after the comma! The command must be exactly one continuous string. If you add a space, a bug in the terminal parser will ignore your input and accidentally save a screenshot of whatever bounding box you used previously!

## Defining New Regions
When adding a new region to `REGIONS` in `parsers.py` that needs to be captured, ALWAYS add it to `MULTI_TARGETS` immediately. This ensures the `c <region>,<target>` command works properly without hitting the parser bug.

## Do Not Cheat Debug Mode
Do it properly the first time. NEVER try to turn on `debug_mode: true` to bypass missing capture file errors or create dummy `.npy` files to "cheat". Always ensure proper setup.

## Do Not Modify Core Logic
NEVER make changes to the core logic (e.g., `tracker.py`, `emulator.py`, etc.). Always use the existing framework as is. If you suspect a bug in the core framework, read the code thoroughly before making assumptions, but ultimately DO NOT modify the core logic unless explicitly instructed to do so. Work within the constraints of the existing system.
