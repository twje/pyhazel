
from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC
from abc import abstractmethod
from enum import Enum
from enum import auto
import glm

if TYPE_CHECKING:
    from . import VertexArray

__all__ = ["RendererAPI"]


class RendererAPI(ABC):
    class API(Enum):
        NONE = auto()
        OpenGL = auto()

    @staticmethod
    def create() -> RendererAPI:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLRendererAPI
            return OpenGLRendererAPI()

        assert False, "Renderer type is undefined"

    @abstractmethod
    def set_clear_color(self, color: glm.vec4):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def draw_vertex_array(self, vertex_array: VertexArray):
        pass

    @classmethod
    @property
    def api(cls) -> API:
        return cls.API.OpenGL
