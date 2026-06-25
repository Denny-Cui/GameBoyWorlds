# Guide: Implementing New Tasks for GameBoyWorlds (Harry Potter Example)

This guide provides a mechanical, step-by-step walkthrough for adding a new evaluation task to the GameBoyWorlds framework, capturing the necessary screen states, wiring up the trackers, and pushing your dataset to Hugging Face.

**Role Legend:**
- 🧑 **(Human)**: Requires manual effort from you (playing the game, visual verification).
- 🤖 **(LLM)**: An LLM can easily write or autofill this code for you if you provide it the names.

---

## Step 1: Create an Initial Save State
You need a starting state from which the agent will attempt to solve the task.

1. 🧑 **(Human) Run the Emulator in Dev Mode:**
   ```bash
   python dev/dev_play.py --game harry_potter_chamber_of_secrets
   ```
   *(Note: Ensure `gameboy_dev_play_stop` is set to `false` in `configs/gameboy_vars.yaml` before running this)*

2. 🧑 **(Human) Play to the Start Point:** 
   Play the game normally until you reach the exact moment you want the agent's task to begin.

3. 🧑 **(Human) Trigger Save Breakpoint:**
   Leave the game running. Open `configs/gameboy_vars.yaml` and change `gameboy_dev_play_stop: false` to `true`. Save the YAML file.
   *Pitfall:* You must keep the emulator running while you edit the file. The game will automatically pause and prompt the terminal.

4. 🧑 **(Human) Save the State:**
   In your terminal prompt, type:
   ```bash
   s burrow_start
   ```
   *(Replace `burrow_start` with your desired initial state name).*

   **Where are these states saved?**
   Once saved, the `.state` files are physically stored in your storage directory under the specific game's ROM data path. For example, Harry Potter states are located at:
   `storage/rom_data/harry_potter/harry_potter_chamber_of_secrets/states/`
   
   *Tip:* You can quickly view a list of all your currently saved states (and export them to a CSV) by running:
   ```bash
   python dev/list_states.py --game harry_potter_chamber_of_secrets
   ```

---

## Step 2: Configure the Parser and Capture Target Regions
To detect when the task is "completed" (e.g., standing next to the car), you must define a screen bounding box and capture a reference image of what success looks like.

*(Newcomer Tip: To figure out the exact `x, y, width, height` coordinates for your new bounding box, you can type `d` in the dev play terminal prompt to open a full-screen image viewer. Hovering your mouse over the image will show the exact pixel coordinates!)*

1. 🤖 **(LLM) Define Bounding Box:**
   Open `src/gameboy_worlds/emulation/harry_potter/parsers.py`. Locate `HarryPotterChamberOfSecretsParser` (or similar subclass). Add your region to `MULTI_TARGET_REGIONS` and the target name to `MULTI_TARGETS`:
   ```python
   MULTI_TARGET_REGIONS = [
       # ... existing regions
       ("car_area", 80, 65, 55, 70), # Format: (name, x, y, width, height)
   ]
   
   MULTI_TARGETS = {
       # ... existing targets
       "car_area": ["next_to_car"],
   }
   ```

2. 🧑 **(Human) Play to the "Success" Screen:**
   *(Pitfall: Ensure you have changed `gameboy_dev_play_stop` back to `false` in `configs/gameboy_vars.yaml` first, otherwise the emulator will instantly freeze!)*
   Load back into your new state:
   ```bash
   python dev/dev_play.py --game harry_potter_chamber_of_secrets --init_state burrow_start
   ```
   Play until you reach the exact screen representing task success.

3. 🧑 **(Human) Capture the Reference Image:**
   Change `gameboy_dev_play_stop` to `true` in your configs again. When the terminal prompts you, capture the specific target using the multi-target syntax:
   ```bash
   c car_area,next_to_car
   ```
   *(Note: The `c` command references the region name defined in your parser, followed by a comma, followed by the specific target name. This saves it to a `.npy` file. Verify the image pop-up looks correct before closing it).*

---

## Step 3: Define the Termination Metric
Metrics define the logic for ending an episode. 

1. 🤖 **(LLM) Create the Metric Class:**
   Open `src/gameboy_worlds/emulation/harry_potter/test_metrics.py` and append:
   ```python
   from gameboy_worlds.emulation.tracker import RegionMatchTerminationOnlyMetric
   
   class NavigateToCarTerminateMetric(RegionMatchTerminationOnlyMetric):
       REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
       _TERMINATION_NAMED_REGION = "car_area"
       _TERMINATION_TARGET_NAME = "next_to_car"
   ```
   *Caveat:* If your termination logic requires checking multiple possible targets or regions, you'll need to use `MULTI_TARGET_REGIONS` (in your parser) or create custom logic. 
   - **`MULTI_TARGET_REGIONS` / `MULTI_TARGETS`:** Use this when checking the *exact same bounding box coordinate* on the screen, but the image inside could be one of several possibilities (e.g., "standing left of car" vs "standing right of car").
   - **Multiple Distinct Regions:** If success means checking entirely different bounding boxes (e.g. matching `car_area` OR matching `truck_area`), you will need to implement custom termination logic using multiple `named_region_matches_target` checks.

---

## Step 3.5: Define Subgoals (Highly Recommended)
Generally, we want to create tests that have at least 1 subgoal to track partial progress and provide intermediate rewards.

