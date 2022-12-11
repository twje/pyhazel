from __future__ import annotations

from typing import TYPE_CHECKING
from pyhazel.renderer import IndexBuffer
from OpenGL.GL import *


if TYPE_CHECKING:
    from numpy import ndarray


__all__ = ["OpenGLIndexBuffer"]


class OpenGLIndexBuffer(IndexBuffer):
    def __init__(self, data: ndarray) -> None:
        super().__init__()
        self._renderer_id = glGenBuffers(1)
        self._count = len(data)

        glBindBuffer(GL_ARRAY_BUFFER, self._renderer_id)
        glBufferData(
            GL_ARRAY_BUFFER,
            data.nbytes,
            data,
            GL_STATIC_DRAW
        )

    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._renderer_id)

    def unbind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    @property
    def count(self) -> int:
        return self._count
