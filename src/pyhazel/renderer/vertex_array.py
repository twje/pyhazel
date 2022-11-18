from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Sequence
from abc import ABC
from abc import abstractmethod
from .renderer_api import RendererAPI

if TYPE_CHECKING:
    from .vertex_buffer import VertexBuffer
    from .index_buffer import IndexBuffer


__all__ = ["VertexArray"]


class VertexArray(ABC):
    @staticmethod
    def create() -> VertexArray:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLVertexArray
            return OpenGLVertexArray()

        assert False, "Renderer type is undefined"

    @abstractmethod
    def bind(self):
        pass

    @abstractmethod
    def unbind(self):
        pass

    @abstractmethod
    def add_vertex_buffer(self, vertex_buffer):
        pass

    @property
    @abstractmethod
    def vertex_buffers(self) -> Sequence[VertexBuffer]:
        pass

    @property
    @abstractmethod
    def index_buffer(self) -> IndexBuffer:
        pass

    @index_buffer.setter
    @abstractmethod
    def index_buffer(self, value: IndexBuffer):
        pass
