"""Structures used throughout LLRP messages and parameters."""

from construct import *

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
def TLVParameterHeader (paramType):
    assert paramType > 127
    assert paramType < 1024
    return Struct("TLVParameterHeader",
            EmbeddedBitStruct(
                Const(Bit("TV"), 0),
                Padding(5),
                Const(BitField("Type", 10), paramType)),
            UBInt16("Length"))            # XXX dynamically compute?

# 17.2.1.2
def TVParameterHeader (paramType):
    assert paramType > 0
    assert paramType < 128
    return BitStruct("TVParameterHeader",
            Const(Bit("TV"), 1),
            Const(BitField("Type", 7), paramType))