1. 🤖 **(LLM) Create the Subgoal Class:**
   In `src/gameboy_worlds/emulation/harry_potter/test_metrics.py`, define a subgoal.
   - For a single region check (using REGIONS), subclass `SingleRegionMatchSubGoal`.
   - For a single region check that uses MULTI_TARGET_REGIONS, subclass `RegionMatchSubGoal` and provide both `_NAMED_REGION` and `_TARGET_NAME`.
   - For checking if *any* region in a list matches, subclass `AnyRegionMatchSubGoal` (this relies on `MULTI_TARGET_REGIONS` and takes lists for `_NAMED_REGIONS` and `_TARGET_NAMES`).
   
   Example using `AnyRegionMatchSubGoal` (since we used MULTI_TARGET_REGIONS in Step 2):
   ```python
   from gameboy_worlds.emulation.tracker import AnyRegionMatchSubGoal, make_subgoal_metric_class
   
   class ReachGarageSubGoal(AnyRegionMatchSubGoal):
       NAME = "reach_garage"
       _NAMED_REGIONS = ["car_area"]
       _TARGET_NAMES = ["next_to_car"]
       
   # Bundle your subgoals together:
   NavigateToCarSubGoalMetric = make_subgoal_metric_class([ReachGarageSubGoal])
   ```

---

## Step 4: Define the Tracker
Trackers bundle the termination metrics and subgoal metrics so the environment can track progress.

1. 🤖 **(LLM) Create the Tracker Class:**
   Open `src/gameboy_worlds/emulation/harry_potter/trackers.py`. 
   Import your metrics at the top, then append:
   ```python
   from .test_metrics import NavigateToCarTerminateMetric, NavigateToCarSubGoalMetric
   
   class NavigateToCarTestTracker(HarryPotterTestTracker):
       TERMINATION_TRUNCATION_METRIC = NavigateToCarTerminateMetric
       SUBGOAL_METRIC = NavigateToCarSubGoalMetric 
   ```

---

## Step 5: Register the Tracker
The system needs to know your tracker exists.

1. 🤖 **(LLM) Update the Registry:**
   Open `src/gameboy_worlds/emulation/harry_potter/registry.py` (not the global registry). 
   First, add the import at the top of the file with the others:
   ```python
   from .trackers import NavigateToCarTestTracker
   ```
   Then, locate the `AVAILABLE_STATE_TRACKERS` dictionary and add your tracker inside the specific game's dictionary block:
   ```python
   "navigate_to_car_test": NavigateToCarTestTracker,
   ```

---

## Step 6: Add Task to the Benchmark Database
Your task must be documented in the CSV so the evaluation framework can iterate over it.

1. 🤖 **(LLM) Update the CSV:**
   Open `benchmark/tests/harry_potter.csv`. Add a new line for your task matching the exact schema:
   ```csv
   harry_potter_chamber_of_secrets,navigation,navigate to the white car,burrow_start,navigate_to_car_test,harry_potter_philosophers_stone,True
   ```
   *(Schema: game, task_category, task_description, init_state, state_tracker_class, shifted_training_games, can_train_from_init_state)*

---

## Step 7: Test Your Implementation (Crucial)
Before committing and pushing data, verify that your new metrics actually work and detect the goal when you reach it.

1. 🧑 **(Human) Run the Dev Play Script with your Tracker:**
   *(Pitfall: Remember to set `gameboy_dev_play_stop` back to `false` again!)*
   ```bash
   python dev/dev_play.py --game harry_potter_chamber_of_secrets --init_state burrow_start --state_tracker_class navigate_to_car_test
   ```
2. 🧑 **(Human) Play to the Goal:**
   Play the game normally until you reach the success condition (e.g., the car).
   - If your setup is correct, **the game window will automatically close/terminate** the exact moment the goal screen is reached.
   - If you walk past the goal and the game doesn't stop, your bounding box coordinates or `.npy` target match failed and need to be recaptured.

---

## Step 8: Push Data to Hugging Face & Pull Request
Because you generated local binaries (the `.state` file and the `.npy` screen capture array), you must push them to a remote database so others don't crash when running your task.

*(Newcomer Pitfall: You likely do not have write access to the central `DJ-Research` Hugging Face namespace or the main GameBoyWorlds github repository. You will need to use your own fork!)*

1. 🤖 **(LLM / Human) Run the Setup Script:**
   If you are an external contributor, you must first open `src/gameboy_worlds/setup_data.py` and change the `repo_namespace` variable (around line 26) from `"DJ-Research"` to your own Hugging Face username!
   Then, authenticate your Hugging Face CLI (`huggingface-cli login`) and execute the data push pipeline:
   ```bash
   python -m gameboy_worlds.setup_data push --game harry_potter_chamber_of_secrets
   ```

2. 🤖 **(LLM / Human) Standard Git Workflow (Fork):**
   Commit your python file changes. Since you cannot push directly to `origin`, make sure you have forked the repository on GitHub, added your fork as a remote, and push to your fork instead!
   ```bash
   git checkout -b add-hp-car-task
   git add .
   git commit -m "Add navigate to white car task for HP CoS"
   # Push to YOUR fork, not origin (e.g., git push <your-fork-remote> add-hp-car-task)
   git push my-fork add-hp-car-task
   ```
   Go to GitHub and open a Pull Request from your fork to the main repository. Be sure to link your Hugging Face dataset in the PR description so the maintainers can pull your binary files!
