from proto.messages_pb2 import WrapperMessage
from protobuf_parser.DelimitedMessagesStreamParser import DelimitedMessagesStreamParser

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

import unittest


class DelimitedMessagesStreamParserTest(unittest.TestCase):
    # Tests DelimitedMessagesStreamParser on some trivial cases.
    def test_trivial_cases(self):
        message = WrapperMessage()
        parser = DelimitedMessagesStreamParser(WrapperMessage)

        message.request_for_fast_response.SetInParent()
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        message.Clear()
        data += b'\x61\x02\x04'

        messages = parser.parse(data)
        print(messages)
        print(parser.m_buffer)