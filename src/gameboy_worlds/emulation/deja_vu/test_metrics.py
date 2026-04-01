import numpy as np

from gameboy_worlds.emulation.deja_vu.parsers import DejaVu1StateParser
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationMetric,
    RegionMatchTerminationOnlyMetric,
    SubGoal,
    SubGoalMetric,
    TerminationMetric,
    AnyRegionMatchSubGoal
)

# class DejaVuCoatSubGoalMetric(SubGoalMetric):
#     """SubGoalMetric for the take_coat_test task, tracking 'Take' action selection as an intermediate step."""

#     REQUIRED_PARSER = DejaVu1StateParser
#     SUBGOALS = [SelectedTakeActionSubGoal]

# class DejaVuCoatTerminationMetric(RegionMatchTerminationMetric, TerminationMetric):
class TakeCoatTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "took_coat"

class TakeGunTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "took_gun"

class OpenDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_door"

class CloseDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_door"

class OpenPocketTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_pocket"

class OpenWalletTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_wallet"

# class ClosedPocketTerminationMetric(RegionMatchTerminationOnlyMetric):
#     REQUIRED_PARSER = DejaVu1StateParser

#     _TERMINATION_NAMED_REGION = "dialogue_box_area"
#     _TERMINATION_TARGET_NAME = "closed_pocket"


# subgoal classes
class SelectedTakeActionInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_take_action"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["selected_take_action"]

class SelectedOpenActionInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_open_action"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["selected_open_action"]

class SelectedCloseActionInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_close_action"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["selected_close_action"]

class NoActionSelectedInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_selected"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["no_action_selected"]

class SelectedTakeActionInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_take_action_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["selected_take_action"]

class SelectedOpenActionInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_open_action_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["selected_open_action"]

class SelectedCloseActionInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_close_action_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["selected_close_action"]

class NoActionSelectedInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_selected_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["no_action_selected"]