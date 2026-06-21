"""State trackers for Survival Kids."""

from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.tracker import DummySubGoalMetric, TestTrackerMixin
from gameboy_worlds.emulation.survival_kids.base_metrics import (
    CoreSurvivalKidsMetrics,
    SurvivalKidsExploreMetrics,
    SurvivalKidsHudMetrics,
    SurvivalKidsOCRMetric,
    SurvivalKidsVitalMetrics,
)
from gameboy_worlds.emulation.survival_kids.test_metrics import (
    AfterDrinkingWaterTerminateMetric,
    AfterFillingWaterTerminateMetric,
    AfternoonReferenceTerminateMetric,
    BagIconTerminateMetric,
    BurnConfirmTerminateMetric,
    AnimalKilledTerminateMetric,
    CanteenActionMenuTerminateMetric,
    CanteenChosenTerminateMetric,
    CanteenDrinkSelectedTerminateMetric,
    CanteenPickupDialogueTerminateMetric,
    CanteenTakeLeaveMenuTerminateMetric,
    CanteenUseSelectedTerminateMetric,
    Chapter1PathClearedTerminateMetric,
    ClubEquippedScreenTerminateMetric,
    CookedMeatActionMenuTerminateMetric,
    CookedMeatEatenDialogueTerminateMetric,
    CookedMeatEatSelectedTerminateMetric,
    CookedMeatStoredTerminateMetric,
    DayReferenceTerminateMetric,
    DrinkWaterTerminateMetric,
    EnteredShelterTerminateMetric,
    FeatherTakeLeaveMenuTerminateMetric,
    FireLitTerminateMetric,
    FoundRiverTerminateMetric,
    FruitActionMenuTerminateMetric,
    FruitEatenDialogueTerminateMetric,
    FruitEatenTerminateMetric,
    FruitEatSelectedTerminateMetric,
    FruitFoundDialogueTerminateMetric,
    FruitTakenDialogueTerminateMetric,
    GameViewportChangedTerminateMetric,
    GotTheBrdfeatherTerminateMetric,
    GotTheClamTerminateMetric,
    GotTheLogTerminateMetric,
    GotTheSharpStoneTerminateMetric,
    GotTheStickTerminateMetric,
    GotTheStoneTerminateMetric,
    GotTheTreeBarkTerminateMetric,
    GotTheVineTerminateMetric,
    GotTheWaterTerminateMetric,
    GrassCutBeforePickupLogTerminateMetric,
    GrassCutBeforePushStone2TerminateMetric,
    GrassCutBeforeSharpStoneTerminateMetric,
    GrassCutTerminateMetric,
    HelmetFoundTerminateMetric,
    HpChangedTerminateMetric,
    HungerChangedTerminateMetric,
    InTheShelterTerminateMetric,
    InventoryAfterFireLitTerminateMetric,
    InventoryOpenTerminateMetric,
    InventoryOpenWithClubTerminateMetric,
    InventoryOpenWithClubNearPryStoneTerminateMetric,
    InventoryOpenWithClubNearPushStone2TerminateMetric,
    InventorySelectItemTerminateMetric,
    KindlingMergedTerminateMetric,
    KnifeEquippedScreenTerminateMetric,
    KnifeChosenTerminateMetric,
    KnifeEquippedTerminateMetric,
    LogActionMenuTerminateMetric,
    LogFoundDialogueTerminateMetric,
    LogInventoryActionMenuTerminateMetric,
    LogInventorySelectTakeTerminateMetric,
    LogSelectTakeTerminateMetric,
    MergeConfirmTerminateMetric,
    MergeMenuTerminateMetric,
    MeatActionMenuTerminateMetric,
    MeatBurnSelectedTerminateMetric,
    MeatCookedDialogueTerminateMetric,
    MeatEatenDialogueTerminateMetric,
    MeatEatSelectedTerminateMetric,
    NearPryStoneTerminateMetric,
    NearPushStone2TerminateMetric,
    NewPath1FoundTerminateMetric,
    NewPath2FoundTerminateMetric,
    NightReferenceTerminateMetric,
    ObjectTerminateMetric,
    PickupItemDialogueTerminateMetric,
    PathAfterPriedStoneTerminateMetric,
    PathAfterPushedStone2TerminateMetric,
    PathAfterBlockingGrassC1TerminateMetric,
    PathAfterBlockingGrassTerminateMetric,
    PryStoneDialogueTerminateMetric,
    PushStoneDialogue2TerminateMetric,
    ResolveHungerTerminateMetric,
    SelectClubNearPryStoneTerminateMetric,
    SelectClubTerminateMetric,
    SelectKindlingTerminateMetric,
    SelectDropTerminateMetric,
    SelectLogTerminateMetric,
    SelectMeatTerminateMetric,
    SelectTakeTerminateMetric,
    SharpStoneFoundTerminateMetric,
    StaminaChangedTerminateMetric,
    StatusBarChangedTerminateMetric,
    StonePushedOpen2TerminateMetric,
    TakeLeaveMenuTerminateMetric,
    ThirstChangedTerminateMetric,
    TreeBarkPickupDialogueTerminateMetric,
    UseKindlingTerminateMetric,
    WaterAvailableDialogueTerminateMetric,
    WaterMenuOpenTerminateMetric,
)


