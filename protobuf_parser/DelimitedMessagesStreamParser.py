from typing import TypeVar, Generic
from .helpers import parseDelimited

T = TypeVar("T")

class DelimitedMessagesStreamParser:
    def __init__(self, message_type : Generic[T]) -> None:
        self.m_buffer = b''
        self.message_type = message_type

    def parse(self, data : bytes) -> list[T]:
        self.m_buffer += data

        messages : list[T] = []

        while (self.m_buffer):
            message, bytesConsumed = parseDelimited(self.m_buffer, self.message_type)
            if message:
                messages.append(message)
            
            if (bytesConsumed == 0):
                break
            
            self.m_buffer = self.m_buffer[bytesConsumed:]

        return messages