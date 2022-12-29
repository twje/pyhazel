
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from .renderer_api import RendererAPI
import glm

__all__ = ["Shader"]


class Shader(ABC):
    @staticmethod
    def create_from_filepath(filepath: str):
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLShader
            return OpenGLShader.create_from_filepath(filepath)

        assert False, "Renderer type is undefined"

    @staticmethod
    def create_from_source(name: str, vertex_src: str, fragment_src: str) -> Shader:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLShader
            return OpenGLShader.create_from_source(name, vertex_src, fragment_src)

        assert False, "Renderer type is undefined"

    @abstractmethod
    def bind(self):
        pass

    @abstractmethod
    def unbind(self):
        pass

    @abstractmethod
    def set_int(self, name: str, value: int):
        pass

    @abstractmethod
    def set_float3(self, name: str, value: glm.vec3):
        pass

    @abstractmethod
    def set_float4(self, name: str, value: glm.vec4):
        pass

    @abstractmethod
    def set_mat4(self, name: str, value: glm.mat4):
        pass

    @property
    @abstractmethod
    def name(self):
        pass
