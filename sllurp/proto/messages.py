"""Implementations of LLRP messages from Section 17.1 of the LLRP 1.1 protocol
specification."""

from construct import *
from .common import *
from .params import *

# 17.1.1
GET_SUPPORTED_VERSION = Struct("GET_SUPPORTED_VERSION",
        Embed(MessageHeader(46)))

# 17.1.2
GET_SUPPORTED_VERSION_RESPONSE = Struct("GET_SUPPORTED_VERSION_RESPONSE",
        Embed(MessageHeader(56)),
        UBInt8("CurrentVersion"),
        UBInt8("SupportedVersion"),
        LLRPStatus)

# 17.1.3
SET_PROTOCOL_VERSION = Struct("SET_PROTOCOL_VERSION",
        Embed(MessageHeader(47)),
        UBInt8("ProtocolVersion"))

# 17.1.4
SET_PROTOCOL_VERSION_RESPONSE = Struct("SET_PROTOCOL_VERSION_RESPONSE",
        Embed(MessageHeader(57)),
        LLRPStatus)

# 17.1.5
GET_READER_CAPABILITIES = Struct("GET_READER_CAPABILITIES",
        Embed(MessageHeader(1)),
        UBInt8("RequestedData"), # XXX Enum?
        # XXX OptionalGreedyRange(CustomParameter)
        )

# 17.1.6
GET_READER_CAPABILITIES_RESPONSE = Struct("GET_READER_CAPABILITIES_RESPONSE",
        Embed(MessageHeader(11)),
        LLRPStatus,
        Optional(GeneralDeviceCapabilities),
        Optional(LLRPCapabilities),
        Optional(RegulatoryCapabilities),
        Optional(C1G2LLRPCapabilities))
