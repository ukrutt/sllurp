"""Implementations of LLRP messages from Section 17.1 of the LLRP 1.1 protocol
specification."""

from construct import *
from .common import MessageHeader
from . import params

# 17.1.1
GET_SUPPORTED_VERSION = Struct("GET_SUPPORTED_VERSION",
        Embed(MessageHeader(46)))

# 17.1.2
GET_SUPPORTED_VERSION_RESPONSE = Struct("GET_SUPPORTED_VERSION_RESPONSE",
        Embed(MessageHeader(56)),
        UBInt8("CurrentVersion"),
        UBInt8("SupportedVersion"),
        params.LLRPStatus)

# 17.1.3
SET_PROTOCOL_VERSION = Struct("SET_PROTOCOL_VERSION",
        Embed(MessageHeader(47)),
        UBInt8("ProtocolVersion"))

# 17.1.4
SET_PROTOCOL_VERSION_RESPONSE = Struct("SET_PROTOCOL_VERSION_RESPONSE",
        Embed(MessageHeader(57)),
        params.LLRPStatus)

# 17.1.5
GET_READER_CAPABILITIES = Struct("GET_READER_CAPABILITIES",
        Embed(MessageHeader(1)),
        UBInt8("RequestedData"), # XXX Enum?
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.6
GET_READER_CAPABILITIES_RESPONSE = Struct("GET_READER_CAPABILITIES_RESPONSE",
        Embed(MessageHeader(11)),
        params.LLRPStatus,
        Optional(params.GeneralDeviceCapabilities),
        Optional(params.LLRPCapabilities),
        Optional(params.RegulatoryCapabilities),
        Optional(params.C1G2LLRPCapabilities))

# 17.1.7
ADD_ROSPEC = Struct("ADD_ROSPEC",
        Embed(MessageHeader(20)),
        params.ROSpec)

# 17.1.8
ADD_ROSPEC_RESPONSE = Struct("ADD_ROSPEC_RESPONSE",
        Embed(MessageHeader(30)),
        params.LLRPStatus)

# 17.1.9
DELETE_ROSPEC = Struct("DELETE_ROSPEC",
        Embed(MessageHeader(21)),
        UBInt32("ROSpecID"))

# 17.1.10
DELETE_ROSPEC_RESPONSE = Struct("DELETE_ROSPEC_RESPONSE",
        Embed(MessageHeader(31)),
        params.LLRPStatus)

# 17.1.11
START_ROSPEC = Struct("START_ROSPEC",
        Embed(MessageHeader(22)),
        UBInt32("ROSpecID"))

# 17.1.12
START_ROSPEC_RESPONSE = Struct("START_ROSPEC_RESPONSE",
        Embed(MessageHeader(32)),
        params.LLRPStatus)

# 17.1.13
STOP_ROSPEC = Struct("STOP_ROSPEC",
        Embed(MessageHeader(23)),
        UBInt32("ROSpecID"))

# 17.1.14
STOP_ROSPEC_RESPONSE = Struct("STOP_ROSPEC_RESPONSE",
        Embed(MessageHeader(33)),
        params.LLRPStatus)

# 17.1.15
ENABLE_ROSPEC = Struct("ENABLE_ROSPEC",
        Embed(MessageHeader(24)),
        UBInt32("ROSpecID"))

# 17.1.16
ENABLE_ROSPEC_RESPONSE = Struct("ENABLE_ROSPEC_RESPONSE",
        Embed(MessageHeader(34)),
        params.LLRPStatus)

# 17.1.17
DISABLE_ROSPEC = Struct("DISABLE_ROSPEC",
        Embed(MessageHeader(25)),
        UBInt32("ROSpecID"))

# 17.1.18
DISABLE_ROSPEC_RESPONSE = Struct("DISABLE_ROSPEC_RESPONSE",
        Embed(MessageHeader(35)),
        params.LLRPStatus)

# 17.1.19
GET_ROSPECS = Struct("GET_ROSPECS",
        Embed(MessageHeader(26)))

# 17.1.20
GET_ROSPECS_RESPONSE = Struct("GET_ROSPECS_RESPONSE",
        Embed(MessageHeader(36)),
        params.LLRPStatus,
        OptionalGreedyRange(params.ROSpec))

# 17.1.21
ADD_ACCESSSPEC = Struct("ADD_ACCESSSPEC",
        Embed(MessageHeader(40)),
        params.AccessSpec)

# 17.1.22
ADD_ACCESSSPEC_RESPONSE = Struct("ADD_ACCESSSPEC_RESPONSE",
        Embed(MessageHeader(50)),
        params.LLRPStatus)

# 17.1.23
DELETE_ACCESSSPEC = Struct("DELETE_ACCESSSPEC",
        Embed(MessageHeader(41)),
        UBInt32("AccessSpecID"))

# 17.1.24
DELETE_ACCESSSPEC_RESPONSE = Struct("DELETE_ACCESSSPEC_RESPONSE",
        Embed(MessageHeader(51)),
        params.LLRPStatus)

# 17.1.25
ENABLE_ACCESSSPEC = Struct("ENABLE_ACCESSSPEC",
        Embed(MessageHeader(42)),
        UBInt32("AccessSpecID"))

# 17.1.26
ENABLE_ACCESSSPEC_RESPONSE = Struct("ENABLE_ACCESSSPEC_RESPONSE",
        Embed(MessageHeader(52)),
        params.LLRPStatus)

# 17.1.27
DISABLE_ACCESSSPEC = Struct("DISABLE_ACCESSSPEC",
        Embed(MessageHeader(43)),
        UBInt32("AccessSpecID"))

# 17.1.28
DISABLE_ACCESSSPEC_RESPONSE = Struct("DISABLE_ACCESSSPEC_RESPONSE",
        Embed(MessageHeader(53)),
        params.LLRPStatus)

# 17.1.29
GET_ACCESSSPECS = Struct("GET_ACCESSSPECS",
        Embed(MessageHeader(44)))

# 17.1.30
GET_ACCESSSPECS_RESPONSE = Struct("GET_ACCESSSPECS_RESPONSE",
        Embed(MessageHeader(54)),
        params.LLRPStatus,
        OptionalGreedyRange(params.AccessSpec))

# 17.1.31
CLIENT_REQUEST_OP = Struct("CLIENT_REQUEST_OP",
        Embed(MessageHeader(45)),
        params.TagReportData)

# 17.1.32
CLIENT_REQUEST_OP_RESPONSE = Struct("CLIENT_REQUEST_OP_RESPONSE",
        Embed(MessageHeader(55)),
        params.ClientRequestResponse)

# 17.1.33
GET_REPORT = Struct("GET_REPORT",
        Embed(MessageHeader(60)))

# 17.1.34
RO_ACCESS_REPORT = Struct("RO_ACCESS_REPORT",
        Embed(MessageHeader(61)),
        OptionalGreedyRange(params.TagReportData),
        OptionalGreedyRange(params.RFSurveyReportData),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.35
KEEPALIVE = Struct("KEEPALIVE",
        Embed(MessageHeader(62)))

# 17.1.36
KEEPALIVE_ACK = Struct("KEEPALIVE_ACK",
        Embed(MessageHeader(72)))

# 17.1.37
READER_EVENT_NOTIFICATION = Struct("READER_EVENT_NOTIFICATION",
        Embed(MessageHeader(63)),
        params.ReaderEventNotificationData)

# 17.1.38
ENABLE_EVENTS_AND_REPORTS = Struct("ENABLE_EVENTS_AND_REPORTS",
        Embed(MessageHeader(64)))

# 17.1.39
ERROR_MESSAGE = Struct("ERROR_MESSAGE",
        Embed(MessageHeader(100)),
        params.LLRPStatus)

# 17.1.40
GET_READER_CONFIG = Struct("GET_READER_CONFIG",
        Embed(MessageHeader(2)),
        UBInt16("AntennaID"),
        UBInt8("RequestedData"),
        UBInt16("GPIPortNum"),
        UBInt16("GPOPortNum"),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.41
GET_READER_CONFIG_RESPONSE = Struct("GET_READER_CONFIG_RESPONSE",
        Embed(MessageHeader(12)),
        params.LLRPStatus,
        Optional(params.Identification),
        OptionalGreedyRange(params.AntennaProperties),
        OptionalGreedyRange(params.AntennaConfiguration),
        Optional(params.ReaderEventNotificationSpec),
        Optional(params.ROReportSpec),
        Optional(params.AccessReportSpec),
        Optional(params.LLRPConfigurationStateValue),
        Optional(params.KeepaliveSpec),
        OptionalGreedyRange(params.GPIPortCurrentState),
        OptionalGreedyRange(params.GPOWriteData),
        Optional(params.EventsAndReports),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.42
SET_READER_CONFIG = Struct("SET_READER_CONFIG",
        Embed(MessageHeader(3)),
        EmbeddedBitStruct(
            Flag("ResetToFactoryDefaults"),
            Alias("R", "ResetToFactoryDefaults"),
            Padding(7)),
        Optional(params.ReaderEventNotificationSpec),
        OptionalGreedyRange(params.AntennaProperties),
        OptionalGreedyRange(params.AntennaConfiguration),
        Optional(params.ROReportSpec),
        Optional(params.AccessReportSpec),
        Optional(params.KeepaliveSpec),
        OptionalGreedyRange(params.GPOWriteData),
        OptionalGreedyRange(params.GPIPortCurrentState),
        Optional(params.EventsAndReports),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.43
SET_READER_CONFIG_RESPONSE = Struct("SET_READER_CONFIG_RESPONSE",
        Embed(MessageHeader(13)),
        params.LLRPStatus)

# 17.1.44
CLOSE_CONNECTION = Struct("CLOSE_CONNECTION",
        Embed(MessageHeader(14)))

# 17.1.45
CLOSE_CONNECTION_RESPONSE = Struct("CLOSE_CONNECTION_RESPONSE",
        Embed(MessageHeader(4)),
        params.LLRPStatus)

# 17.1.46
# CUSTOM_MESSAGE not supported.
