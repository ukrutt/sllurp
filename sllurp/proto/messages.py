"""Implementations of LLRP messages from Section 17.1 of the LLRP 1.1 protocol
specification."""

from construct import *
from .common import MessageHeader, DecodingError, EncodingError
from . import params

# mapping of message types to the corresponding decoders
decoderClasses = {}

# mapping of message names to their corresponding encoders
encoderClasses = {}

class LLRPMessageStruct (Struct):
    def __init__ (self, name, ty, *subcons, **kw):
        _subcons = (Embed(MessageHeader(ty)),) + subcons
        Struct.__init__(self, name, *_subcons, **kw)
        self.name = name
        encoderClasses[name] = self
        self.type = ty
        decoderClasses[ty] = self

# 17.1.1
GET_SUPPORTED_VERSION = LLRPMessageStruct("GET_SUPPORTED_VERSION", 46)

# 17.1.2
GET_SUPPORTED_VERSION_RESPONSE = LLRPMessageStruct( \
        "GET_SUPPORTED_VERSION_RESPONSE", 56,
        UBInt8("CurrentVersion"),
        UBInt8("SupportedVersion"),
        params.LLRPStatus)

# 17.1.3
SET_PROTOCOL_VERSION = LLRPMessageStruct("SET_PROTOCOL_VERSION", 47,
        UBInt8("ProtocolVersion"))

# 17.1.4
SET_PROTOCOL_VERSION_RESPONSE = LLRPMessageStruct( \
        "SET_PROTOCOL_VERSION_RESPONSE", 57,
        params.LLRPStatus)

