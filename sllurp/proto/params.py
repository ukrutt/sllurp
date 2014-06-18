"""Implementations of LLRP parameters from Section 17.2 of the LLRP 1.1 protocol
specification.

Section headers like 17.x.x.x refer to version 1.1 of the LLRP specification.
They often appear out of order in this file because parameters are often nested,
and children must precede their parents."""

from construct import *
from .common import TLVParameterHeader, TVParameterHeader, IntRange, \
     StatusCode, AirProtocol

# mapping of param types to the corresponding decoders
decoderClasses = {}

# mapping of param names to their corresponding encoders
encoderClasses = {}

class LLRPParamStruct (Struct):
    def __init__ (self, name, ty, *subcons, **kw):
        hdr = TLVParameterHeader
        try:
            if kw['tv']:
                hdr = TVParameterHeader
            del kw['tv']
        except KeyError:
            pass
        _subcons = (Embed(hdr(ty)),) + subcons
        Struct.__init__(self, name, *_subcons, **kw)
        self.name = name
        encoderClasses[name] = self
        self.type = ty
        decoderClasses[ty] = self

# 17.2.2
TimestampOrUptime = LLRPParamStruct("TimestampOrUptime", None,
        UBInt64("Microseconds"))

# 17.2.2.1
UTCTimestamp = LLRPParamStruct("UTCTimestamp", 128,
        UBInt64("Microseconds"))

# 17.2.2.2
Uptime = LLRPParamStruct("Uptime", 129,
        UBInt64("Microseconds"))

# 17.2.3.1
GeneralDeviceCapabilities = LLRPParamStruct("GeneralDeviceCapabilities", 137,
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
        GreedyRange(LLRPParamStruct("ReceiveSensitivityTableEntry", 139,
                UBInt16("Index"),
                IntRange(UBInt16("ReceiveSensitivityValue"), 0, 128))),

        # 17.2.3.1.3
        OptionalGreedyRange(LLRPParamStruct("PerAntennaReceiveSensitivityRange",
                149,
                UBInt16("AntennaID"),
                UBInt16("ReceiveSensitivityIndexMin"),
                UBInt16("ReceiveSensitivityIndexMax"))),

        # 17.2.3.1.5
        LLRPParamStruct("GPIOCapabilities", 141,
                UBInt16("NumGPIs"),
                UBInt16("NumGPOs")),

        # 17.2.3.1.4
        GreedyRange(LLRPParamStruct("PerAntennaAirProtocol", 140,
                    UBInt16("AntennaID"),
                    UBInt16("NumProtocols"),
                    Array(lambda ctx: ctx.NumProtocols, AirProtocol))),

        # 17.2.3.1.1
        Optional(LLRPParamStruct("MaximumReceiveSensitivity", 363,
                    UBInt16("MaximumSensitivity")))
        )

