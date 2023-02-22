from typing import TypeVar, Generic
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.message import DecodeError

T = TypeVar("T")

def parseDelimited(data : bytes, message_type : Generic[T]) -> tuple[T, int]:
    if (data is None or len(data) == 0):
        return None, 0

    message_size, pos = _DecodeVarint32(data, 0)

    if (message_size + pos > len(data) or pos == 0):
        return None, 0

    current_message = data[pos:(message_size + pos)]

    message = message_type()

    try:
        message.ParseFromString(current_message)
    except (DecodeError):
        return None, pos + message_size

    return message, pos + message_size