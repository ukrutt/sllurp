"""Structures used throughout LLRP messages and parameters."""

from construct import *

class IntRange (Validator):
    def __init__ (self, subcon, _min, _max):
        Validator.__init__(self, subcon)
        self._min = _min
        self._max = _max
    def _validate (self, obj, context):
        return (obj >= self._min and obj <= self._max)

# 17.1
def MessageHeader (msgType):
    assert msgType > 0
    assert msgType < 2**10
    return Struct("MessageHeader",
            EmbeddedBitStruct(
                Padding(3),
                BitField("Version", 3),
                Const(BitField("Type", 10), msgType)),
            UBInt32("Length"),            # XXX dynamically compute?
            UBInt32("ID"))

# 17.2.1.1
def TLVParameterHeader (paramType=None):
    if paramType:
        assert paramType > 127
        assert paramType < 1024
    return Struct("TLVParameterHeader",
            EmbeddedBitStruct(
                Const(Bit("TV"), 0),
                Padding(5),
                paramType and Const(BitField("Type", 10), paramType) \
                          or        BitField("Type", 10)),
            UBInt16("Length"))            # XXX dynamically compute?

# 17.2.1.2
def TVParameterHeader (paramType=None):
    if paramType:
        assert paramType > 0
        assert paramType < 128
    return BitStruct("TVParameterHeader",
            Const(Bit("TV"), 1),
            paramType and Const(BitField("Type", 7), paramType) \
                      or        BitField("Type", 7))

# 15.2.1
StatusCode = Enum(UBInt16("StatusCode"),
        M_Success = 0,
        M_ParameterError = 100,
        M_FieldError = 101,
        M_UnexpectedParameter = 102,
        M_MissingParameter = 103,
        M_DuplicateParameter = 104,
        M_OverflowParameter = 105,
        M_OverflowField = 106,
        M_UnknownParameter = 107,
        M_UnknownField = 108,
        M_UnsupportedMessage = 109,
        M_UnsupportedVersion = 110,
        M_UnsupportedParameter = 111,
        M_UnexpectedMessage = 112,
        P_ParameterError = 200,
        P_FieldError = 201,
        P_UnexpectedParameter = 202,
        P_MissingParameter = 203,
        P_DuplicateParameter = 204,
        P_OverflowParameter = 205,
        P_OverflowField = 206,
        P_UnknownParameter = 207,
        P_UnknownField = 208,
        P_UnsupportedParameter = 209,
        A_Invalid = 300,
        A_OutOfRange = 301,
        R_DeviceError = 401)

# 7.1.4 Table 4
AirProtocol = Enum(UBInt8("ProtocolID"),
        Unspecified = 0,
        EPCGlobalC1G2 = 1,
        # 2-255 for future use
        )

class DecodingError (Exception):
    pass

class EncodingError (Exception):
    pass
