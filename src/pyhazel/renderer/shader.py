
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from .renderer_api import RendererAPI

__all__ = ["Shader"]


class Shader(ABC):
    @staticmethod
    def create(vertex_src: str, fragment_src: str) -> Shader:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLShader
            return OpenGLShader(vertex_src, fragment_src)

        assert False, "Renderer type is undefined"

    @abstractmethod
    def bind(self):
        pass

    @abstractmethod
    def unbind(self):
        pass
