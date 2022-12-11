
from abc import ABC
from abc import abstractmethod
from .renderer_api import RendererAPI

__all__ = ["Texture2D"]


class Texture(ABC):
    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def bind(self, slot) -> None:
        pass

    @abstractmethod
    def delete(self) -> None:
        pass


class Texture2D(Texture):
    @staticmethod
    def create(path: str) -> Texture:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLTexture
            return OpenGLTexture(path)

        assert False, "Renderer type is undefined"
