from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.harry_potter.base_metrics import HarryPotterOCRMetric
from gameboy_worlds.emulation.harry_potter.test_metrics import (
    PotionsShopTerminateMetric,
    OllivandersInteriorTerminateMetric,
    OutsideOllivandersSubgoal,
    GetWandTerminateMetric,
    TalkToOllivanderSubgoal,
    ReceiveFolioMagiTerminateMetric,
    BoyApproachesSubgoal,
    SelectCardDeckTerminateMetric,
    CardOptionsShownSubgoal,
    GringottsInteriorTerminateMetric,
    OutsideGringottsSubgoal,
    TalkHagridGringottsTerminateMetric,
    FindHagridGringottsSubgoal,
    ReenterGringottsSubgoal,
    ExitGringottsTerminateMetric,
    TalkToWeasleysSubgoal,
    OnTrainTerminateMetric,
    TalkToRonWeasleySubgoal,
    ChocolateFrogs5InventoryTerminateMetric,
    SellChocolateFrogSubgoal,
    ChocolateFrogs4InventoryTerminateMetric,
    StartOfDuelSubgoal,
    LoseDuelTerminateMetric,
    WinDuelTerminateMetric,
    LeftmostTrainCarTerminateMetric,
    RightmostTrainCarSubgoal,
    LeftmostTrainCarSubgoal,
    GainLevelTerminateMetric,
    GainSpellTerminateMetric,
    WinBattleTerminateMetric,
    FindBossRatSubgoal,
    RatKingSpriteSubgoal,
    UnableToEscapeSubgoal,
    RespawnDeathRatTerminateMetric,
    FullyRestoreMPSubgoal,
    UtilizeDeflectCardsSubgoal,
    # Task 14
    FindHagridVaultTerminateMetric,
    NavigateToHagridSubgoal,
    # Madam Malkin split tasks
    EnterMalkinsTerminateMetric,
    OpenMalkinsBuyMenuTerminateMetric,
    SelectRobesTerminateMetric,
    ConfirmRobesPurchaseTerminateMetric,
    OutsideMalkinsSubgoal,
    # Flourish & Blotts split tasks
    EnterFlourishBlottsTerminateMetric,
    OutsideFlourishBlottsSubgoal,
    BuyBooksTerminateMetric,
    TalkToFlourishClerkSubgoal,
    # Apothecary tasks
    EnterApothecaryTerminateMetric,
    BuyPotionKitTerminateMetric,
    OutsideApothecarySubgoal,
    ApothecaryBuyMenuOpenSubgoal,
    # Cauldron shop tasks
    EnterCauldronShopTerminateMetric,
    BuyCauldronTerminateMetric,
    OutsideCauldronShopSubgoal,
    CauldronBuyMenuOpenSubgoal,
    # Sugarplums Sweets filler tasks
    EnterSugarplumsTerminateMetric,
    OpenSugarplumsBuyMenuTerminateMetric,
    OutsideSugarplumsSubgoal,
    # Talk to Hagrid in Diagon Alley
    TalkToHagridDiagonTerminateMetric,
    # CoS Task 1
    FindDobbyTerminateMetric,
    FindDobbySubgoal,
    # CoS Task 2
    SelectCardDeckCosTerminateMetric,
    # CoS Task 3
    BoardFlyingCarTerminateMetric,
    TalkToRonCosSubgoal,
    # CoS Task 4
    EnterBurrowTerminateMetric,
    OutsideBurrowAfterCutsceneSubgoal,
    # CoS Task 5
    EnterBattleCosTerminateMetric,
    # Burrow room navigation tasks (CoS)
    EnterPercyRoomTerminateMetric,
    EnterGinnyRoomTerminateMetric,
    EnterParentsRoomTerminateMetric,
    EnterFredGeorgeRoomTerminateMetric,
    EnterRonsRoomTerminateMetric,
    TalkToRonBurrowTerminateMetric,
    EnterKitchenBurrowTerminateMetric,
    EnterBurrowGardenTerminateMetric,
    OutsideGardenDoorSubgoal,
    NavigateToCarTerminateMetric,
    StartMenuTerminateMetric,
    DiagonAlleySubgoal,
    PumpkinPastySubgoal,
    EatPumpkinPastyTerminateMetric,
    EquippedPointedHatSubgoal,
    EquippedPointedHatPlainWorkRobeTerminateMetric,
    RemoveHatSubgoal,
    RemoveRobeSubgoal,
    EmptyEquipCursorRobeTerminateMetric,
)


class HarryPotterOCRTracker(StateTracker):
    """
    Base tracker that adds OCR dialogue capture support for Harry Potter games.
    Requires the parser to have a "dialogue_box_full" region defined.
    """

    def start(self):
        super().start()
        self.metric_classes.extend([HarryPotterOCRMetric])


