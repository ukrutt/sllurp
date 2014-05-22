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

# 17.3.1.3.1.1
C1G2TargetTag = Struct("C1G2TargetTag",
        TLVParameterHeader(339),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Flag("Match"),
            Alias("M", "Match"),
            Padding(5)),
        UBInt16("Pointer"),
        UBInt16("MaskBitCount"),
        MetaField("TagMask", lambda ctx: ctx.MaskBitCount / 8),
        UBInt16("DataBitCount"),
        MetaField("TagData", lambda ctx: ctx.DataBitCount / 8))

# 17.3.1.3.2.1
C1G2Read = Struct("C1G2Read",
        TLVParameterHeader(341),
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("WordPointer"),
        UBInt16("WordCount"))

# 17.3.1.3.2.2
C1G2Write = Struct("C1G2Write",
        TLVParameterHeader(342),
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("WordPointer"),
        UBInt16("WriteDataWordCount"),
        MetaField("WriteData", lambda ctx: ctx.WriteDataWordCount * 2))

# 17.3.1.3.2.3
C1G2Kill = Struct("C1G2Kill",
        TLVParameterHeader(343),
        UBInt16("OpSpecID"),
        UBInt32("KillPassword"))

# 17.3.1.3.2.4
C1G2Recommission = Struct("C1G2Recommission",
        TLVParameterHeader(357),
        UBInt16("OpSpecID"),
        UBInt32("KillPassword"),
        EmbeddedBitStruct(
            Padding(5),
            Flag("3SB"),
            Flag("2SB"),
            Flag("LSB")))

# 17.3.1.3.2.5.1
C1G2LockPayload = Struct("C1G2LockPayload",
        TLVParameterHeader(345),
        UBInt8("Privilege"), # XXX
        UBInt8("DataField"))

# 17.3.1.3.2.5
C1G2Lock = Struct("C1G2Lock",
        TLVParameterHeader(344),
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        GreedyRange(C1G2LockPayload))

# 17.3.1.3.2.6
C1G2BlockErase = Struct("C1G2BlockErase",
        TLVParameterHeader(346),
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("WordPointer"),
        UBInt16("WordCount"))

# 17.3.1.3.2.7
C1G2BlockWrite = Struct("C1G2BlockWrite",
        TLVParameterHeader(347),
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("WordPointer"),
        UBInt16("WriteDataWordCount"),
        MetaField("WriteData", lambda ctx: ctx.WriteDataWordCount * 2))

# 17.3.1.3.2.8
C1G2BlockPermalock = Struct("C1G2BlockPermalock",
        TLVParameterHeader(358),
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("BlockPointer"),
        UBInt16("BlockMaskWordCount"),
        MetaField("BlockMask", lambda ctx: ctx.WriteDataWordCount * 2))

# 17.3.1.3.2.9
C1G2BlockPermalockStatus = Struct("C1G2BlockPermalockStatus",
        TLVParameterHeader(359),
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("BlockPointer"),
        UBInt16("BlockRange"))

# 17.3.1.3.1
C1G2TagSpec = Struct("C1G2TagSpec",
        TLVParameterHeader(338),
        C1G2TargetTag,
        Optional(C1G2TargetTag))

# 17.2.5.1.1
AccessSpecStopTrigger = Struct("AccessSpecStopTrigger",
        TLVParameterHeader(208),
        Enum(UBInt8("AccessSpecStopTriggerType"),
            Null = 0,
            OperationCount = 1),
        UBInt16("OperationCountValue"))

# 17.2.5.1.3
ClientRequestOpSpec = Struct("ClientRequestOpSpec",
        TLVParameterHeader(210),
        UBInt16("OpSpecID"))

