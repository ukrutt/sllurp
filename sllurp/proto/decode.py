"""Decoder for message constructs"""

import logging
import struct
from . import common, messages, params
from common import DecodingError

HDRFMT = '!HII'
HDRFMT_LEN = struct.calcsize(HDRFMT)

logger = logging.getLogger('sllurp')

def __getType (msghdr):
    assert len(msghdr) == HDRFMT_LEN
    ty, length, _ = struct.unpack(HDRFMT, msghdr)
    ty &= 0x3ff # lower 10 bits

    return ty, length

def decodeMessage (msgbytes):
    if len(msgbytes) < HDRFMT_LEN:
        raise DecodingError('message is too short (incomplete header)')

    # inspect the message header
    m_ty, m_len = __getType(msgbytes[:HDRFMT_LEN])

    if len(msgbytes) < m_len:
        raise DecodingError('message is too short (wanted {} bytes, ' \
                    'got {})'.format(m_len, len(msgbytes)))

    decoder = messages.getDecoderForType(m_ty)
    logger.debug('data: {}'.format(msgbytes.encode('hex')))
    logger.debug('decoder: {}'.format(decoder))

    return decoder.parse(msgbytes)
