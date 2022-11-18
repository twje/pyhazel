from typing import Iterator
from .buffer_element import BufferElement


__all__ = ["BufferLayout"]


class BufferLayout:
    """
    A utility class to describe the layout of a vertex buffer.
    """

    def __init__(self, *elements: BufferElement) -> None:
        self.elements: tuple[BufferElement] = elements
        self.stride = 0
        self._calculate_offsets_and_stride()

    def _calculate_offsets_and_stride(self):
        offset = 0
        for element in self.elements:
            element.offset = offset
            offset += element.s_type.size
            self.stride += element.s_type.size

    def __iter__(self) -> Iterator[BufferElement]:
        return iter(self.elements)
