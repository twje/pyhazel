
from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC
from abc import abstractmethod
from .renderer_api import RendererAPI

if TYPE_CHECKING:
    from .buffer_layout import BufferLayout
    from numpy import ndarray

__all__ = ["VertexBuffer"]


class VertexBuffer(ABC):
    @staticmethod
    def create(data: ndarray) -> VertexBuffer:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLVertexBuffer
            return OpenGLVertexBuffer(data)

        assert False, "Renderer type is undefined"

    @abstractmethod
    def bind(self):
        pass

    @abstractmethod
    def unbind(self):
        pass

    @property
    @abstractmethod
    def buffer_layout(self) -> BufferLayout:
        pass

    @buffer_layout.setter
    @abstractmethod
    def buffer_layout(self, value: BufferLayout):
        pass
