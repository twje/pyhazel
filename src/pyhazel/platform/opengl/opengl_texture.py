from pyhazel.renderer.texture import Texture2D
from pyhazel.debug.instrumentor import *
from OpenGL.GL import *
from PIL import Image
import numpy as np

__all__ = ["OpenGLTexture"]


class OpenGLTexture(Texture2D):
    def __init__(self) -> None:
        super().__init__()
        self._renderer_id = None
        self._width = None
        self._height = None
        # describes how texture is stored in the GPU
        self.internal_format = None
        # describes format of pixel data in client memory
        self.data_format = None

    @classmethod
    @HZ_PROFILE_FUNCTION
    def create(cls, width: int, height: int) -> Texture2D:
        self = cls()

        self._width = width
        self._height = height
        self.internal_format = GL_RGBA8
        self.data_format = GL_RGBA

        self._renderer_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._renderer_id)

        # set texture filtering parameters
        glTextureParameteri(self._renderer_id,
                            GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTextureParameteri(
            self._renderer_id, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTextureParameteri(self._renderer_id, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTextureParameteri(self._renderer_id, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            self.internal_format,
            self._width,
            self._height,
            0,
            self.data_format,
            GL_UNSIGNED_BYTE,
            bytes.fromhex('00000000')
        )

        return self

    @classmethod
    @HZ_PROFILE_FUNCTION
    def create_from_path(cls, path: str) -> Texture2D:
        self = cls()

        self._renderer_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._renderer_id)

        # set texture filtering parameters
        glTextureParameteri(self._renderer_id,
                            GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTextureParameteri(
            self._renderer_id, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTextureParameteri(self._renderer_id, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTextureParameteri(self._renderer_id, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # load image data
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        data = image.tobytes()

        if image.mode == "RGB":
            self.internal_format = GL_RGB
            self.data_format = GL_RGB
        elif image.mode == "RGBA":
            self.internal_format = GL_RGBA8
            self.data_format = GL_RGBA
        else:
            assert False, "Format not supported!"

        self._width = image.width
        self._height = image.height

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            self.internal_format,
            self._width,
            self._height,
            0,
            self.data_format,
            GL_UNSIGNED_BYTE,
            data
        )

        return self

    @HZ_PROFILE_FUNCTION
    def destroy(self):
        pass
        # todo: wire up to parent class and implement

    @property
    def renderer_id(self) -> int:
        return self._renderer_id

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def set_data(self, data, size: int):
        bpp = 4 if self.data_format == GL_RGBA else 3
        assert size == bpp * self.width * self.height, "Data must be entire texture"
        glTextureSubImage2D(
            self._renderer_id,
            0,
            0,
            0,
            self.width,
            self.height,
            self.data_format,
            GL_UNSIGNED_BYTE,
            data
        )

    @HZ_PROFILE_FUNCTION
    def bind(self, slot: int = 0) -> None:
        glBindTextureUnit(slot, self._renderer_id)

    @HZ_PROFILE_FUNCTION
    def delete(self) -> None:
        glDeleteTextures(1, self._renderer_id)

    def __eq__(self, __o: object) -> bool:
        return self._renderer_id == __o._renderer_id
