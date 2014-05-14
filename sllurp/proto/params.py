"""Implementations of LLRP parameters from Section 17.2 of the LLRP 1.1 protocol
specification."""

from construct import *
from .common import *

# 17.2.8.1
LLRPStatus = Struct("LLRPStatus",
        TLVParameterHeader(287),
        UBInt16("StatusCode"),
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
                UBInt16("ReceiveSensitivityValue"))),

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
                    Array(lambda ctx: ctx.NumProtocols, UBInt8("ProtocolID")))),

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
        UBInt8("MaxPriorityLevelSupported"),
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
                UBInt16("Index"),
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
                                Flag("DR"),
                                Flag("EPCHAGT&CConformance"),
                                Padding(6)),
                            UBInt8("Mod"),
                            UBInt8("FLM"),
                            UBInt8("M"),
                            UBInt32("BDR"),
                            UBInt32("PIE"),
                            UBInt32("MinTari"),
                            UBInt32("MaxTari"),
                            UBInt32("StepTari"))))),

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
