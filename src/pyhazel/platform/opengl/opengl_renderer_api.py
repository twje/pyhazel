"""
Todo:
    - Port commit '8c3cc55b93a7261f0ae45f56082a05001eebbdec' - Logging OpenGL messages (#114)
"""
from __future__ import annotations

from typing import TYPE_CHECKING
from pyhazel.renderer import RendererAPI
from pyhazel.debug.instrumentor import *
from OpenGL.GL import *
import glm

if TYPE_CHECKING:
    from pyhazel.renderer import VertexArray


__all__ = ["OpenGLRendererAPI"]


class OpenGLRendererAPI(RendererAPI):
    @HZ_PROFILE_FUNCTION
    def init(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_DEPTH_TEST)

    def set_viewport(self, x: float, y: float, width: float, height: float):
        glViewport(x, y, width, height)

    def set_clear_color(self, color: glm.vec4):
        glClearColor(color.r, color.g, color.b, color.a)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def draw_vertex_array(self, vertex_array: VertexArray):
        glDrawElements(
            GL_TRIANGLES,
            vertex_array.index_buffer.count,
            GL_UNSIGNED_INT,
            None
        )