class HarryPotterTestTracker(TestTrackerMixin, HarryPotterOCRTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harry Potter games.
    All test trackers get OCR dialogue capture support via HarryPotterOCRTracker.
    """

    TERMINATION_TRUNCATION_METRIC = PotionsShopTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PotionsShopTestTracker(HarryPotterTestTracker):
    """
    A TestTracker for Harry Potter Philosopher's Stone that ends an episode when the agent enters the potions shop.
    """

    TERMINATION_TRUNCATION_METRIC = PotionsShopTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterOllivandersTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = OllivandersInteriorTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideOllivandersSubgoal])


class GetWandTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = GetWandTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TalkToOllivanderSubgoal])


class ReceiveFolioMagiTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = ReceiveFolioMagiTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BoyApproachesSubgoal])


class SelectCardDeckTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectCardDeckTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CardOptionsShownSubgoal])


class EnterGringottsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = GringottsInteriorTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideGringottsSubgoal])


class TalkHagridGringottsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = TalkHagridGringottsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([FindHagridGringottsSubgoal])


class ExitGringottsWithoutHagridTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = ExitGringottsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([ReenterGringottsSubgoal])


class GetOnTrainTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = OnTrainTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TalkToWeasleysSubgoal])


class BuyChocolateFrogsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = ChocolateFrogs5InventoryTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TalkToRonWeasleySubgoal])


class SellOneChocolateFrogTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = ChocolateFrogs4InventoryTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SellChocolateFrogSubgoal])


class LoseDuelTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = LoseDuelTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([StartOfDuelSubgoal])


class WinDuelTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = WinDuelTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([StartOfDuelSubgoal])


class GainLevelTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = GainLevelTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class GainSpellTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = GainSpellTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class WinBattleTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = WinBattleTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class BeatBossRatTestTracker(HarryPotterTestTracker):
    """Boss fight — termination TBD, subgoal is finding the boss rat."""
    TERMINATION_TRUNCATION_METRIC = WinBattleTerminateMetric  # placeholder until boss-specific termination
    SUBGOAL_METRIC = make_subgoal_metric_class([FindBossRatSubgoal])


class FailRatKingBattleTestTracker(HarryPotterTestTracker):
    """Fail the rat king battle by attempting to escape and dying."""
    TERMINATION_TRUNCATION_METRIC = RespawnDeathRatTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([RatKingSpriteSubgoal, UnableToEscapeSubgoal])


class DefeatRatKingWithDeflectTestTracker(HarryPotterTestTracker):
    """Restore MP, use deflect cards, and beat the rat king."""
    TERMINATION_TRUNCATION_METRIC = WinBattleTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([FullyRestoreMPSubgoal, UtilizeDeflectCardsSubgoal])


# Task 14
class FindHagridVaultTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = FindHagridVaultTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NavigateToHagridSubgoal])


# Madam Malkin split tasks (Task 15a/b/c/d)
class EnterMalkinsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterMalkinsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideMalkinsSubgoal])


class OpenMalkinsBuyMenuTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = OpenMalkinsBuyMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SelectRobesTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectRobesTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ConfirmRobesPurchaseTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = ConfirmRobesPurchaseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# Flourish & Blotts split tasks
class EnterFlourishBlottsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterFlourishBlottsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideFlourishBlottsSubgoal])


class BuyBooksTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyBooksTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TalkToFlourishClerkSubgoal])


# Apothecary tasks
class EnterApothecaryTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterApothecaryTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideApothecarySubgoal])


class BuyPotionKitTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyPotionKitTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([ApothecaryBuyMenuOpenSubgoal])


# Cauldron shop tasks
class EnterCauldronShopTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterCauldronShopTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideCauldronShopSubgoal])


class BuyCauldronTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyCauldronTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CauldronBuyMenuOpenSubgoal])


class WalkTrain3TimesTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = LeftmostTrainCarTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        RightmostTrainCarSubgoal,
        LeftmostTrainCarSubgoal,
        RightmostTrainCarSubgoal,
        LeftmostTrainCarSubgoal,
        RightmostTrainCarSubgoal
    ])


# Sugarplums Sweets filler tasks
class EnterSugarplumsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterSugarplumsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideSugarplumsSubgoal])


class OpenSugarplumsBuyMenuTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = OpenSugarplumsBuyMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# Talk to Hagrid in Diagon Alley
class TalkToHagridDiagonTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = TalkToHagridDiagonTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# CoS Task 1
class FindDobbyTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = FindDobbyTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([FindDobbySubgoal])


# CoS Task 2
class SelectCardDeckCosTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectCardDeckCosTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# CoS Task 3
class BoardFlyingCarTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = BoardFlyingCarTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TalkToRonCosSubgoal])


# CoS Task 4
class EnterBurrowTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterBurrowTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideBurrowAfterCutsceneSubgoal])


# CoS Task 5
class EnterBattleCosTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterBattleCosTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# Burrow room navigation tasks (CoS)
class EnterPercyRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterPercyRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterGinnyRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterGinnyRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterParentsRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterParentsRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterFredGeorgeRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterFredGeorgeRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterRonsRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterRonsRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class TalkToRonBurrowTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = TalkToRonBurrowTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterKitchenBurrowTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterKitchenBurrowTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterBurrowGardenTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterBurrowGardenTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideGardenDoorSubgoal])

class NavigateToCarTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = NavigateToCarTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class StartMenuTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = StartMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([DiagonAlleySubgoal])

class EatPumpkinPastyTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EatPumpkinPastyTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PumpkinPastySubgoal])

class EquipPointedHatPlainWorkRobeTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EquippedPointedHatPlainWorkRobeTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([EquippedPointedHatSubgoal])

class RemoveAllEquippedItemsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EmptyEquipCursorRobeTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([RemoveHatSubgoal, RemoveRobeSubgoal])