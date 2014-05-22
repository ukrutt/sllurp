"""Implementations of LLRP parameters from Section 17.2 of the LLRP 1.1 protocol
specification.

Section headers like 17.x.x.x refer to version 1.1 of the LLRP specification.
They often appear out of order in this file because parameters are often nested,
and children must precede their parents."""

from construct import *
from .common import TLVParameterHeader, TVParameterHeader, IntRange, \
     StatusCode, AirProtocol

Tests = {}

# 17.2.2.1
UTCTimestamp = Struct("UTCTimestamp",
        TLVParameterHeader(128),
        UBInt64("Microseconds"))

# 17.2.2.2
Uptime = Struct("Uptime",
        TLVParameterHeader(129),
        UBInt64("Microseconds"))

# 17.2.3.1
GeneralDeviceCapabilities = Struct("GeneralDeviceCapabilities",
        TLVParameterHeader(137),
        UBInt16("MaxNumberOfAntennaSupported"),
        EmbeddedBitStruct(
            Flag("CanSetAntennaProperties"),
            Flag("HasUTCClockCapability"),
            Padding(14)),
        UBInt32("DeviceManufacturerName"),
        UBInt32("ModelName"),
        UBInt16("FirmwareVersionByteCount"),
        String("ReaderFirmwareVersion",
            lambda ctx: ctx["FirmwareVersionByteCount"]),

        # 17.2.3.1.2
        GreedyRange(Struct("ReceiveSensitivityTableEntry",
                TLVParameterHeader(139),
                UBInt16("Index"),
                IntRange(UBInt16("ReceiveSensitivityValue"), 0, 128))),

        # 17.2.3.1.3
        OptionalGreedyRange(Struct("PerAntennaReceiveSensitivityRange",
                TLVParameterHeader(149),
                UBInt16("AntennaID"),
                UBInt16("ReceiveSensitivityIndexMin"),
                UBInt16("ReceiveSensitivityIndexMax"))),

        # 17.2.3.1.5
        Struct("GPIOCapabilities",
                TLVParameterHeader(141),
                UBInt16("NumGPIs"),
                UBInt16("NumGPOs")),

        # 17.2.3.1.4
        GreedyRange(Struct("PerAntennaAirProtocol",
                    TLVParameterHeader(140),
                    UBInt16("AntennaID"),
                    UBInt16("NumProtocols"),
                    Array(lambda ctx: ctx.NumProtocols, AirProtocol))),

        # 17.2.3.1.1
        Optional(Struct("MaximumReceiveSensitivity",
                    TLVParameterHeader(363),
                    UBInt16("MaximumSensitivity")))
        )

# 17.2.3.2
LLRPCapabilities = Struct("LLRPCapabilities",
        TLVParameterHeader(142),
        EmbeddedBitStruct(
            Flag("CanDoRFSurvey"),
            Flag("CanReportBufferFillWarning"),
            Flag("SupportsClientRequestOpSpec"),
            Flag("CanDoTagInventoryStateAwareSingulation"),
            Flag("SupportsEventAndReportHolding"),
            Padding(3)),
        IntRange(UBInt8("MaxPriorityLevelSupported"), 0, 7),
        UBInt16("ClientRequestOpSpecTimeout"),
        UBInt32("MaxNumROSpecs"),
        UBInt32("MaxNumSpecsPerROSpec"),
        UBInt32("MaxNumInventoryParameterSpecsPerAISpec"),
        UBInt32("MaxNumAccessSpecs"),
        UBInt32("MaxNumOpSpecsPerAccessSpec"))

