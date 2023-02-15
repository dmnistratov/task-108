from proto.messages_pb2 import WrapperMessage
from protobuf_parser.DelimitedMessagesStreamParser import DelimitedMessagesStreamParser

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

import unittest


class DelimitedMessagesStreamParserTest(unittest.TestCase):
    # Tests DelimitedMessagesStreamParser on some trivial cases.
    def test_trivial_cases(self):
        message = WrapperMessage()
        message2 = WrapperMessage()
        parser = DelimitedMessagesStreamParser(WrapperMessage)

        # Tests RequestForFastResponse.
        message.request_for_fast_response.SetInParent()
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        messages = parser.parse(data)
        self.assertEqual(1 , len(messages))
        self.assertEqual(message, messages[0])
        messages.clear()
        message.Clear()

        # Tests RequestForSlowResponse.
        message.request_for_slow_response.time_in_seconds_to_sleep = 1
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        messages = parser.parse(data)
        self.assertEqual(1 , len(messages))
        self.assertEqual(message, messages[0])
        messages.clear()
        message.Clear()

        # Tests FastResponse.
        message.fast_response.current_date_time = "19851019T050107.333"
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        messages = parser.parse(data)
        self.assertEqual(1 , len(messages))
        self.assertEqual(message, messages[0])
        messages.clear()
        message.Clear()

        # Tests SlowResponse.
        message.slow_response.connected_client_count = 1
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        messages = parser.parse(data)
        self.assertEqual(1 , len(messages))
        self.assertEqual(message, messages[0])
        messages.clear()
        message.Clear()

        # Tests multiple identical messages.
        message.request_for_fast_response.SetInParent()
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        data += data
        messages = parser.parse(data)
        self.assertEqual(2 , len(messages))
        self.assertEqual(message, messages[0])
        self.assertEqual(message, messages[-1])
        messages.clear()
        message.Clear()
        
        # Tests miltiple different messages.
        message.request_for_fast_response.SetInParent()
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        buffer = data
        message2.request_for_slow_response.time_in_seconds_to_sleep = 1
        data = _VarintBytes(message2.ByteSize()) + message2.SerializeToString()
        buffer += data
        messages = parser.parse(buffer)
        self.assertEqual(2 , len(messages))
        self.assertEqual(message, messages[0])
        self.assertEqual(message2, messages[-1])
        messages.clear()
        message.Clear()
    
    # Tests DelimitedMessagesStreamParser on empty data.
    def test_on_empty_data(self):
        parser = DelimitedMessagesStreamParser(WrapperMessage)

        data = b""
        messages = parser.parse(data)
        self.assertEqual(0 , len(messages))

    # Tests DelimitedMessagesStreamParser with wrong buffer data.
    def test_on_wrong_data(self):
        parser = DelimitedMessagesStreamParser(WrapperMessage)

        # Test parser on message without length-prefixed
        data = b"Hello, world!"
        messages = parser.parse(data)
        self.assertEqual(0 , len(messages))

        data = b"\x02\x05\x02"
        messages = parser.parse(data)
        self.assertEqual(0 , len(messages))