# 17.2.5.1.2
AccessCommand = Struct("AccessCommand",
        TLVParameterHeader(209),
        C1G2TagSpec,

        Union("C1G2OpSpec",
            # XXX default for Union?
            OptionalGreedyRange(C1G2Read),
            OptionalGreedyRange(C1G2Write),
            OptionalGreedyRange(C1G2Kill),
            OptionalGreedyRange(C1G2Recommission),
            OptionalGreedyRange(C1G2Lock),
            OptionalGreedyRange(C1G2BlockErase),
            OptionalGreedyRange(C1G2BlockWrite),
            OptionalGreedyRange(C1G2BlockPermalock),
            OptionalGreedyRange(C1G2BlockPermalockStatus)),

        OptionalGreedyRange(ClientRequestOpSpec),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.7.2
AccessReportSpec = Struct("AccessReportSpec",
        TLVParameterHeader(239),
        Enum(UBInt8("AccessReportTrigger"),
            ROReport = 0,
            EndOfAccessSpec = 1))

# 17.2.7.3.1
EPCData = Struct("EPCData",
        TLVParameterHeader(241),
        UBInt16("EPCLengthBits"),
        MetaField("EPC", lambda ctx: ctx.EPCLengthBits / 8))

# 17.2.7.3.2
EPC96 = Struct("EPC96",
        TVParameterHeader(13),
        StaticField("EPC", 96/8))

# 17.2.7.3.3
ROSpecID = Struct("ROSpecID",
        TVParameterHeader(9),
        UBInt32("ROSpecID"))

# 17.2.7.3.4
SpecIndex = Struct("SpecIndex",
        TVParameterHeader(14),
        UBInt16("SpecIndex"))

# 17.2.7.3.5
InventoryParameterSpecID = Struct("InventoryParameterSpecID",
        TVParameterHeader(10),
        UBInt16("InventoryParameterSpecID"))

# 17.2.7.3.6
AntennaID = Struct("AntennaID",
        TVParameterHeader(1),
        UBInt16("AntennaID"))

# 17.2.7.3.7
PeakRSSI = Struct("PeakRSSI",
        TVParameterHeader(6),
        UBInt8("PeakRSSI"))

# 17.2.7.3.8
ChannelIndex = Struct("ChannelIndex",
        TVParameterHeader(7),
        UBInt16("ChannelIndex"))

# 17.2.7.3.9
FirstSeenTimestampUTC = Struct("FirstSeenTimestampUTC",
        TVParameterHeader(2),
        UBInt64("Microseconds"))

# 17.2.7.3.10
FirstSeenTimestampUptime = Struct("FirstSeenTimestampUptime",
        TVParameterHeader(3),
        UBInt64("Microseconds"))

# 17.2.7.3.11
LastSeenTimestampUTC = Struct("LastSeenTimestampUTC",
        TVParameterHeader(4),
        UBInt64("Microseconds"))

# 17.2.7.3.12
LastSeenTimestampUptime = Struct("LastSeenTimestampUptime",
        TVParameterHeader(5),
        UBInt64("Microseconds"))

# 17.2.7.3.13
TagSeenCount = Struct("TagSeenCount",
        TVParameterHeader(8),
        UBInt16("TagCount"))

# 17.2.7.3.14
ClientRequestOpSpecResult = Struct("ClientRequestOpSpecResult",
        TVParameterHeader(15),
        UBInt16("OpSpecID"))

# 17.2.7.3.15
AccessSpecID = Struct("AccessSpecID",
        TVParameterHeader(16),
        UBInt32("AccessSpecID"))

# 17.3.1.5.7.1
C1G2ReadOpSpecResult = Struct("C1G2ReadOpSpecResult",
        TLVParameterHeader(349),
        Enum(UBInt8("Result"),
            Success = 0,
            NonSpecificTagError = 1,
            NoResponseFromTag = 2,
            NonSpecificReaderError = 3,
            MemoryOverrunError = 4,
            MemoryLockedError = 5,
            IncorrectPasswordError = 6),
        UBInt16("OpSpecID"),
        UBInt16("ReadDataWordCount"),
        MetaField("ReadData", lambda ctx: ctx.ReadDataWordCount * 2))

# 17.3.1.5.7.2
C1G2WriteOpSpecResult = Struct("C1G2WriteOpSpecResult",
        TLVParameterHeader(350),
        Enum(UBInt8("Result"),
            Success = 0,
            TagMemoryOverrunError = 1,
            TagMemoryLockedError = 2,
            InsufficientPower = 3,
            NonSpecificTagError = 4,
            NoResponseFromTag = 5,
            NonSpecificReaderError = 6,
            IncorrectPasswordError = 7),
        UBInt16("OpSpecID"),
        UBInt16("NumWordsWritten"))

# 17.3.1.5.7.3
C1G2KillOpSpecResult = Struct("C1G2KillOpSpecResult",
        TLVParameterHeader(351),
        Enum(UBInt8("Result"),
            Success = 0,
            ZeroKillPasswordError = 1,
            InsufficientPower = 2,
            NonSpecificTagError = 3,
            NoResponseFromTag = 4,
            NonSpecificReaderError = 5,
            IncorrectPasswordError = 6),
        UBInt16("OpSpecID"))

# 17.3.1.5.7.4
C1G2RecommissionOpSpecResult = Struct("C1G2RecommissionOpSpecResult",
        TLVParameterHeader(360),
        Enum(UBInt8("Result"),
            Success = 0,
            InsufficientPower = 1,
            NonSpecificTagError = 2,
            NoResponseFromTag = 3,
            NonSpecificReaderError = 4,
            IncorrectPasswordError = 5,
            TagMemoryOverrunError = 6,
            TagMemoryLockedError = 7),
        UBInt16("OpSpecID"))

# 17.3.1.5.7.5
C1G2LockOpSpecResult = Struct("C1G2LockOpSpecResult",
        TLVParameterHeader(360),
        Enum(UBInt8("Result"),
            Success = 0,
            ZeroKillPasswordError = 1,
            InsufficientPower = 2,
            NonSpecificTagError = 3,
            NoResponseFromTag = 4,
            NonSpecificReaderError = 5,
            IncorrectPasswordError = 6),
        UBInt16("OpSpecID"))

# 17.3.1.5.7.6
C1G2BlockEraseOpSpecResult = Struct("C1G2BlockEraseOpSpecResult",
        TLVParameterHeader(353),
        Enum(UBInt8("Result"),
            Success = 0,
            TagMemoryOverrunError = 1,
            TagMemoryLockedError = 2,
            InsufficientPower = 3,
            NonSpecificTagError = 4,
            NoResponseFromTag = 5,
            NonSpecificReaderError = 6,
            IncorrectPasswordError = 7),
        UBInt16("OpSpecID"))

# 17.3.1.5.7.7
C1G2BlockWriteOpSpecResult = Struct("C1G2BlockWriteOpSpecResult",
        TLVParameterHeader(354),
        Enum(UBInt8("Result"),
            Success = 0,
            TagMemoryOverrunError = 1,
            TagMemoryLockedError = 2,
            InsufficientPower = 3,
            NonSpecificTagError = 4,
            NoResponseFromTag = 5,
            NonSpecificReaderError = 6,
            IncorrectPasswordError = 7),
        UBInt16("OpSpecID"),
        UBInt16("NumWordsWritten"))

# 17.3.1.5.7.8
C1G2BlockPermalockOpSpecResult = Struct("C1G2BlockPermalockOpSpecResult",
        TLVParameterHeader(361),
        Enum(UBInt8("Result"),
            Success = 0,
            InsufficientPower = 1,
            NonSpecificTagError = 2,
            NoResponseFromTag = 3,
            NonSpecificReaderError = 4,
            IncorrectPasswordError = 5,
            TagMemoryOverrunError = 6),
        UBInt16("OpSpecID"))

# 17.3.1.5.7.9
C1G2BlockPermalockStatusOpSpecResult = \
    Struct("C1G2BlockPermalockStatusOpSpecResult",
        TLVParameterHeader(362),
        Enum(UBInt8("Result"),
            Success = 0,
            NonSpecificTagError = 1,
            NoResponseFromTag = 2,
            NonSpecificReaderError = 3,
            IncorrectPasswordError = 4,
            TagMemoryOverrunError = 5),
        UBInt16("OpSpecID"),
        UBInt16("StatusWordCount"),
        MetaField("PermalockStatus", lambda ctx: ctx.StatusWordCount * 2))

OpSpecResult = Struct("OpSpecResult",
        Peek(Enum(UBInt16("TLVType"),
                C1G2ReadOpSpecResult                 = 349,
                C1G2WriteOpSpecResult                = 350,
                C1G2KillOpSpecResult                 = 351,
                C1G2RecommissionOpSpecResult         = 360,
                C1G2LockOpSpecResult                 = 352,
                C1G2BlockEraseOpSpecResult           = 353,
                C1G2BlockWriteOpSpecResult           = 354,
                C1G2BlockPermalockOpSpecResult       = 361,
                C1G2BlockPermalockStatusOpSpecResult = 362,
                ClientRequestOpSpecResult            = 15<<8, # XXX correct?
                )),
        Switch("OpSpecResult",
            lambda ctx: ctx.TLVType, {
            "C1G2ReadOpSpecResult":           C1G2ReadOpSpecResult,
            "C1G2WriteOpSpecResult":          C1G2WriteOpSpecResult,
            "C1G2KillOpSpecResult":           C1G2KillOpSpecResult,
            "C1G2RecommissionOpSpecResult":   C1G2RecommissionOpSpecResult,
            "C1G2LockOpSpecResult":           C1G2LockOpSpecResult,
            "C1G2BlockEraseOpSpecResult":     C1G2BlockEraseOpSpecResult,
            "C1G2BlockWriteOpSpecResult":     C1G2BlockWriteOpSpecResult,
            "C1G2BlockPermalockOpSpecResult": C1G2BlockPermalockOpSpecResult,
            "C1G2BlockPermalockStatusOpSpecResult": \
                C1G2BlockPermalockStatusOpSpecResult,
            "ClientRequestOpSpecResult":      ClientRequestOpSpecResult,
            })
        )

# 17.2.7.3
TagReportData = Struct("TagReportData",
        TLVParameterHeader(240),
        Peek(UBInt8("EPCType")),
        IfThenElse("EPC", lambda ctx: ctx.EPCType == 0x8d, EPC96, EPCData),
        Optional(ROSpecID),
        Optional(SpecIndex),
        Optional(InventoryParameterSpecID),
        Optional(AntennaID),
        Optional(PeakRSSI),
        Optional(ChannelIndex),
        Optional(FirstSeenTimestampUTC),
        Optional(FirstSeenTimestampUptime),
        Optional(LastSeenTimestampUTC),
        Optional(LastSeenTimestampUptime),
        Optional(TagSeenCount),
        OptionalGreedyRange(Struct("AirProtocolTagData",
                # C1G2PC,
                # C1G2XPCW1,
                # C1G2XPCW2, or
                # C1G2CRC
                )),
        Optional(AccessSpecID),
        OptionalGreedyRange(OpSpecResult))

# 17.2.5.1
AccessSpec = Struct("AccessSpec",
        TLVParameterHeader(207),
        UBInt32("AccessSpecID"),
        UBInt16("AntennaID"),
        AirProtocol,
        EmbeddedBitStruct(
            Flag("CurrentState"),
            Alias("C", "CurrentState"),
            Padding(7)),
        UBInt32("ROSpecID"),
        AccessSpecStopTrigger,
        AccessCommand,
        Optional(AccessReportSpec),
        # XXX OptionalGreedyRange(CustomParameter)
        )
