
from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC
from abc import abstractmethod
from .renderer_api import RendererAPI

if TYPE_CHECKING:
    from numpy import ndarray

__all__ = ["IndexBuffer"]


class IndexBuffer(ABC):
    @staticmethod
    def create(data: ndarray, count: int = 0) -> IndexBuffer:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLIndexBuffer
            return OpenGLIndexBuffer(data)

        assert False, "Renderer type is undefined"

    @abstractmethod
    def bind(self):
        pass

    @abstractmethod
    def unbind(self):
        pass

    @property
    @abstractmethod
    def count(self) -> int:
        pass
