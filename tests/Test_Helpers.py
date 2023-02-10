from proto.messages_pb2 import WrapperMessage
from protobuf_parser.helpers import parseDelimited

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

import unittest


class ParseDelimitedTest(unittest.TestCase):
    # Tests parseDelimited function on some trivial cases.
    def test_trivial_cases(self):
        message = WrapperMessage()

        # Tests RequestForFastResponse.
        message.request_for_fast_response.SetInParent()
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        parsedMessage, bytesConsumed = parseDelimited(data, WrapperMessage)

        self.assertEqual(message, parsedMessage)
        message.Clear()

        # Tests RequestForSlowResponse.
        message.request_for_slow_response.time_in_seconds_to_sleep = 1
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        parsedMessage, bytesConsumed = parseDelimited(data, WrapperMessage)

        self.assertEqual(message, parsedMessage)
        message.Clear()

        # Tests FastResponse.
        message.fast_response.current_date_time = "19851019T050107.333"
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        parsedMessage, bytesConsumed = parseDelimited(data, WrapperMessage)

        self.assertEqual(message, parsedMessage)
        message.Clear()

        # Tests SlowResponse.
        message.slow_response.connected_client_count = 1
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        parsedMessage, bytesConsumed = parseDelimited(data, WrapperMessage)

        self.assertEqual(message, parsedMessage)
        message.Clear()

    # Tests parseDelimited function on empty data.
    def test_empty_data(self):
        parsedMessage, bytesConsumed =  parseDelimited(None, WrapperMessage)
        self.assertEqual(None, parsedMessage)
        self.assertEqual(0, bytesConsumed)

        parsedMessage, bytesConsumed =  parseDelimited("", WrapperMessage)
        self.assertEqual(None, parsedMessage)
        self.assertEqual(0, bytesConsumed)

    # Tests parseDelimited funcion length-prefixed.
    def test_length_prefixed(self):
        message = WrapperMessage()
        data = ""

        # Tests string as message without length-prefixed.
        data = "String test"
        parsedMessage, bytesConsumed =  parseDelimited(data, WrapperMessage)
        self.assertEqual(None, parsedMessage)
        self.assertEqual(len(data), bytesConsumed)

        # Tests message without length-prefixed.
        message.request_for_fast_response.SetInParent()
        data = message.SerializeToString()
        parsedMessage, bytesConsumed =  parseDelimited(data, WrapperMessage)
        self.assertEqual(None, parsedMessage)
        self.assertEqual(0, bytesConsumed) # \x1a == 26 waiting for other bytes

        # Tests message with length-prefixed.
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        parsedMessage, bytesConsumed =  parseDelimited(data, WrapperMessage)
        self.assertEqual(message, parsedMessage)

    # Tests parseDelimited bytesConsumed.
    def test_bytes_consumed(self):
        message = WrapperMessage()
        buffer = ""

        # Test bytesConsumed with empty message.
        parsedMessage, bytesConsumed =  parseDelimited(None, WrapperMessage)
        self.assertEqual(0, bytesConsumed)

        # Test bytesConsumed on trivial case.
        message.request_for_fast_response.SetInParent()
        data = _VarintBytes(message.ByteSize()) + message.SerializeToString()
        parsedMessage, bytesConsumed =  parseDelimited(data, WrapperMessage)
        self.assertEqual(3 , bytesConsumed)
        
        # Tests bytesConsumed on multiple messages.
        buffer += str(data)
        buffer += str(data)
        parsedMessage, bytesConsumed =  parseDelimited(data, WrapperMessage)
        self.assertEqual(3 , bytesConsumed)
        self.assertEqual(message , parsedMessage)

    # Test parseDelimited on unsupported type.
    def test_unsupported_type(self):
        message = "Hello, world!"

        data =  _VarintBytes(len(message)) + str.encode(message)
        parsedMessage, bytesConsumed =  parseDelimited(data, str)
        self.assertEqual(None , parsedMessage)
        self.assertEqual(len(data), bytesConsumed)