# 17.1.5
GET_READER_CAPABILITIES = LLRPMessageStruct("GET_READER_CAPABILITIES", 1,
        UBInt8("RequestedData"), # XXX Enum?
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.6
GET_READER_CAPABILITIES_RESPONSE = LLRPMessageStruct( \
        "GET_READER_CAPABILITIES_RESPONSE", 11,
        params.LLRPStatus,
        Optional(params.GeneralDeviceCapabilities),
        Optional(params.LLRPCapabilities),
        Optional(params.RegulatoryCapabilities),
        Optional(params.C1G2LLRPCapabilities))

# 17.1.7
ADD_ROSPEC = LLRPMessageStruct("ADD_ROSPEC", 20,
        params.ROSpec)

# 17.1.8
ADD_ROSPEC_RESPONSE = LLRPMessageStruct("ADD_ROSPEC_RESPONSE", 30,
        params.LLRPStatus)

# 17.1.9
DELETE_ROSPEC = LLRPMessageStruct("DELETE_ROSPEC", 21,
        UBInt32("ROSpecID"))

# 17.1.10
DELETE_ROSPEC_RESPONSE = LLRPMessageStruct("DELETE_ROSPEC_RESPONSE", 31,
        params.LLRPStatus)

# 17.1.11
START_ROSPEC = LLRPMessageStruct("START_ROSPEC", 22,
        UBInt32("ROSpecID"))

# 17.1.12
START_ROSPEC_RESPONSE = LLRPMessageStruct("START_ROSPEC_RESPONSE", 32,
        params.LLRPStatus)

# 17.1.13
STOP_ROSPEC = LLRPMessageStruct("STOP_ROSPEC", 23,
        UBInt32("ROSpecID"))

# 17.1.14
STOP_ROSPEC_RESPONSE = LLRPMessageStruct("STOP_ROSPEC_RESPONSE", 33,
        params.LLRPStatus)

# 17.1.15
ENABLE_ROSPEC = LLRPMessageStruct("ENABLE_ROSPEC", 24,
        UBInt32("ROSpecID"))

# 17.1.16
ENABLE_ROSPEC_RESPONSE = LLRPMessageStruct("ENABLE_ROSPEC_RESPONSE", 34,
        params.LLRPStatus)

# 17.1.17
DISABLE_ROSPEC = LLRPMessageStruct("DISABLE_ROSPEC", 25,
        UBInt32("ROSpecID"))

# 17.1.18
DISABLE_ROSPEC_RESPONSE = LLRPMessageStruct("DISABLE_ROSPEC_RESPONSE", 35,
        params.LLRPStatus)

# 17.1.19
GET_ROSPECS = LLRPMessageStruct("GET_ROSPECS", 26)

# 17.1.20
GET_ROSPECS_RESPONSE = LLRPMessageStruct("GET_ROSPECS_RESPONSE", 36,
        params.LLRPStatus,
        OptionalGreedyRange(params.ROSpec))

# 17.1.21
ADD_ACCESSSPEC = LLRPMessageStruct("ADD_ACCESSSPEC", 40,
        params.AccessSpec)

# 17.1.22
ADD_ACCESSSPEC_RESPONSE = LLRPMessageStruct("ADD_ACCESSSPEC_RESPONSE", 50,
        params.LLRPStatus)

# 17.1.23
DELETE_ACCESSSPEC = LLRPMessageStruct("DELETE_ACCESSSPEC", 41,
        UBInt32("AccessSpecID"))

# 17.1.24
DELETE_ACCESSSPEC_RESPONSE = LLRPMessageStruct("DELETE_ACCESSSPEC_RESPONSE", 51,
        params.LLRPStatus)

# 17.1.25
ENABLE_ACCESSSPEC = LLRPMessageStruct("ENABLE_ACCESSSPEC", 42,
        UBInt32("AccessSpecID"))

# 17.1.26
ENABLE_ACCESSSPEC_RESPONSE = LLRPMessageStruct("ENABLE_ACCESSSPEC_RESPONSE", 52,
        params.LLRPStatus)

# 17.1.27
DISABLE_ACCESSSPEC = LLRPMessageStruct("DISABLE_ACCESSSPEC", 43,
        UBInt32("AccessSpecID"))

# 17.1.28
DISABLE_ACCESSSPEC_RESPONSE = LLRPMessageStruct("DISABLE_ACCESSSPEC_RESPONSE",
        53,
        params.LLRPStatus)

# 17.1.29
GET_ACCESSSPECS = LLRPMessageStruct("GET_ACCESSSPECS", 44)

# 17.1.30
GET_ACCESSSPECS_RESPONSE = LLRPMessageStruct("GET_ACCESSSPECS_RESPONSE", 54,
        params.LLRPStatus,
        OptionalGreedyRange(params.AccessSpec))

# 17.1.31
CLIENT_REQUEST_OP = LLRPMessageStruct("CLIENT_REQUEST_OP", 45,
        params.TagReportData)

# 17.1.32
CLIENT_REQUEST_OP_RESPONSE = LLRPMessageStruct("CLIENT_REQUEST_OP_RESPONSE", 55,
        params.ClientRequestResponse)

# 17.1.33
GET_REPORT = LLRPMessageStruct("GET_REPORT", 60)

# 17.1.34
RO_ACCESS_REPORT = LLRPMessageStruct("RO_ACCESS_REPORT", 61,
        OptionalGreedyRange(params.TagReportData),
        OptionalGreedyRange(params.RFSurveyReportData),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.35
KEEPALIVE = LLRPMessageStruct("KEEPALIVE", 62)

# 17.1.36
KEEPALIVE_ACK = LLRPMessageStruct("KEEPALIVE_ACK", 72)

# 17.1.37
READER_EVENT_NOTIFICATION = LLRPMessageStruct("READER_EVENT_NOTIFICATION", 63,
        params.ReaderEventNotificationData)

# 17.1.38
ENABLE_EVENTS_AND_REPORTS = LLRPMessageStruct("ENABLE_EVENTS_AND_REPORTS", 64)

# 17.1.39
ERROR_MESSAGE = LLRPMessageStruct("ERROR_MESSAGE", 100,
        params.LLRPStatus)

# 17.1.40
GET_READER_CONFIG = LLRPMessageStruct("GET_READER_CONFIG", 2,
        UBInt16("AntennaID"),
        UBInt8("RequestedData"),
        UBInt16("GPIPortNum"),
        UBInt16("GPOPortNum"),
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.41
GET_READER_CONFIG_RESPONSE = LLRPMessageStruct("GET_READER_CONFIG_RESPONSE", 12,
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
SET_READER_CONFIG = LLRPMessageStruct("SET_READER_CONFIG", 3,
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
SET_READER_CONFIG_RESPONSE = LLRPMessageStruct("SET_READER_CONFIG_RESPONSE", 13,
        params.LLRPStatus)

# 17.1.44
CLOSE_CONNECTION = LLRPMessageStruct("CLOSE_CONNECTION", 14)

# 17.1.45
CLOSE_CONNECTION_RESPONSE = LLRPMessageStruct("CLOSE_CONNECTION_RESPONSE", 4,
        params.LLRPStatus)

# 17.1.46
# CUSTOM_MESSAGE not supported.

def getDecoderForType (ty):
    try:
        return decoderClasses[ty]
    except KeyError:
        raise DecodingError('no decoder for message type {}'.format(ty))

def getEncoderForName (name):
    try:
        return encoderClasses[name]
    except KeyError:
        raise EncodingError('no encoder for {} messages'.format(name))
