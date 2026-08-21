from typing import Optional

from gameboy_worlds.emulation.pokemon.parsers import (
    PokemonBrownStateParser,
    PokemonPrismStateParser,
    PokemonRedStateParser,
)
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationOnlyMetric,
    TerminationMetric,
    RegionMatchTerminationMetric,
    RegionMatchSubGoal,
    AnyRegionMatchSubGoal,
)
from gameboy_worlds.emulation.pokemon.base_metrics import (
    PokemonExitBattleTruncationMetric,
)
import numpy as np


class PokemonCenterTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "viridian_pokemon_center_entrance"


class OutsideViridianCenterSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_viridian_center"
    _NAMED_REGIONS = [
        "screen_middle",
        "screen_middle",
    ]
    _TARGET_NAMES = [
        "outside_viridian_center_from_left",
        "outside_viridian_center_from_right",
    ]


class MtMoonTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "mt_moon_entrance"


class SpeakToBillCompleteTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "talk_bill_complete"


class PickupPokeballTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "pick_up_pokeball_starting"


class ReadTrainersTipsSignTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "trainers_tips_sign"


class SpeakToCinnabarGymAideCompleteTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "cinnabar_gym_aid_complete"


class SpeakToCinnabarMonkTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "talk_cinnabar_monk"


class UsedNotVeryEffectiveAttackOnSeakingTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_not_very_effective_attack"


class DefeatedBrockTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "defeated_brock"


class DefeatedLassTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "defeated_lass"


class CaughtPidgeyTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "caught_pidgey"


class CaughtPikachuTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "caught_pikachu"


class BoughtPotionAtPewterPokemartTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_potion_at_pewter_pokemart"


class UsedPotionOnCharmanderTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_potion_on_charmander"


class OpenMapTerminateMetric(TerminationMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            self.state_parser: PokemonRedStateParser
            in_map = self.state_parser.named_region_matches_target(
                frame, "map_bottom_right"
            )
            if in_map:
                return True
        return False


# ---------------------------------------------------------------------------
# Pokemon Brown metrics
# ---------------------------------------------------------------------------


class PokemonBrownMarineBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_marine_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_marine_badge"


class PokemonBrownHailBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_hail_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_hail_badge"


class PokemonBrownSproutBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_sprout_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_sprout_badge"


class PokemonBrownSparkyBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_sparky_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_sparky_badge"


class PokemonBrownFistBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_fist_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_fist_badge"


class PokemonBrownEquityBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_equity_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_equity_badge"


class PokemonBrownStarBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_star_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_star_badge"


class PokemonBrownPsiBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_psi_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_psi_badge"


class PokemonBrownChampionshipTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonBrownStateParser
    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "collect_championship"


# ---------------------------------------------------------------------------
# Pokemon Prism metrics
# ---------------------------------------------------------------------------


class PokemonPrismPyreBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_pyre_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_pyre_badge"


class PokemonPrismNatureBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_nature_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_nature_badge"


class PokemonPrismCharmBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_charm_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_charm_badge"


class PokemonPrismMidnightBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_midnight_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_midnight_badge"


class PokemonPrismMuscleBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_muscle_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_muscle_badge"


class PokemonPrismHazeBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_haze_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_haze_badge"


class PokemonPrismRaucousBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_raucous_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_raucous_badge"


class PokemonPrismNaljoBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_naljo_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_naljo_badge"


class PokemonPrismChampionshipTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonPrismStateParser
    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "collect_championship"
