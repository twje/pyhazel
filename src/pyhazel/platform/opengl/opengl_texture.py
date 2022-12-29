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
        glTextureParameteri(self.renderer_id, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTextureParameteri(
            self.renderer_id, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTextureParameteri(self.renderer_id, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTextureParameteri(self.renderer_id, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # load image data
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        data = image.tobytes()

        internal_format = 0
        data_format = 0
        if image.mode == "RGB":
            internal_format = GL_RGB
            data_format = GL_RGB
        elif image.mode == "RGBA":
            internal_format = GL_RGBA8
            data_format = GL_RGBA
        else:
            assert False, "Format not supported!"

        self._width = image.width
        self._height = image.height

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            internal_format,  # describes how texture is stored in the GPU
            self._width,
            self._height,
            0,
            data_format,  # describes format of pixel data in client memory
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
