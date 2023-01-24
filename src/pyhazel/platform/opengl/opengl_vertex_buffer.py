
from __future__ import annotations

from typing import TYPE_CHECKING
from pyhazel.renderer.vertex_buffer import VertexBuffer
from pyhazel.debug.instrumentor import *
from OpenGL.GL import *


if TYPE_CHECKING:
    from pyhazel.renderer import BufferLayout
    from numpy import ndarray


__all__ = ["OpenGLVertexBuffer"]


class OpenGLVertexBuffer(VertexBuffer):
    @HZ_PROFILE_FUNCTION
    def __init__(self) -> None:
        super().__init__()
        self._layout: BufferLayout = None
        self._renderer_id = glGenBuffers(1)

    @classmethod
    def init_factory(cls, size: int):
        instance = cls()
        glBindBuffer(GL_ARRAY_BUFFER, instance._renderer_id)
        glBufferData(GL_ARRAY_BUFFER, size, None, GL_DYNAMIC_DRAW)
        return instance

    @classmethod
    def init_from_data_factory(cls, data: ndarray):
        instance = cls()
        glBindBuffer(GL_ARRAY_BUFFER, instance._renderer_id)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        return instance

    @HZ_PROFILE_FUNCTION
    def destroy(self):
        pass
        # todo: wire up to parent class and implement

    @HZ_PROFILE_FUNCTION
    def bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self._renderer_id)

    @HZ_PROFILE_FUNCTION
    def unbind(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    @property
    def buffer_layout(self) -> BufferLayout:
        return self.layout

    @buffer_layout.setter
    def buffer_layout(self, value: BufferLayout):
        self.layout = value

    def set_data(self, data: ndarray, size: int = 0):
        glBindBuffer(GL_ARRAY_BUFFER, self._renderer_id)
        glBufferSubData(GL_ARRAY_BUFFER, 0, size, data)