# 17.2.3.2
LLRPCapabilities = LLRPParamStruct("LLRPCapabilities", 142,
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
UHFBandCapabilities = LLRPParamStruct("UHFBandCapabilities", 144,

        # 17.2.3.4.1.1
        GreedyRange(LLRPParamStruct("TransmitPowerLevelTableEntry", 145,
                IntRange(UBInt16("Index"), 0, 255),
                UBInt16("TransmitPowerValue"))),

        # 17.2.3.4.1.2
        LLRPParamStruct("FrequencyInformation", 146,
            EmbeddedBitStruct(
                Flag("Hopping"),
                Padding(7)),

            # 17.2.3.4.1.2.1
            OptionalGreedyRange(LLRPParamStruct("FrequencyHopTable", 147,
                    UBInt8("HopTableID"),
                    Padding(1),
                    UBInt16("NumHops"),
                    Array(lambda ctx: ctx.NumHops, UBInt32("Frequency")))),

            # 17.2.3.4.1.2.2
            Optional(LLRPParamStruct("FixedFrequencyTable", 148,
                    UBInt16("NumFrequencies"),
                    Array(lambda ctx: ctx.NumFrequencies,
                        UBInt32("Frequency"))))),

        # 17.3.1.1.2
        GreedyRange(LLRPParamStruct("UHFC1G2RFModeTable", 328,

                    # 17.3.1.1.2.1
                    GreedyRange(LLRPParamStruct("UHFC1G2RFModeTableEntry", 329,
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
        Optional(LLRPParamStruct("RFSurveyFrequencyCapabilities", 365,
                    UBInt32("MinimumFrequency"),
                    UBInt32("MaximumFrequency"))))


# 17.2.3.4
RegulatoryCapabilities = LLRPParamStruct("RegulatoryCapabilities", 143,
        UBInt16("CountryCode"),
        UBInt16("CommunicationsStandard"),
        Optional(UHFBandCapabilities),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.1.1.1.1
PeriodicTriggerValue = LLRPParamStruct("PeriodicTriggerValue", 180,
        UBInt32("Offset"),
        UBInt32("Period"),
        Optional(UTCTimestamp))

# 17.2.4.1.1.1.2
GPITriggerValue = LLRPParamStruct("GPITriggerValue", 181,
        UBInt16("GPIPortNumber"),
        EmbeddedBitStruct(
            Flag("GPIEvent"),
            Alias("E", "GPIEvent"),
            Padding(7)),
        UBInt32("Timeout"))

# 17.2.4.1.1.1
ROSpecStartTrigger = LLRPParamStruct("ROSpecStartTrigger", 179,
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
ROSpecStopTrigger = LLRPParamStruct("ROSpecStopTrigger", 182,
        Enum(UBInt8("ROSpecStopTriggerType"),
            Null = 0,
            Duration = 1,
            GPI = 2),
        UBInt32("DurationTriggerValue"),
        Optional(GPITriggerValue))

# 17.2.4.1.1
ROBoundarySpec = LLRPParamStruct("ROBoundarySpec", 178,
        ROSpecStartTrigger,
        ROSpecStopTrigger)

# 17.2.4.2.1.1
TagObservationTrigger = LLRPParamStruct("TagObservationTrigger", 185,
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
AISpecStopTrigger = LLRPParamStruct("AISpecStopTrigger", 184,
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
RFReceiverSettings = LLRPParamStruct("RFReceiverSettings", 223,
        UBInt16("ReceiveSensitivity"))

# 17.2.6.8
RFTransmitterSettings = LLRPParamStruct("RFTransmitterSettings", 224,
        UBInt16("HopTableID"),
        UBInt16("ChannelIndex"),
        UBInt16("TransmitPower"))

# 17.2.6.9
GPIPortCurrentState = LLRPParamStruct("GPIPortCurrentState", 225,
        UBInt16("GPIPortNumber"),
        EmbeddedBitStruct(
            Flag("GPIConfig"),
            Alias("C", "GPIConfig"),
            Padding(7)),
        Enum(UBInt8("GPIState"),
            Low = 0,
            High = 1,
            Unknown = 2))

# 17.2.6.10
EventsAndReports = LLRPParamStruct("EventsAndReports", 226,
        EmbeddedBitStruct(
            Flag("HoldEventsAndReportsUponReconnect"),
            Alias("H", "HoldEventsAndReportsUponReconnect"),
            Padding(7)))

# 17.3.1.2.1.1.1
C1G2TagInventoryMask = LLRPParamStruct("C1G2TagInventoryMask", 332,
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("Pointer"),
        UBInt16("MaskBitCount"),
        MetaField("TagMask", lambda ctx: ctx.MaskBitCount / 8))

# 17.3.1.2.1.1.2
C1G2TagInventoryStateAwareFilterAction = \
    LLRPParamStruct("C1G2TagInventoryStateAwareFilterAction", 333,
        IntRange(UBInt8("Target"), 0, 4),
        IntRange(UBInt8("Action"), 0, 7))

# 17.3.1.2.1.1.3
C1G2TagInventoryStateUnawareFilterAction = \
    LLRPParamStruct("C1G2TagInventoryStateUnawareFilterAction", 334,
        IntRange(UBInt8("Action"), 0, 5))

# 17.3.1.2.1.1
C1G2Filter = LLRPParamStruct("C1G2Filter", 331,
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
C1G2RFControl = LLRPParamStruct("C1G2RFControl", 335,
        UBInt16("ModeIndex"),
        IntRange(UBInt16("Tari"), 6250, 25000))

# 17.3.1.2.1.3.1
C1G2TagInventoryStateAwareSingulationAction = \
    LLRPParamStruct("C1G2TagInventoryStateAwareSingulationAction", 337,
        EmbeddedBitStruct(
            Flag("I"),
            Flag("S"),
            Flag("S_All"),
            Alias("A", "S_All")))

# 17.3.1.2.1.3
C1G2SingulationControl = LLRPParamStruct("C1G2SingulationControl", 336,
        IntRange(UBInt8("Session"), 0, 3),
        Alias("S", "Session"),
        UBInt16("TagPopulation"),
        UBInt32("TagTransitTime"),
        Optional(C1G2TagInventoryStateAwareSingulationAction))

# 17.3.1.2.1
C1G2InventoryCommand = LLRPParamStruct("C1G2InventoryCommand", 330,
        OptionalGreedyRange(C1G2Filter),
        Optional(C1G2RFControl),
        Optional(C1G2SingulationControl),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.6.5
AntennaProperties = LLRPParamStruct("AntennaProperties", 221,
        EmbeddedBitStruct(
            Flag("Connected"),
            Alias("C", "Connected"),
            Padding(7)),
        UBInt16("AntennaID"),
        SBInt16("AntennaGain"))

# 17.2.6.6
AntennaConfiguration = LLRPParamStruct("AntennaConfiguration", 222,
        UBInt16("AntennaID"),
        Optional(RFReceiverSettings),
        Optional(RFTransmitterSettings),
        OptionalGreedyRange(C1G2InventoryCommand),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.2.2
InventoryParameterSpec = LLRPParamStruct("InventoryParameterSpec", 186,
        UBInt16("InventoryParameterSpecID"),
        AirProtocol,
        OptionalGreedyRange(AntennaConfiguration),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.2
AISpec = LLRPParamStruct("AISpec", 183,
        UBInt16("AntennaCount"),
        GreedyRange(UBInt16("AntennaID")),
        AISpecStopTrigger,
        GreedyRange(InventoryParameterSpec),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.3.1
RFSurveySpecStopTrigger = LLRPParamStruct("RFSurveySpecStopTrigger", 188,
        Enum(UBInt8("StopTriggerType"),
            Null = 0,
            Duration = 1,
            NIterations = 2),
        UBInt32("Duration"),
        UBInt32("N"))

# 17.2.4.3
RFSurveySpec = LLRPParamStruct("RFSurveySpec", 187,
        UBInt16("AntennaID"),
        UBInt32("StartFrequency"),
        UBInt32("EndFrequency"),
        RFSurveySpecStopTrigger,
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.4.4
LoopSpec = LLRPParamStruct("LoopSpec", 355,
        UBInt32("LoopCount"))

# 17.3.1.5.1
C1G2EPCMemorySelector = LLRPParamStruct("C1G2EPCMemorySelector", 348,
        EmbeddedBitStruct(
            Flag("EnableCRC"),
            Alias("C", "EnableCRC"),
            Flag("EnablePCBits"),
            Alias("P", "EnablePCBits"),
            Flag("EnableXPCBits"),
            Alias("X", "EnableXPCBits"),
            Padding(5)))

# 17.2.7.1.1
TagReportContentSelector = LLRPParamStruct("TagReportContentSelector", 238,
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
ROReportSpec = LLRPParamStruct("ROReportSpec", 237,
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
ROSpec = LLRPParamStruct("ROSpec", 177,
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
LLRPStatus = LLRPParamStruct("LLRPStatus", 287,
        StatusCode,
        UBInt16("ErrorDescriptionByteCount"),
        If(lambda ctx: ctx.ErrorDescriptionByteCount,
            String("ErrorDescription",
                lambda ctx: ctx.ErrorDescriptionByteCount)),
        Optional(LLRPParamStruct("FieldError", 288,
            UBInt16("FieldNum"),
            UBInt16("ErrorCode"), # XXX Enum?
            )),
        Optional(LLRPParamStruct("ParameterError", 289,
            UBInt16("ParameterType"),
            UBInt16("ErrorCode"), # XXX Enum?
            ))
        )

# 17.3
C1G2LLRPCapabilities = LLRPParamStruct("C1G2LLRPCapabilities", 327,
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
C1G2TargetTag = LLRPParamStruct("C1G2TargetTag", 339,
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
C1G2Read = LLRPParamStruct("C1G2Read", 341,
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("WordPointer"),
        UBInt16("WordCount"))

# 17.3.1.3.2.2
C1G2Write = LLRPParamStruct("C1G2Write", 342,
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
C1G2Kill = LLRPParamStruct("C1G2Kill", 343,
        UBInt16("OpSpecID"),
        UBInt32("KillPassword"))

# 17.3.1.3.2.4
C1G2Recommission = LLRPParamStruct("C1G2Recommission", 357,
        UBInt16("OpSpecID"),
        UBInt32("KillPassword"),
        EmbeddedBitStruct(
            Padding(5),
            Flag("3SB"),
            Flag("2SB"),
            Flag("LSB")))

# 17.3.1.3.2.5.1
C1G2LockPayload = LLRPParamStruct("C1G2LockPayload", 345,
        UBInt8("Privilege"), # XXX
        UBInt8("DataField"))

# 17.3.1.3.2.5
C1G2Lock = LLRPParamStruct("C1G2Lock", 344,
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        GreedyRange(C1G2LockPayload))

# 17.3.1.3.2.6
C1G2BlockErase = LLRPParamStruct("C1G2BlockErase", 346,
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("WordPointer"),
        UBInt16("WordCount"))

# 17.3.1.3.2.7
C1G2BlockWrite = LLRPParamStruct("C1G2BlockWrite", 347,
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
C1G2BlockPermalock = LLRPParamStruct("C1G2BlockPermalock", 358,
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
C1G2BlockPermalockStatus = LLRPParamStruct("C1G2BlockPermalockStatus", 359,
        UBInt16("OpSpecID"),
        UBInt32("AccessPassword"),
        EmbeddedBitStruct(
            BitField("MemoryBank", 2),
            Alias("MB", "MemoryBank"),
            Padding(6)),
        UBInt16("BlockPointer"),
        UBInt16("BlockRange"))

# 17.3.1.3.1
C1G2TagSpec = LLRPParamStruct("C1G2TagSpec", 338,
        C1G2TargetTag,
        Optional(C1G2TargetTag))

# 17.2.5.1.1
AccessSpecStopTrigger = LLRPParamStruct("AccessSpecStopTrigger", 208,
        Enum(UBInt8("AccessSpecStopTriggerType"),
            Null = 0,
            OperationCount = 1),
        UBInt16("OperationCountValue"))

# 17.2.5.1.3
ClientRequestOpSpec = LLRPParamStruct("ClientRequestOpSpec", 210,
        UBInt16("OpSpecID"))

# XXX make into LLRPParamStruct?
OpSpec = Struct("OpSpec",
        Peek(Enum(UBInt16("TLVType"),
                C1G2Read                 = 349,
                C1G2Write                = 350,
                C1G2Kill                 = 351,
                C1G2Recommission         = 360,
                C1G2Lock                 = 352,
                C1G2BlockErase           = 353,
                C1G2BlockWrite           = 354,
                C1G2BlockPermalock       = 361,
                C1G2BlockPermalockStatus = 362,
                ClientRequest            = 210,
                )),
        Switch("OpSpec",
            lambda ctx: ctx.TLVType, {
            "C1G2Read":                 C1G2Read,
            "C1G2Write":                C1G2Write,
            "C1G2Kill":                 C1G2Kill,
            "C1G2Recommission":         C1G2Recommission,
            "C1G2Lock":                 C1G2Lock,
            "C1G2BlockErase":           C1G2BlockErase,
            "C1G2BlockWrite":           C1G2BlockWrite,
            "C1G2BlockPermalock":       C1G2BlockPermalock,
            "C1G2BlockPermalockStatus": C1G2BlockPermalockStatus,
            "ClientRequestOpSpec":      ClientRequestOpSpec,
            })
        )

# 17.2.5.1.2
AccessCommand = LLRPParamStruct("AccessCommand", 209,
        C1G2TagSpec,
        OptionalGreedyRange(OpSpec),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.6.1
LLRPConfigurationStateValue = LLRPParamStruct("LLRPConfigurationStateValue", 217,
        UBInt32("LLRPConfigurationStateValue"))

# 17.2.6.2
Identification = LLRPParamStruct("Identification", 218,
        Enum(UBInt8("IDType"),
            MACAddress = 0,
            EPC = 1),
        UBInt16("ByteCount"),
        MetaField("ReaderID", lambda ctx: ctx.ByteCount))

# 17.2.6.3
GPOWriteData = LLRPParamStruct("GPOWriteData", 219,
        UBInt16("GPOPortNumber"),
        EmbeddedBitStruct(
            Flag("GPOData"),
            Alias("W", "GPOData"),
            Padding(7)))

# 17.2.6.4
KeepaliveSpec = LLRPParamStruct("KeepaliveSpec", 220,
        Enum(UBInt8("KeepaliveTriggerType"),
            Null = 0,
            Periodic = 1),
        UBInt32("TimeInterval"))

# 17.2.7.2
AccessReportSpec = LLRPParamStruct("AccessReportSpec", 239,
        Enum(UBInt8("AccessReportTrigger"),
            ROReport = 0,
            EndOfAccessSpec = 1))

# 17.2.7.3.1
EPCData = LLRPParamStruct("EPCData", 241,
        UBInt16("EPCLengthBits"),
        MetaField("EPC", lambda ctx: ctx.EPCLengthBits / 8))

# 17.2.7.3.2
EPC96 = LLRPParamStruct("EPC96", 13,
        StaticField("EPC", 96/8),
        tv=True)

# 17.2.7.3.3
ROSpecID = LLRPParamStruct("ROSpecID", 9,
        UBInt32("ROSpecID"),
        tv=True)

# 17.2.7.3.4
SpecIndex = LLRPParamStruct("SpecIndex", 14,
        UBInt16("SpecIndex"),
        tv=True)

# 17.2.7.3.5
InventoryParameterSpecID = LLRPParamStruct("InventoryParameterSpecID", 10,
        UBInt16("InventoryParameterSpecID"),
        tv=True)

# 17.2.7.3.6
AntennaID = LLRPParamStruct("AntennaID", 1,
        UBInt16("AntennaID"),
        tv=True)

# 17.2.7.3.7
PeakRSSI = LLRPParamStruct("PeakRSSI", 6,
        SBInt8("PeakRSSI"),
        tv=True)

# 17.2.7.3.8
ChannelIndex = LLRPParamStruct("ChannelIndex", 7,
        UBInt16("ChannelIndex"),
        tv=True)

# 17.2.7.3.9
FirstSeenTimestampUTC = LLRPParamStruct("FirstSeenTimestampUTC", 2,
        UBInt64("Microseconds"),
        tv=True)

# 17.2.7.3.10
FirstSeenTimestampUptime = LLRPParamStruct("FirstSeenTimestampUptime", 3,
        UBInt64("Microseconds"),
        tv=True)

# 17.2.7.3.11
LastSeenTimestampUTC = LLRPParamStruct("LastSeenTimestampUTC", 4,
        UBInt64("Microseconds"),
        tv=True)

# 17.2.7.3.12
LastSeenTimestampUptime = LLRPParamStruct("LastSeenTimestampUptime", 5,
        UBInt64("Microseconds"),
        tv=True)

# 17.2.7.3.13
TagSeenCount = LLRPParamStruct("TagSeenCount", 8,
        UBInt16("TagCount"),
        tv=True)

# 17.2.7.3.14
ClientRequestOpSpecResult = LLRPParamStruct("ClientRequestOpSpecResult", 15,
        UBInt16("OpSpecID"),
        tv=True)

# 17.2.7.3.15
AccessSpecID = LLRPParamStruct("AccessSpecID", 16,
        UBInt32("AccessSpecID"),
        tv=True)

# 17.2.7.4.1
FrequencyRSSILevelEntry = LLRPParamStruct("FrequencyRSSILevelEntry", 243,
        UBInt32("Frequency"),
        UBInt32("Bandwidth"),
        SBInt8("AverageRSSI"),
        SBInt8("PeakRSSI"),
        TimestampOrUptime)

# 17.2.7.4
RFSurveyReportData = LLRPParamStruct("RFSurveyReportData", 242,
        Optional(ROSpecID),
        Optional(SpecIndex),
        GreedyRange(FrequencyRSSILevelEntry),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.7.5.1
EventNotificationState = LLRPParamStruct("EventNotificationState", 245,
        Enum(UBInt16("EventType"),
            HoppedToNextChannel = 0,
            GPIEvent = 1,
            ROSpecEvent = 2,
            ReportBufferFillWarning = 3,
            ReaderExceptionEvent = 4,
            RFSurveyEvent = 5,
            AISpecEvent = 6,
            AISpecEventWithSingulationDetails = 7,
            AntennaEvent = 8,
            SpecLoopEvent = 9),
        EmbeddedBitStruct(
            Flag("NotificationState"),
            Alias("S", "NotificationState"),
            Padding(7)))

# 17.2.7.5
ReaderEventNotificationSpec = LLRPParamStruct("ReaderEventNotificationSpec",
        244,
        GreedyRange(EventNotificationState))

# 17.2.7.6.1
HoppingEvent = LLRPParamStruct("HoppingEvent", 247,
        UBInt16("HopTableID"),
        UBInt16("NextChannelIndex"))

# 17.2.7.6.2
GPIEvent = LLRPParamStruct("GPIEvent", 248,
        UBInt16("GPIPortNumber"),
        EmbeddedBitStruct(
            Flag("GPIEvent"),
            Alias("E", "GPIEvent"),
            Padding(7)))

# 17.2.7.6.3
ROSpecEvent = LLRPParamStruct("ROSpecEvent", 249,
        Enum(UBInt8("EventType"),
            StartOfROSpec = 0,
            EndOfROSpec = 1,
            PreemptionOfROSpec = 2),
        UBInt32("ROSpecID"),
        UBInt32("PreemptingROSpecID"))

# 17.2.7.6.4
ReportBufferLevelWarningEvent = LLRPParamStruct("ReportBufferLevelWarningEvent", 250,
        IntRange(UBInt8("ReportBufferPercentageFull"), 0, 100))

# 17.2.7.6.5
ReportBufferOverflowErrorEvent = LLRPParamStruct("ReportBufferOverflowErrorEvent", 251)

# 17.2.7.6.6.1
OpSpecID = LLRPParamStruct("OpSpecID", 17,
        UBInt16("OpSpecID"),
        tv=True)

# 17.2.7.6.6
ReaderExceptionEvent = LLRPParamStruct("ReaderExceptionEvent", 252,
        UBInt16("MessageStringByteCount"),
        MetaField("Message", lambda ctx: ctx.MessageStringByteCount),
        Optional(ROSpecID),
        Optional(SpecIndex),
        Optional(InventoryParameterSpecID),
        Optional(AntennaID),
        Optional(AccessSpecID),
        Optional(OpSpecID),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.2.7.6.7
RFSurveyEvent = LLRPParamStruct("RFSurveyEvent", 253,
        Enum(UBInt8("EventType"),
            StartOfRFSurvey = 0,
            EndOfRFSurvey = 1),
        UBInt32("ROSpecID"),
        UBInt16("SpecIndex"))

# 17.3.1.5.6
C1G2SingulationDetails = LLRPParamStruct("C1G2SingulationDetails", 18,
        UBInt16("NumCollisionSlots"),
        UBInt16("NumEmptySlots"),
        tv=True)

# 17.2.7.6.8
AISpecEvent = LLRPParamStruct("AISpecEvent", 254,
        Enum(UBInt8("EventType"),
            EndOfAISpec = 0),
        UBInt32("ROSpecID"),
        UBInt16("SpecIndex"),
        Optional(C1G2SingulationDetails))

# 17.2.7.6.9
AntennaEvent = LLRPParamStruct("AntennaEvent", 255,
        Enum(UBInt8("EventType"),
            AntennaDisconnected = 0,
            AntennaConnected = 1),
        UBInt16("AntennaID"))

# 17.2.7.6.10
ConnectionAttemptEvent = LLRPParamStruct("ConnectionAttemptEvent", 256,
        Enum(UBInt16("Status"),
            Success = 0,
            Failed_ReaderConnectionAlreadyExists = 1,
            Failed_ClientConnectionAlreadyExists = 2,
            Failed_OtherReason = 3,
            AnotherConnectionAttempted = 4))

# 17.2.7.6.11
ConnectionCloseEvent = LLRPParamStruct("ConnectionCloseEvent", 257)

# 17.2.7.6.12
SpecLoopEvent = LLRPParamStruct("SpecLoopEvent", 356,
        UBInt32("ROSpecID"),
        UBInt32("LoopCount"))

# 17.2.7.6
ReaderEventNotificationData = LLRPParamStruct("ReaderEventNotificationData", 246,
        TimestampOrUptime,
        Optional(HoppingEvent),
        Optional(GPIEvent),
        Optional(ROSpecEvent),
        Optional(ReportBufferLevelWarningEvent),
        Optional(ReportBufferOverflowErrorEvent),
        Optional(ReaderExceptionEvent),
        Optional(RFSurveyEvent),
        Optional(AISpecEvent),
        Optional(AntennaEvent),
        Optional(ConnectionAttemptEvent),
        Optional(ConnectionCloseEvent),
        Optional(SpecLoopEvent),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.3.1.5.7.1
C1G2ReadOpSpecResult = LLRPParamStruct("C1G2ReadOpSpecResult", 349,
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
C1G2WriteOpSpecResult = LLRPParamStruct("C1G2WriteOpSpecResult", 350,
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
C1G2KillOpSpecResult = LLRPParamStruct("C1G2KillOpSpecResult", 351,
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
C1G2RecommissionOpSpecResult = LLRPParamStruct("C1G2RecommissionOpSpecResult", 360,
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
C1G2LockOpSpecResult = LLRPParamStruct("C1G2LockOpSpecResult", 360,
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
C1G2BlockEraseOpSpecResult = LLRPParamStruct("C1G2BlockEraseOpSpecResult", 353,
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
C1G2BlockWriteOpSpecResult = LLRPParamStruct("C1G2BlockWriteOpSpecResult", 354,
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
C1G2BlockPermalockOpSpecResult = LLRPParamStruct("C1G2BlockPermalockOpSpecResult", 361,
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
    LLRPParamStruct("C1G2BlockPermalockStatusOpSpecResult", 362,
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

# XXX write as LLRPParamStruct?
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

# 17.2.5.1.3.1
ClientRequestResponse = LLRPParamStruct("ClientRequestResponse", 211,
        UBInt32("AccessSpecID"),
        Peek(UBInt8("EPCType")),
        IfThenElse("EPC", lambda ctx: ctx.EPCType == 0x8d, EPC96, EPCData),
        OpSpec)

# 17.2.7.3
TagReportData = LLRPParamStruct("TagReportData", 240,
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
        OptionalGreedyRange(UBInt16("AirProtocolTagData")),
        Optional(AccessSpecID),
        OptionalGreedyRange(OpSpecResult))

# 17.2.5.1
AccessSpec = LLRPParamStruct("AccessSpec", 207,
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
