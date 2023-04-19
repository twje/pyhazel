
from __future__ import annotations

from typing import TYPE_CHECKING
from pyhazel.renderer import VertexArray
from pyhazel.renderer import ShaderDataType
from pyhazel.renderer import BufferElement
from pyhazel.renderer import BufferLayout
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


# def set_vector_vertex_attrib_callback(vertex_attrib_index: int, layout: BufferLayout, element: BufferElement):
#     glEnableVertexAttribArray(vertex_attrib_index)
#     glVertexAttribPointer(
#         vertex_attrib_index,
#         element.s_type.count,
#         shader_data_type_to_opengl_base_type(element.s_type),
#         GL_TRUE if element.normalized else GL_FALSE,
#         layout.stride,
#         ctypes.c_void_p(element.offset)
#     )


# def set_matrix_vertex_attrib_callback(vertex_attrib_index: int, layout: BufferLayout, element: BufferElement):
#     glEnableVertexAttribArray(vertex_attrib_index)
#     glVertexAttribPointer(
#         vertex_attrib_index,
#         element.s_type.count,
#         shader_data_type_to_opengl_base_type(element.s_type),
#         GL_TRUE if element.normalized else GL_FALSE,
#         layout.stride,
#         ctypes.c_void_p(element.offset)
#     )


class OpenGLVertexArray(VertexArray):
    @HZ_PROFILE_FUNCTION
    def __init__(self) -> None:
        super().__init__()
        self._index_buffer: IndexBuffer = None
        self._vertex_buffers: list[VertexBuffer] = []
        self._renderer_id = glGenVertexArrays(1)
        self._vertex_buffer_offset = 0
        glBindVertexArray(self._renderer_id)

        self.set_vertex_attrib_callbacks = {
            frozenset({
                ShaderDataType.FLOAT.name,
                ShaderDataType.FLOAT2.name,
                ShaderDataType.FLOAT3.name,
                ShaderDataType.FLOAT4.name,
                ShaderDataType.INT.name,
                ShaderDataType.INT2.name,
                ShaderDataType.INT3.name,
                ShaderDataType.INT4.name,
                ShaderDataType.BOOL.name
            }): self.set_vector_vertex_attrib_callback,
            frozenset({
                ShaderDataType.MAT3.name,
                ShaderDataType.MAT4.name,
            }): self.set_matrix_vertex_attrib_callback
        }

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
            set_vertex_attrib_callback = self.find_vertex_attrib_callback(
                element
            )
            set_vertex_attrib_callback(layout, element)

    def find_vertex_attrib_callback(self, element) -> callable([BufferLayout, BufferElement]):
        result = None
        for shader_data_type_group, set_vertex_attrib_callback in self.set_vertex_attrib_callbacks.items():
            if element.s_type.name in shader_data_type_group:
                result = set_vertex_attrib_callback
                break

        if result is None:
            assert False, "Unknown ShaderDataType!"

        return result

    @HZ_PROFILE_FUNCTION
    def set_vector_vertex_attrib_callback(self, layout: BufferLayout, element: BufferElement):
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

    @HZ_PROFILE_FUNCTION
    def set_matrix_vertex_attrib_callback(self, layout: BufferLayout, element: BufferElement):
        """Represent matrix attrib as seperate vertex attribs."""
        count = element.s_type.count
        for index in range(count):
            glEnableVertexAttribArray(self._vertex_buffer_offset)
            glVertexAttribPointer(
                self._vertex_buffer_offset,
                element.s_type.count,
                shader_data_type_to_opengl_base_type(element.s_type),
                GL_TRUE if element.normalized else GL_FALSE,
                layout.stride,
                ctypes.c_void_p(element.offset + 4 * count * index)
            )
            glVertexArrayBindingDivisor(self._vertex_buffer_offset, 1)
            self._vertex_buffer_offset += 1

    @property
    def vertex_buffers(self) -> list[VertexBuffer]:
        return self._vertex_buffers

    @property
    def index_buffer(self) -> IndexBuffer:
        return self._index_buffer

    @index_buffer.setter
    @HZ_PROFILE_FUNCTION
    def index_buffer(self, value: IndexBuffer):
        glBindVertexArray(self._renderer_id)
        value.bind()
        self._index_buffer = value
