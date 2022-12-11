from pyhazel.renderer.texture import Texture2D
from OpenGL.GL import *
from PIL import Image
import numpy as np

__all__ = ["OpenGLTexture"]


class OpenGLTexture(Texture2D):
    def __init__(self, path: str) -> None:
        super().__init__()

        self.renderer_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.renderer_id)

        # set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # load image data
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        data = image.convert("RGB").tobytes()

        self._width = image.width
        self._height = image.height

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            self._width,
            self._height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            data
        )

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def bind(self, slot: int = 0) -> None:
        glBindTextureUnit(slot, self.renderer_id)

    def delete(self) -> None:
        glDeleteTextures(1, self.renderer_id)
