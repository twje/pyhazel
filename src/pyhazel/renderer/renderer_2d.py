from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .buffer_layout import BufferLayout
from .buffer_element import BufferElement
from .shader_data_type import ShaderDataType
from .index_buffer import IndexBuffer
from .shader import Shader
from .render_command import RenderCommand

import numpy as np
import glm

if TYPE_CHECKING:
    from .orthographic_camera import OrthographicCamera
    from pyhazel.platform.opengl.opengl_shader import OpenGLShader

__all__ = ["Renderer2D"]


@dataclass
class Renderer2DStorage:
    quad_vertex_array: VertexArray = None
    flat_color_shader: Shader = None


class Renderer2D:
    data: Renderer2DStorage = None

    @classmethod
    def init(cls):
        cls.data = Renderer2DStorage()
        cls.data.quad_vertex_array = VertexArray.create()

        square_vertices = np.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.5,  0.5, 0.0,
            -0.5,  0.5, 0.0,
        ], dtype=np.float32)

        square_vb = VertexBuffer.create(square_vertices)
        square_vb.buffer_layout = BufferLayout(
            BufferElement(ShaderDataType.FLOAT3, "a_Position"),
        )
        cls.data.quad_vertex_array.add_vertex_buffer(square_vb)

        square_indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        square_ib = IndexBuffer.create(square_indices)
        cls.data.quad_vertex_array.index_buffer = square_ib

        cls.data.flat_color_shader = Shader.create_from_filepath(
            "assets/shaders/FlatColor.glsl")

    @classmethod
    def shutdown(cls):
        cls.data = None

    @classmethod
    def begin_scene(cls, camera: OrthographicCamera):
        # todo: update interface of baseclass
        shader: OpenGLShader = cls.data.flat_color_shader
        shader.bind()
        shader.upload_uniform_mat4(
            "u_ViewProjection",
            camera.view_projection_matrix
        )
        shader.upload_uniform_mat4("u_Transform", glm.mat4(1))

    @classmethod
    def end_scene(cls):
        pass

    @classmethod
    def draw_quad(cls, position: glm.vec2, size: glm.vec2, color: glm.vec4):
        # todo: update interface of baseclass
        shader: OpenGLShader = cls.data.flat_color_shader
        shader.bind()
        shader.upload_uniform_float4("u_Color", color)

        cls.data.quad_vertex_array.bind()
        RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)
