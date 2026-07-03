# Local Notes for GameBoyWorlds

## Debug Mode
You MUST ALWAYS ensure `debug_mode: true` is set in `configs/project_vars.yaml` before running a game in dev mode to test or capture screens. If `debug_mode` is false, the emulator will instantly crash on boot because it strictly verifies that all targets defined in `parsers.py` have matching `.npy` files on disk!

## `c` Command Bug
CRITICAL WARNING: When using the `c` command to capture a bounding box (e.g., `c car_area,next_to_car`), do NOT put a space after the comma! The command must be exactly one continuous string. If you add a space, a bug in the terminal parser will ignore your input and accidentally save a screenshot of whatever bounding box you used previously!