class SurvivalKidsTracker(StateTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([CoreSurvivalKidsMetrics, SurvivalKidsExploreMetrics])


class SurvivalKidsVitalsTracker(SurvivalKidsTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([SurvivalKidsVitalMetrics])


class SurvivalKidsHudTracker(SurvivalKidsTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([SurvivalKidsHudMetrics])


class SurvivalKidsOCRTracker(SurvivalKidsHudTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([SurvivalKidsOCRMetric])


class SurvivalKidsTestTracker(TestTrackerMixin, SurvivalKidsOCRTracker):
    TERMINATION_TRUNCATION_METRIC = StatusBarChangedTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SurvivalKidsStatusBarChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = StatusBarChangedTerminateMetric


class SurvivalKidsHpChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = HpChangedTerminateMetric


class SurvivalKidsHungerChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = HungerChangedTerminateMetric


class SurvivalKidsResolveHungerTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = ResolveHungerTerminateMetric


class SurvivalKidsThirstChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = ThirstChangedTerminateMetric


class SurvivalKidsDrinkWaterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = DrinkWaterTerminateMetric


class SurvivalKidsStaminaChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = StaminaChangedTerminateMetric


class SurvivalKidsGameViewportChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GameViewportChangedTerminateMetric


class SurvivalKidsGrassCutTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GrassCutTerminateMetric


class SurvivalKidsGrassCutBeforeSharpStoneTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GrassCutBeforeSharpStoneTerminateMetric


class SurvivalKidsGrassCutBeforePickupLogTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GrassCutBeforePickupLogTerminateMetric


class SurvivalKidsGrassCutBeforePushStone2Tracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GrassCutBeforePushStone2TerminateMetric


class SurvivalKidsInventoryOpenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InventoryOpenTerminateMetric


class SurvivalKidsInventoryOpenWithClubTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InventoryOpenWithClubTerminateMetric


class SurvivalKidsInventoryOpenWithClubNearPryStoneTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InventoryOpenWithClubNearPryStoneTerminateMetric


class SurvivalKidsInventoryOpenWithClubNearPushStone2Tracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InventoryOpenWithClubNearPushStone2TerminateMetric


class SurvivalKidsInventoryAfterFireLitTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InventoryAfterFireLitTerminateMetric


class SurvivalKidsInventorySelectItemTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InventorySelectItemTerminateMetric


class SurvivalKidsPickupItemDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PickupItemDialogueTerminateMetric


class SurvivalKidsCanteenPickupDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenPickupDialogueTerminateMetric


class SurvivalKidsGotTheClamTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheClamTerminateMetric


class SurvivalKidsLogFoundDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = LogFoundDialogueTerminateMetric


class SurvivalKidsGotTheLogTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheLogTerminateMetric


class SurvivalKidsBagIconTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = BagIconTerminateMetric


class SurvivalKidsObjectTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = ObjectTerminateMetric


class SurvivalKidsHelmetFoundTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = HelmetFoundTerminateMetric


class SurvivalKidsKnifeEquippedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = KnifeEquippedTerminateMetric


class SurvivalKidsKnifeEquippedScreenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = KnifeEquippedScreenTerminateMetric


class SurvivalKidsClubEquippedScreenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = ClubEquippedScreenTerminateMetric


class SurvivalKidsKnifeChosenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = KnifeChosenTerminateMetric


class SurvivalKidsMergeMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MergeMenuTerminateMetric


class SurvivalKidsMergeConfirmTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MergeConfirmTerminateMetric


class SurvivalKidsCanteenChosenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenChosenTerminateMetric


class SurvivalKidsKindlingMergedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = KindlingMergedTerminateMetric


class SurvivalKidsTakeLeaveMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = TakeLeaveMenuTerminateMetric


class SurvivalKidsSelectTakeTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectTakeTerminateMetric


class SurvivalKidsSelectDropTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectDropTerminateMetric


class SurvivalKidsSelectClubTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectClubTerminateMetric


class SurvivalKidsSelectClubNearPryStoneTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectClubNearPryStoneTerminateMetric


class SurvivalKidsSelectLogTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectLogTerminateMetric


class SurvivalKidsSelectMeatTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectMeatTerminateMetric


class SurvivalKidsCanteenTakeLeaveMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenTakeLeaveMenuTerminateMetric


class SurvivalKidsCanteenActionMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenActionMenuTerminateMetric


class SurvivalKidsCanteenUseSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenUseSelectedTerminateMetric


class SurvivalKidsCanteenDrinkSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenDrinkSelectedTerminateMetric


class SurvivalKidsLogActionMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = LogActionMenuTerminateMetric


class SurvivalKidsLogSelectTakeTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = LogSelectTakeTerminateMetric


class SurvivalKidsLogInventoryActionMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = LogInventoryActionMenuTerminateMetric


class SurvivalKidsLogInventorySelectTakeTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = LogInventorySelectTakeTerminateMetric


class SurvivalKidsAnimalKilledTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = AnimalKilledTerminateMetric


class SurvivalKidsChapter1PathClearedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = Chapter1PathClearedTerminateMetric


class SurvivalKidsPathAfterBlockingGrassTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PathAfterBlockingGrassTerminateMetric


class SurvivalKidsPathAfterBlockingGrassC1Tracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PathAfterBlockingGrassC1TerminateMetric


class SurvivalKidsNearPryStoneTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = NearPryStoneTerminateMetric


class SurvivalKidsNearPushStone2Tracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = NearPushStone2TerminateMetric


class SurvivalKidsPathAfterPriedStoneTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PathAfterPriedStoneTerminateMetric


class SurvivalKidsStonePushedOpen2Tracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = StonePushedOpen2TerminateMetric


class SurvivalKidsPathAfterPushedStone2Tracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PathAfterPushedStone2TerminateMetric


class SurvivalKidsInTheShelterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InTheShelterTerminateMetric


class SurvivalKidsNewPath1FoundTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = NewPath1FoundTerminateMetric


class SurvivalKidsNewPath2FoundTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = NewPath2FoundTerminateMetric


class SurvivalKidsSharpStoneFoundTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SharpStoneFoundTerminateMetric


class SurvivalKidsDayReferenceTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = DayReferenceTerminateMetric


class SurvivalKidsAfternoonReferenceTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = AfternoonReferenceTerminateMetric


class SurvivalKidsNightReferenceTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = NightReferenceTerminateMetric


class SurvivalKidsEnteredShelterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnteredShelterTerminateMetric


class SurvivalKidsFoundRiverTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FoundRiverTerminateMetric


class SurvivalKidsWaterMenuOpenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = WaterMenuOpenTerminateMetric


class SurvivalKidsWaterAvailableDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = WaterAvailableDialogueTerminateMetric


class SurvivalKidsPryStoneDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PryStoneDialogueTerminateMetric


class SurvivalKidsPushStoneDialogue2Tracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PushStoneDialogue2TerminateMetric


class SurvivalKidsAfterFillingWaterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = AfterFillingWaterTerminateMetric


class SurvivalKidsAfterDrinkingWaterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = AfterDrinkingWaterTerminateMetric


class SurvivalKidsGotTheWaterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheWaterTerminateMetric


class SurvivalKidsGotTheStickTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheStickTerminateMetric


class SurvivalKidsGotTheTreeBarkTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheTreeBarkTerminateMetric


class SurvivalKidsGotTheSharpStoneTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheSharpStoneTerminateMetric


class SurvivalKidsGotTheStoneTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheStoneTerminateMetric


class SurvivalKidsGotTheVineTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheVineTerminateMetric


class SurvivalKidsGotTheBrdfeatherTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheBrdfeatherTerminateMetric


class SurvivalKidsSelectKindlingTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectKindlingTerminateMetric


class SurvivalKidsUseKindlingTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = UseKindlingTerminateMetric


class SurvivalKidsFireLitTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FireLitTerminateMetric


class SurvivalKidsFeatherTakeLeaveMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FeatherTakeLeaveMenuTerminateMetric


class SurvivalKidsFruitFoundDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FruitFoundDialogueTerminateMetric


class SurvivalKidsFruitActionMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FruitActionMenuTerminateMetric


class SurvivalKidsFruitEatSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FruitEatSelectedTerminateMetric


class SurvivalKidsFruitTakenDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FruitTakenDialogueTerminateMetric


class SurvivalKidsFruitEatenDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FruitEatenDialogueTerminateMetric


class SurvivalKidsFruitEatenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FruitEatenTerminateMetric


class SurvivalKidsTreeBarkPickupDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = TreeBarkPickupDialogueTerminateMetric


class SurvivalKidsMeatActionMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MeatActionMenuTerminateMetric


class SurvivalKidsCookedMeatActionMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CookedMeatActionMenuTerminateMetric


class SurvivalKidsCookedMeatEatSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CookedMeatEatSelectedTerminateMetric


class SurvivalKidsMeatBurnSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MeatBurnSelectedTerminateMetric


class SurvivalKidsBurnConfirmTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = BurnConfirmTerminateMetric


class SurvivalKidsMeatEatSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MeatEatSelectedTerminateMetric


class SurvivalKidsMeatEatenDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MeatEatenDialogueTerminateMetric


class SurvivalKidsMeatCookedDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MeatCookedDialogueTerminateMetric


class SurvivalKidsCookedMeatEatenDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CookedMeatEatenDialogueTerminateMetric


class SurvivalKidsCookedMeatStoredTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CookedMeatStoredTerminateMetric
