from typing import TypeVar, Generic, Any

T = TypeVar("T")

class DelimitedMessagesStreamParser:
    def __init__(self, type : Generic[T]) -> None:
        self.m_buffer = ''
        self.type = type

    def parse(self, data : bytes) -> list[T]:
        self.m_buffer += data

        messages : list[T]

        