# 17.2.3.4.1
UHFBandCapabilities = Struct("UHFBandCapabilities",
        TLVParameterHeader(144),

        # 17.2.3.4.1.1
        GreedyRange(Struct("TransmitPowerLevelTableEntry",
                TLVParameterHeader(145),
                IntRange(UBInt16("Index"), 0, 255),
                UBInt16("TransmitPowerValue"))),

        # 17.2.3.4.1.2
        Struct("FrequencyInformation",
            TLVParameterHeader(146),
            EmbeddedBitStruct(
                Flag("Hopping"),
                Padding(7)),

            # 17.2.3.4.1.2.1
            OptionalGreedyRange(Struct("FrequencyHopTable",
                    TLVParameterHeader(147),
                    UBInt8("HopTableID"),
                    Padding(1),
                    UBInt16("NumHops"),
                    Array(lambda ctx: ctx.NumHops, UBInt32("Frequency")))),

            # 17.2.3.4.1.2.2
            Optional(Struct("FixedFrequencyTable",
                    TLVParameterHeader(148),
                    UBInt16("NumFrequencies"),
                    Array(lambda ctx: ctx.NumFrequencies,
                        UBInt32("Frequency"))))),

        # 17.3.1.1.2
        GreedyRange(Struct("UHFC1G2RFModeTable",
                    TLVParameterHeader(328),

                    # 17.3.1.1.2.1
                    GreedyRange(Struct("UHFC1G2RFModeTableEntry",
                            TLVParameterHeader(329),
                            UBInt32("ModeIdentifier"),
                            EmbeddedBitStruct(
                                Flag("DivideRatio"),
                                Alias("DR", "DivideRatio"),
                                Flag("EPCHAGT&CConformance"),
                                Padding(6)),

                            Enum(UBInt8("Modulation"),
                                FM0 = 0,
                                Miller2 = 1,
                                Miller4 = 2,
                                Miller8 = 3),
                            Alias("Mod", "Modulation"),

                            Enum(UBInt8("ForwardLinkModulation"),
                                PR_ASK = 0,
                                SSB_ASK = 1,
                                DSB_ASK = 2),
                            Alias("FLM", "ForwardLinkModulation"),

                            Enum(UBInt8("SpectralMaskIndicator"),
                                    Unknown = 0,
                                    SingleInterrogator = 1,
                                    MultiInterrogator = 2,
                                    DenseInterrogator = 3),
                            Alias("M", "SpectralMaskIndicator"),

                            IntRange(UBInt32("BackscatterDataRate"),
                                40e3, 640e3),
                            Alias("BDR", "BackscatterDataRate"),

                            IntRange(UBInt32("PIE"), 1500, 2000),
                            IntRange(UBInt32("MinTari"), 6250, 25000),
                            IntRange(UBInt32("MaxTari"), 6250, 25000),
                            IntRange(UBInt32("StepTari"), 0, 18750)
                            )))),

        # 17.2.3.4.1.3
        Optional(Struct("RFSurveyFrequencyCapabilities",
                    TLVParameterHeader(365),
                    UBInt32("MinimumFrequency"),
                    UBInt32("MaximumFrequency"))))


