
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
    def set_data(self, data, size: int) -> None:
        pass

    @abstractmethod
    def bind(self, slot) -> None:
        pass

    @abstractmethod
    def delete(self) -> None:
        pass

    @abstractmethod
    def __eq__(self, __o: object) -> bool:
        pass


class Texture2D(Texture):
    @staticmethod
    def create(width: int, height: int) -> Texture:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLTexture
            return OpenGLTexture.create(width, height)

        assert False, "Renderer type is undefined"

    @staticmethod
    def create_from_path(path: str) -> Texture:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLTexture
            return OpenGLTexture.create_from_path(path)

        assert False, "Renderer type is undefined"
