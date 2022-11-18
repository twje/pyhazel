from __future__ import annotations

from typing import TYPE_CHECKING
from . import RenderCommand

if TYPE_CHECKING:
    from . import VertexArray

__all__ = ["Renderer"]


class Renderer:
    @staticmethod
    def begin_scene():
        pass

    @staticmethod
    def end_scene():
        pass

    @staticmethod
    def submit(vertex_array: VertexArray):
        vertex_array.bind()
        RenderCommand.draw_vertex_array(vertex_array)
