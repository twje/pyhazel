
from __future__ import annotations

from typing import TYPE_CHECKING
from pyhazel.renderer import VertexArray
from pyhazel.renderer import ShaderDataType
from pyhazel.debug.instrumentor import *
from OpenGL.GL import *

if TYPE_CHECKING:
    from pyhazel.renderer import VertexBuffer
    from pyhazel.renderer import IndexBuffer

__all__ = ["OpenGLVertexArray"]


def shader_data_type_to_opengl_base_type(value: ShaderDataType):
    if value == ShaderDataType.FLOAT:
        return GL_FLOAT
    elif value == ShaderDataType.FLOAT2:
        return GL_FLOAT
    elif value == ShaderDataType.FLOAT3:
        return GL_FLOAT
    elif value == ShaderDataType.FLOAT4:
        return GL_FLOAT
    elif value == ShaderDataType.MAT3:
        return GL_FLOAT
    elif value == ShaderDataType.MAT4:
        return GL_FLOAT
    elif value == ShaderDataType.INT:
        return GL_INT
    elif value == ShaderDataType.INT2:
        return GL_INT
    elif value == ShaderDataType.INT3:
        return GL_INT
    elif value == ShaderDataType.INT4:
        return GL_INT
    elif value == ShaderDataType.BOOL:
        return GL_BOOL

    assert False, "Unknown ShaderDataType"


class OpenGLVertexArray(VertexArray):
    @HZ_PROFILE_FUNCTION
    def __init__(self) -> None:
        super().__init__()
        self._index_buffer: IndexBuffer = None
        self._vertex_buffers: list[VertexBuffer] = []
        self._renderer_id = glGenVertexArrays(1)
        self._vertex_buffer_offset = 0
        glBindVertexArray(self._renderer_id)

    @HZ_PROFILE_FUNCTION
    def destroy(self):
        pass
        # todo: wire up to parent class and implement

    @HZ_PROFILE_FUNCTION
    def bind(self):
        glBindVertexArray(self._renderer_id)

    @HZ_PROFILE_FUNCTION
    def unbind(self):
        glBindVertexArray(0)

    @HZ_PROFILE_FUNCTION
    def add_vertex_buffer(self, vertex_buffer: VertexBuffer):
        assert len(vertex_buffer.buffer_layout.elements) > 0

        glBindVertexArray(self._renderer_id)
        vertex_buffer.bind()

        layout = vertex_buffer.buffer_layout
        for element in layout:
            glEnableVertexAttribArray(self._vertex_buffer_offset)
            glVertexAttribPointer(
                self._vertex_buffer_offset,
                element.s_type.count,
                shader_data_type_to_opengl_base_type(element.s_type),
                GL_TRUE if element.normalized else GL_FALSE,
                layout.stride,
                ctypes.c_void_p(element.offset)
            )
            self._vertex_buffer_offset += 1

        self.vertex_buffers.append(vertex_buffer)

    @ property
    def vertex_buffers(self) -> list[VertexBuffer]:
        return self._vertex_buffers

    @ property
    def index_buffer(self) -> IndexBuffer:
        return self._index_buffer

    @index_buffer.setter
    @HZ_PROFILE_FUNCTION
    def index_buffer(self, value: IndexBuffer):
        glBindVertexArray(self._renderer_id)
        value.bind()
        self._index_buffer = value
