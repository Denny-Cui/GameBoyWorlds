<div align="center">
  <picture>
    <img alt="Pokémon Environments" src="assets/logo_tilt.png" width="350px" style="max-width: 100%;">
  </picture>
  <br>
  
  **Actually Building Intelligent and General Pokémon Agents**
  
  <br>
    <a href="https://github.com/DhananjayAshok/GameBoyWorlds/blob/main/LICENSE" target="_blank" rel="noopener noreferrer"><img alt="GitHub" src="https://img.shields.io/badge/license-MIT-blue"></a>
    <a href="https://dhananjayashok.github.io/" target="_blank" rel="noopener noreferrer"><img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/docs/transformers/index.svg?down_color=red&down_message=offline&up_message=online"></a>
    <a href="https://dhananjayashok.github.io/GameBoyWorlds/" target="_blank" rel="noopener noreferrer"><img alt="GitHub" src="https://img.shields.io/badge/documentation-pdoc-red"></a>
</div>

<img src="assets/logo.png" width="70px"> is organized into 2 primary modules:
* `emulation`: Handles GameBoy emulation, parsing and state tracking
* `interface`: Implements high level actions, and Gym-compliant environments

See the [API documentation](https://dhananjayashok.github.io/GameBoyWorlds/) to understand the code base, the rest of this document goes into details on how you would implement new features or test tasks in <img src="assets/logo.png" width="70">. 

  - [Custom Starting States](#I-want-to-create-my-own-starting-states)
  - [Descriptive State and Event Tracking](#I-want-to-track-fine-grained-details)
  - [Reward Engineering](#I-want-to-engineer-my-own-reward-functions)
  - [Adding New ROMs](#I-want-to-add-a-new-ROM-Hack)
  - [Adding New Test Tasks](#i-want-to-add-a-new-test-task)
  - [Useful things](#useful-things)

### I want to create my own starting states
Easy. The only question is whether you want to save an mGBA state (perhaps you use cheats to lazily put the agent in a very specific state) or save a PyBoy state directly (i.e. you start from an existing state and play to the new state).

**From mGBA state:**

First, start with mGBA and **make sure** to match the text box frame options from the existing default states. This is vital to ensure the state parsing system works. Play till the point you want to replicate with a state and save the game (go to the start menu and save) in the state you want to restore from. This will make a `game_ROMNAME.sav` file in the same directory as the rom file. Then run:

```bash
python dev/save_state.py --game <game> --state_name <name>
```

This will save the state and allows you to load it by specifying it as a state name. 


To get to the state from PyBoy, first make sure the `gameboy_dev_play_stop` parameter is [configured](configs/gameboy_vars.yaml) to `false`. Then, run:
```bash 
python dev/dev_play.py --game <game> --init_state <optional_starting_state>
```

This will run the game with the option to enter dev mode. Play the game like you usually would, until you reach the state you want to save. Then, go to [the gameboy configs](configs/gameboy_vars.yaml) *while* playing the game (at the state you want to save), change the `gameboy_dev_play_stop` parameter to `true` (save the configs file) and then check the terminal. You will get a message with the possible dev actions. The one you're looking for is `s <name>`, which saves the state.

Regardless of how you did it, you can test that your state save worked with:
```bash
python demos/emulator --game <game> --init_state <name>
```

### I want to track fine-grained details
Maybe you want to enhance the observation space of the agent with information about the current playthrough (e.g. current map ID, enemy team level). Perhaps you want to train text-only / weak visual agents, and parse as much of the screen image as possible into numerical signals / text (e.g. your team stats, bag contents). Some might not even care about their agents, but want to have a sophisticated set of metrics that they can look at to assess goal conditions, judge the quality of a playthrough, or [craft a good reward function](#i-want-to-engineer-my-own-reward-functions). 

Whatever your motivation, <img src="assets/logo.png" width="70"> provides a powerful set of approaches for reading game states, and then allows you to aggregate over these values over time to compute useful metrics for reward assignment and evaluation. 

The first thing to do is detect an event at a moment in time. This is done in subclasses of the `StateParser` [object](src/gameboy_worlds//emulation/emulator.py) in one of two ways: 

1. **Emulator Screen Captures:** Often particular game states can be cleanly identified by a unique text popup, or some other characteristic marker on the screen. Any of these can be easily captured and checked with the existing parsing system. For example, the current implementation for Pokémon Red has screen captures set up to identify which starter the player chooses. See the [section below](#state-parser-set-up) for examples of this being done. See the [`StateParser` API documentation](https://dhananjayashok.github.io/GameBoyWorlds/gameboy_worlds/emulation/parser.html) for a quick overview on how this works.  
2. **Memory Slot Hooks:** A strong alternative is to just directly read statistics from the game's WRAM. Visually inaccessible information (e.g. the attack stats of all Pokémon on the opponents team) are often easy to obtain this way. The only catch is, this method relies on knowing which memory slots to look for. That's easy enough for games which have excellent [decompilation guides](https://github.com/pret/pokered/blob/symbols/pokered.sym), but is much harder to do for ROM hacks which may mess around with the slots arbitrarily or less popular games. See the [memory reader](src/gameboy_worlds/emulation/pokemon/parsers.py) state parser to get a sense of how you should go about this. 

These approaches allow your state parsers to give instant-wise decisions or indications when an event has occured. You can then configure your `StateTracker` to use the parser to check for this flag / read this information, and store appropriate metrics. See the existing [parsers](src/gameboy_worlds/emulation/pokemon/parsers.py) and [trackers](src/gameboy_worlds/emulation/pokemon/trackers.py) for examples. 

### I want to add a new ROM Hack or GameBoy Game
Setting up a new game is an easy process at a basic level, but can be an involved endeavour if you want to make the new environment a strong one. Please do reach out to me if you have any questions, and we can work to merge the new ROM into <img src="assets/logo.png" width="70"> together. 

#### Initial Steps:

0. Set the repo to `debug` mode by editing the [config file](configs/project_vars.yaml)
1. Create a `<game>_rom_data_path` parameter in the [configs](configs) (either as a new file or in an existing one)
2. Obtain the ROM and place it in the desired path under the ROM data folder. Remember, the `<game>_rom_data_path` folder is rooted at the `storage_dir` from the [configs](configs/private_vars.yaml). 
4. Go to the [registry](src/gameboy_worlds/emulation/registry.py) and add the ROM name to :
    - `GAME_TO_GB_NAME`: This will be the name the system expects to find in `<storage>/<game>_rom_data_path/` 
    - `_STRONGEST_PARSERS`: with `DummyParser` as the value. 
    - `AVAILABLE_STATE_TRACKERS`: give it a `default` value of `StateTracker`. 
    - `AVAILABLE_EMULATORS`: give it a `default` value of `Emulator`.
5. Run `python dev/create_first_state.py --game <game>`. This will create a default state. You will not be able to run the `Emulator` on this ROM before doing this. 
6. Run `python dev/dev_play.py --game <game>` (with the [`gameboy_dev_play_stop` parameter](configs/gameboy_vars.yaml) set to `false`) and proceed through the game until you reach a satisfactory default starting state. Then, open the [config file](configs/gameboy_vars.yaml) and set `gameboy_dev_play_stop` to `true` and save the config file. This will trigger a dev mode and ask you for a terminal input. Enter `s default` and you will set that as the new default state. Enter `s initial` as well to save it properly. 

I have provided an [example](https://drive.google.com/file/d/1fsMjkOjpbyeLLNxP3JVaj6uVXycwSAVC/view?usp=sharing) video for this process. *Note*: In the video, I set the text speed to fast. This was the wrong choice, and so I have set it to slow in all states. 

#### State Parser Set Up:
The above steps will let you play the game on the emulator, but the real power of this framework is only realized when you get involved and create a proper `StateParser`. As mentioned in the [section above](#i-want-to-track-fine-grained-details), this is done either by reading from gameboy memory states or by setting up screen captures to track events. Here, I detail the screen capture method. 

Simply put, this approach aims to capture a given region of the games frame at the right moment, hence saving what the screen "looks like" when a particular event occurs. For example, in Pokémon, the top right of the screen always has the edge of the player menu, and is hence a reliable signal as to whether or not the player is in the menu. The exact regions and events to capture will depend on the game, but the most important components are:
- `NamedScreenRegion`: Every `StateParser` can define certain boxes within the game screen (e.g. the top right portion where the player menu identifier will pop up). These can linked to one or more reference targets, that you need to manually capture once and save. After you save the target, the `StateParser` allows you to take any game frame, select the region in question, and compare it to the reference image. Once you've designated the named regions in the state parser, run the game in dev play mode, stop the game at the moment you want to capture. Then, run `c <region_name>` to save the screen region at that point. The [Pokémon parsers](src/gameboy_worlds/emulation/pokemon/parsers.py) show a clear example of this, and I have provided an [example](https://drive.google.com/file/d/1EEpoxHAnNwdSMSYcc93xrQCcLzbtVCyX/view?usp=sharing) video of the frames being captured. 

You will know that you have filled out all required regions when you can run `python demos/emulator.py --game <game>` without debug mode. 

To use the `StateParser` you created, make sure to:
- Add the parser to the registry
- Create a `MetricGroup` objects that calls on the parsers methods and capabilities in its `step` method
- Add these `MetricGroup` objects to a `StateParser` and then add that to the registry

#### Enabling Environment
To enable an agent to play the game in a gym-style environment loop, you must create a simple `Environment` subclass with implementations for the abstract methods, and add this to the interface registry. That is now a gym-compliant game environment. 

#### Creating HighLevelActions
The above set up gives you more descriptive state information, but still forces the agents use simple button presses to play the game. You must think of decent actions you can implement, and create `HighLevelAction` subclasses to execute them. 

#### 


### I want to engineer my own reward functions

<img src="assets/logo.png" width="70"> avoids most domain-knowledge specific reward design, with a motivation of having the agent discover the best policy with minimal guidance. But it's absolutely possible to use your knowledge of the game to create sophisticated reward systems, like [other people](https://www.youtube.com/watch?v=DcYLT37ImBY&feature=youtu.be) have. 

You'll likely want to gather as much state and trajectory information as possible, for which you should see the [section above](#I-want-to-create-my-own-starting-states).

Then, you'll want to create your own `Environment` subclass, and configure the reward return. See [`PokemonRedChooseCharmanderFastEnv`](src/gameboy_worlds/interface/pokemon/environments.py#90) for more


### Extras:

**Setup Speedrun Guide:**
I've documented the fastest workflow I have found to capturing all the screens for a Pokémon ROM hack properly. This may come in handy for someone. 

Start by just playing through the game (super high `gameboy_headed_emulation_speed`) and establishing save states for the following:
1. `initial`: Right out of the intro screen with options set to fastest / least animation
2. `starter`: Right before the player needs to make a choice of starter
3. `pokedex`: Not too long after the player obtains the Pokedex, but anywhere you like. 

Then, start with:
```
python dev/dev_play.py --game <game> --init_state initial
```
You can tick off the following captures:
* `dialogue_bottom_right`: usually theres something you can interact with in your starting room
* `menu_top_right`: open the start menu
* `pc_top_left`: there is often a PC in your room
* `player_card_middle`: open your player card
* `map_bottom_right`: usually there's a map around you

Then, switch out to the start choice state with `l starter`. Use this state to capture:
* `dialogue_choice_bottom_right`: confirmation message for starter
* `name_entity_top_left`: give the starter a nickname
* `battle_enemy_hp_text`: either a rival battle or just your first Pokémon battle
* `battle_player_hp_text`: same
* `pokemon_list_hp_text`: can do once you've got the starter

Then honestly you probably want to exit with `e` and start again at the `pokedex` state with:
```bash
python dev/dev_play.py --game <game> --init_state pokedex
```
You'll get a message letting you know what's left. You can finish them all off now. If any of the captures weren't clean and good, you should leave them for the end and override their named screen regions. 

Using this process I'm able to set up all but one capture in [under 10 minutes](https://drive.google.com/file/d/1KkZZe3ON-0EWiBs_EhrAHc9D7lsQmCxW/view?usp=sharing) (the video cuts off with only `pokedex_info_height_text` unassigned because it needs to be manually repositioned as an override region). 

### I want to add a new test task

To create a new test task that automatically detects when an agent succeeds (or fails) at a specific goal, follow these steps:

**1. Create an initial state**
First, create a starting state from which your task is achievable. See the [section above](#i-want-to-create-my-own-starting-states) for detailed instructions on creating states.

**2. Define termination and truncation conditions**
- **Termination**: The goal has been achieved. This should be a reliably reproducible screen element that always appears when the goal is reached (e.g., unique dialogue when defeating a specific trainer). In this framework, termination always equals task success - we avoid failure termination signals to prevent agents from using them as learning feedback.
- **Truncation**: Optional. Cut the episode short when the player can no longer achieve the task (e.g., walked too far away). Maximum environment / emulator steps are handled automatically, so don't bother implementing that. 

**3. Set up parser for screen capture (if needed)**
If your termination condition relies on a specific screen capture not already available in the parser, you'll need to add it. See the [screen capture method](#state-parser-set-up) in the [section above](#i-want-to-track-fine-grained-details) for guidance on capturing named screen regions.

Make sure to use `python -m gameboy_worlds.setup_data push --game <game>` to update the cloud database. 

**4. Create the termination/truncation metric**
Make a child or descendant of the [TerminationTruncationTracker](src/gameboy_worlds/emulation/tracker.py) :
- For termination only: `TerminationMetric` ([line 466](src/gameboy_worlds/emulation/tracker.py:466))
- For both termination and truncation: `TerminationTruncationMetric` ([line 368](src/gameboy_worlds/emulation/tracker.py:368))

If using screen region comparisons (most common), inherit from:
- `RegionMatchTerminationMetric` ([line 717](src/gameboy_worlds/emulation/tracker.py:717))
- `RegionMatchTruncationMetric` ([line 693](src/gameboy_worlds/emulation/tracker.py:693))

Example: [`PokemonCenterTerminateMetric`](src/gameboy_worlds/emulation/pokemon/test_metrics.py:15) inherits from both `RegionMatchTerminationMetric` and `TerminationMetric`.

**5. Create the test tracker**
Most trackers can be created by simply setting the `TERMINATION_TRUNCATION_METRIC` class parameter. See [`PokemonRedCenterTestTracker`](src/gameboy_worlds/emulation/pokemon/trackers.py:72) for an example.

```python
class MyTestTracker(PokemonTestTracker):
    TERMINATION_TRUNCATION_METRIC = MyCustomTerminateMetric
```

**6. Register the tracker**
Add your new tracker to the [`AVAILABLE_STATE_TRACKERS`](src/gameboy_worlds/emulation/registry.py:58) dictionary in the registry with a descriptive name.

**7. Test your implementation**
Verify it works with the test play script:

```bash
python dev/dev_play.py --game <game> --state_tracker_class <your_tracker_name> --init_state <your_start_state>
```

The game should automatically stop when you reach the termination/truncation condition.

*Example video: [here](https://drive.google.com/file/d/1j5u8N1OFm45pa6sf3aGnXxfFyYaDt8Ei/view?usp=sharing)*

#### Detailed Mechanical Walkthrough (Harry Potter Example)

The steps above cover the general process, but here is a more mechanical, copy-pasteable walkthrough of the same workflow, using the example of adding a "navigate to the white car" task to Harry Potter: Chamber of Secrets.

**Role Legend:**
- 🧑 **(Human)**: Requires manual effort from you (playing the game, visual verification).
- 🤖 **(LLM)**: An LLM can easily write or autofill this code for you if you provide it the names.

**Step 1: Create an Initial Save State**

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

**Step 2: Configure the Parser and Capture Target Regions**

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

   🧑 *(Human)* Caveat: You must manually determine the bounding box dimensions for this to make sense.

2. 🧑 **(Human) Play to the "Success" Screen:**
   *(Pitfalls: Ensure you have changed `gameboy_dev_play_stop` back to `false` in `configs/gameboy_vars.yaml` first. You MUST ALSO ensure `debug_mode: true` is set in `configs/project_vars.yaml`. If `debug_mode` is false, the emulator will instantly crash on boot because it strictly verifies that all targets defined in `parsers.py` have matching `.npy` files on disk!)*
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
   *(CRITICAL WARNING: Do NOT put a space after the comma! The command must be exactly one continuous string. If you add a space, a bug in the terminal parser will ignore your input and accidentally save a screenshot of whatever bounding box you used previously!)*
   *(Note: The `c` command references the region name defined in your parser, followed by a comma, followed by the specific target name. This saves it to a `.npy` file. Verify the image pop-up looks correct before closing it).*

**Step 3: Define the Termination Metric**

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

**Step 3.5: Define Subgoals (Highly Recommended)**

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

**Step 4: Define the Tracker**

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

**Step 5: Register the Tracker**

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

**Step 6: Add Task to the Benchmark Database**

Your task must be documented in the CSV so the evaluation framework can iterate over it.

1. 🤖 **(LLM) Update the CSV:**
   Open `benchmark/tests/harry_potter.csv`. Add a new line for your task matching the exact schema:
   ```csv
   harry_potter_chamber_of_secrets,navigation,navigate to the white car,burrow_start,navigate_to_car_test,harry_potter_philosophers_stone,True
   ```
   *(Schema: game, task_category, task_description, init_state, state_tracker_class, shifted_training_games, can_train_from_init_state)*

**Step 7: Test Your Implementation (Crucial)**

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

**Step 8: Push Data to Hugging Face & Pull Request**

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


### Useful Things

* `demos/environment.py`: You can specify a game, environment_variant or controller_variant to test parsing, HighLevelActions etc.

Everything in `dev`:
* `dev_play.py`: vital for being able to play the game, pause the game and capture the screen or enter a breakpoint. 
* `list_states.py`: prints out all of the states you've saved so far and writes them to `tmp_state_list.csv`