# 17.2.3.4
RegulatoryCapabilities = Struct("RegulatoryCapabilities",
        TLVParameterHeader(143),
        UBInt16("CountryCode"),
        UBInt16("CommunicationsStandard"),
        Optional(UHFBandCapabilities),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.1.1.1.1
PeriodicTriggerValue = Struct("PeriodicTriggerValue",
        TLVParameterHeader(180),
        UBInt32("Offset"),
        UBInt32("Period"),
        Optional(UTCTimestamp))

# 17.2.4.1.1.1.2
GPITriggerValue = Struct("GPITriggerValue",
        TLVParameterHeader(181),
        IntRange(UBInt16("GPIPortNum"), 0, 65535),
        EmbeddedBitStruct(
            Flag("GPIEvent"),
            Alias("E", "GPIEvent"),
            Padding(7)),
        UBInt32("Timeout"))

# 17.2.4.1.1.1
ROSpecStartTrigger = Struct("ROSpecStartTrigger",
        TLVParameterHeader(179),
        Enum(UBInt8("ROSpecStartTriggerType"),
            Null = 0,
            Immediate = 1,
            Periodic = 2,
            GPI = 3),
        If(lambda ctx: ctx.ROSpecStartTriggerType == "Periodic",
            PeriodicTriggerValue),
        If(lambda ctx: ctx.ROSpecStartTriggerType == "GPI",
            GPITriggerValue))

# 17.2.4.1.1.2
ROSpecStopTrigger = Struct("ROSpecStopTrigger",
        TLVParameterHeader(182),
        Enum(UBInt8("ROSpecStopTriggerType"),
            Null = 0,
            Duration = 1,
            GPI = 2),
        UBInt32("DurationTriggerValue"),
        Optional(GPITriggerValue))

# 17.2.4.1.1
ROBoundarySpec = Struct("ROBoundarySpec",
        TLVParameterHeader(178),
        ROSpecStartTrigger,
        ROSpecStopTrigger)

# 17.2.4.2.1.1
TagObservationTrigger = Struct("TagObservationTrigger",
        TLVParameterHeader(185),
        Enum(UBInt8("TriggerType"),
            UponNTagObservations = 0,
            UponTimeout = 1,
            NAttempts = 2,
            NUniqueTags = 3,
            UponUniqueTimeout = 4),
        UBInt16("NumberOfTags"),
        UBInt16("NumberOfAttempts"),
        UBInt16("T"),
        UBInt32("Timeout"))

# 17.2.4.2.1
AISpecStopTrigger = Struct("AISpecStopTrigger",
        TLVParameterHeader(184),
        Enum(UBInt8("AISpecStopTriggerType"),
            Null = 0,
            Duration = 1,
            GPIWithTimeout = 2,
            TagObservation = 3),
        Padding(1),
        UBInt32("DurationTrigger"),
        If(lambda ctx: ctx.AISpecStopTriggerType == "GPIWithTimeout",
            GPITriggerValue),
        If(lambda ctx: ctx.AISpecStopTriggerType == "TagObservation",
            TagObservationTrigger))

# 17.2.6.7
RFReceiverSettings = Struct("RFReceiverSettings",
        TLVParameterHeader(223),
        UBInt16("ReceiveSensitivity"))

# 17.2.6.8
RFTransmitterSettings = Struct("RFTransmitterSettings",
        TLVParameterHeader(224),
        UBInt16("HopTableID"),
        UBInt16("ChannelIndex"),
        UBInt16("TransmitPower"))

# 17.3.1.2.1.1.1
C1G2TagInventoryMask = Struct("C1G2TagInventoryMask",
        TLVParameterHeader(332),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("Pointer"),
        UBInt16("MaskBitCount"),
        MetaField("TagMask", lambda ctx: ctx.MaskBitCount / 8))
Tests["C1G2TagInventoryMask"] = "014c" "80" "0000" "60" \
        "ffffffffffffffffffffffff"

# 17.3.1.2.1.1.2
C1G2TagInventoryStateAwareFilterAction = \
    Struct("C1G2TagInventoryStateAwareFilterAction",
        TLVParameterHeader(333),
        IntRange(UBInt8("Target"), 0, 4),
        IntRange(UBInt8("Action"), 0, 7))

# 17.3.1.2.1.1.3
C1G2TagInventoryStateUnawareFilterAction = \
    Struct("C1G2TagInventoryStateUnawareFilterAction",
        TLVParameterHeader(334),
        IntRange(UBInt8("Action"), 0, 5))

# 17.3.1.2.1.1
C1G2Filter = Struct("C1G2Filter",
        TLVParameterHeader(331),
        EmbeddedBitStruct(
            Enum(BitField("T", 2),
                Unspecified = 0,
                DoNotTruncate = 1,
                Truncate = 2),
            Padding(6)),
        C1G2TagInventoryMask,
        Optional(C1G2TagInventoryStateAwareFilterAction),
        Optional(C1G2TagInventoryStateUnawareFilterAction))

# 17.3.1.2.1.2
C1G2RFControl = Struct("C1G2RFControl",
        TLVParameterHeader(335),
        UBInt16("ModeIndex"),
        IntRange(UBInt16("Tari"), 6250, 25000))

# 17.3.1.2.1.3.1
C1G2TagInventoryStateAwareSingulationAction = \
    Struct("C1G2TagInventoryStateAwareSingulationAction",
        TLVParameterHeader(337),
        EmbeddedBitStruct(
            Flag("I"),
            Flag("S"),
            Flag("S_All"),
            Alias("A", "S_All")))

# 17.3.1.2.1.3
C1G2SingulationControl = Struct("C1G2SingulationControl",
        TLVParameterHeader(336),
        IntRange(UBInt8("Session"), 0, 3),
        Alias("S", "Session"),
        UBInt16("TagPopulation"),
        UBInt32("TagTransitTime"),
        Optional(C1G2TagInventoryStateAwareSingulationAction))

# 17.3.1.2.1
C1G2InventoryCommand = Struct("C1G2InventoryCommand",
        TLVParameterHeader(330),
        OptionalGreedyRange(C1G2Filter),
        Optional(C1G2RFControl),
        Optional(C1G2SingulationControl),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.6.6
AntennaConfiguration = Struct("AntennaConfiguration",
        TLVParameterHeader(222),
        UBInt16("AntennaID"),
        Optional(RFReceiverSettings),
        Optional(RFTransmitterSettings),
        OptionalGreedyRange(C1G2InventoryCommand),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.2.2
InventoryParameterSpec = Struct("InventoryParameterSpec",
        TLVParameterHeader(186),
        UBInt16("InventoryParameterSpecID"),
        AirProtocol,
        OptionalGreedyRange(AntennaConfiguration),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.2
AISpec = Struct("AISpec",
        TLVParameterHeader(183),
        UBInt16("AntennaCount"),
        GreedyRange(UBInt16("AntennaID")),
        AISpecStopTrigger,
        GreedyRange(InventoryParameterSpec),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.3.1
RFSurveySpecStopTrigger = Struct("RFSurveySpecStopTrigger",
        TLVParameterHeader(188),
        Enum(UBInt8("StopTriggerType"),
            Null = 0,
            Duration = 1,
            NIterations = 2),
        UBInt32("Duration"),
        UBInt32("N"))

# 17.2.4.3
RFSurveySpec = Struct("RFSurveySpec",
        TLVParameterHeader(187),
        UBInt16("AntennaID"),
        UBInt32("StartFrequency"),
        UBInt32("EndFrequency"),
        RFSurveySpecStopTrigger,
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.4
LoopSpec = Struct("LoopSpec",
        TLVParameterHeader(355),
        UBInt32("LoopCount"))

# 17.3.1.5.1
C1G2EPCMemorySelector = Struct("C1G2EPCMemorySelector",
        TLVParameterHeader(348),
        EmbeddedBitStruct(
            Flag("EnableCRC"),
            Alias("C", "EnableCRC"),
            Flag("EnablePCBits"),
            Alias("P", "EnablePCBits"),
            Flag("EnableXPCBits"),
            Alias("X", "EnableXPCBits"),
            Padding(5)))

# 17.2.7.1.1
TagReportContentSelector = Struct("TagReportContentSelector",
        TLVParameterHeader(238),
        EmbeddedBitStruct(
            Flag("EnableROSpecID"),
            Alias("R", "EnableROSpecID"),
            Flag("EnableSpecIndex"),
            Alias("I", "EnableSpecIndex"),
            Flag("EnableInventoryParameterSpecID"),
            Alias("P", "EnableInventoryParameterSpecID"),
            Flag("EnableAntennaID"),
            Alias("A", "EnableAntennaID"),
            Flag("EnableChannelIndex"),
            Alias("C", "EnableChannelIndex"),
            Flag("EnablePeakRSSI"),
            Alias("RS", "EnablePeakRSSI"),
            Flag("EnableFirstSeenTimestamp"),
            Alias("F", "EnableFirstSeenTimestamp"),
            Flag("EnableLastSeenTimestamp"),
            Alias("L", "EnableLastSeenTimestamp"),
            Flag("EnableTagSeenCount"),
            Alias("T", "EnableTagSeenCount"),
            Flag("EnableAccessSpecID"),
            Alias("S", "EnableAccessSpecID"),
            Padding(6)),
        OptionalGreedyRange(C1G2EPCMemorySelector),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.7.1
ROReportSpec = Struct("ROReportSpec",
        TLVParameterHeader(237),
        Enum(UBInt8("ROReportTrigger"),
            Null = 0,
            UponNTagReportsOrEndOfAISpec = 1,
            UponNTagReportsOrEndOfROSpec = 2,
            UponNSecondsOrEndOfAISpec = 3,
            UponNSecondsOrEndOfROSpec = 4,
            UponNMillisecondsOrEndOfAISpec = 5,
            UponNMillisecondsOrEndOfROSpec = 6),
        UBInt16("N"),
        TagReportContentSelector,
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.1
ROSpec = Struct("ROSpec",
        TLVParameterHeader(177),
        UBInt32("ROSpecID"),
        IntRange(UBInt8("Priority"), 0, 7),
        Enum(UBInt8("CurrentState"),
            Disabled = 0,
            Inactive = 1,
            Active = 2),
        ROBoundarySpec,

        # unordered sequence of AISpec, RFSurveySpec, or LoopSpec
        # XXX a Union isn't quite right, because these are all different sizes.
        OptionalGreedyRange(AISpec),
        OptionalGreedyRange(RFSurveySpec),
        OptionalGreedyRange(LoopSpec),

        Optional(ROReportSpec))

# 17.2.8.1
LLRPStatus = Struct("LLRPStatus",
        TLVParameterHeader(287),
        StatusCode,
        UBInt16("ErrorDescriptionByteCount"),
        If(lambda ctx: ctx.ErrorDescriptionByteCount,
            String("ErrorDescription",
                lambda ctx: ctx.ErrorDescriptionByteCount)),
        Optional(Struct("FieldError",
            TLVParameterHeader(288),
            UBInt16("FieldNum"),
            UBInt16("ErrorCode"), # XXX Enum?
            )),
        Optional(Struct("ParameterError",
            TLVParameterHeader(289),
            UBInt16("ParameterType"),
            UBInt16("ErrorCode"), # XXX Enum?
            ))
        )

# 17.3
C1G2LLRPCapabilities = Struct("C1G2LLRPCapabilities",
        TLVParameterHeader(327),
        EmbeddedBitStruct(
            Flag("CanSupportBlockErase"),
            Flag("CanSupportBlockWrite"),
            Flag("CanSupportBlockPermalock"),
            Flag("CanSupportTagRecommissioning"),
            Flag("CanSupportUMIMethod2"),
            Flag("CanSupportXPC"),
            Padding(2)),
        UBInt16("MaxNumSelectFiltersPerQuery"))

# 17.3.1.3.1
C1G2TagSpec = None

# 17.3.1.3.1.1
C1G2TargetTag = None

# 17.3.1.3.2.1
C1G2Read = None

# 17.3.1.3.2.2
C1G2Write = None

# 17.3.1.3.2.3
C1G2Kill = None

# 17.3.1.3.2.4
C1G2Recommission = None

# 17.3.1.3.2.5
C1G2Lock = None

# 17.3.1.3.2.6
C1G2BlockErase = None

# 17.3.1.3.2.7
C1G2BlockWrite = None

# 17.3.1.3.2.8
C1G2BlockPermalock = None

# 17.3.1.3.2.9
C1G2BlockPermalockStatus = None
