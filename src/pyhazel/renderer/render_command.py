from __future__ import annotations
from typing import TYPE_CHECKING
import glm

if TYPE_CHECKING:
    from .vertex_array import VertexArray

__all__ = ["RenderCommand"]


class LazyRendererAPIFactory:
    """
    This class is a non-data descriptor factory to defer the import of RendererAPI 
    until runtime to avoid a partial circular import.
    """

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, type=None) -> object:
        from .renderer_api import RendererAPI
        type.__dict__[self.name] = RendererAPI.create()
        return type.__dict__[self.name]


class RenderCommand:
    _renderer_api = None

    @classmethod
    @property
    def renderer_api(cls):
        if cls._renderer_api is None:
            from .renderer_api import RendererAPI
            cls._renderer_api = RendererAPI.create()
        return cls._renderer_api

    @classmethod
    def init(cls):
        cls.renderer_api.init()

    @classmethod
    def on_window_resize(cls, x: float, y: float, width: float, height: float):
        cls.renderer_api.set_viewport(x, y, width, height)

    @classmethod
    def set_clear_color(cls, color: glm.vec4):
        cls.renderer_api.set_clear_color(color)

    @classmethod
    def clear(cls):
        cls.renderer_api.clear()

    @classmethod
    def draw_vertex_array(cls, vertex_array: VertexArray):
        cls.renderer_api.draw_vertex_array(vertex_array)
