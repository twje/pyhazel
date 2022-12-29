from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .buffer_layout import BufferLayout
from .buffer_element import BufferElement
from .shader_data_type import ShaderDataType
from .index_buffer import IndexBuffer
from .texture import Texture2D
from .shader import Shader
from .render_command import RenderCommand

import numpy as np
import glm

if TYPE_CHECKING:
    from .orthographic_camera import OrthographicCamera

__all__ = ["Renderer2D"]


@dataclass
class Renderer2DStorage:
    quad_vertex_array: VertexArray = None
    flat_color_shader: Shader = None
    texture_shader: Shader = None


class Renderer2D:
    data: Renderer2DStorage = None

    @classmethod
    def init(cls):
        cls.data = Renderer2DStorage()
        cls.data.quad_vertex_array = VertexArray.create()

        square_vertices = np.array([
            -0.5, -0.5, 0.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 1.0, 0.0,
            0.5,  0.5, 0.0, 1.0, 1.0,
            -0.5,  0.5, 0.0, 0.0, 1.0
        ], dtype=np.float32)

        square_vb = VertexBuffer.create(square_vertices)
        square_vb.buffer_layout = BufferLayout(
            BufferElement(ShaderDataType.FLOAT3, "a_Position"),
            BufferElement(ShaderDataType.FLOAT2, "a_TexCoord"),
        )
        cls.data.quad_vertex_array.add_vertex_buffer(square_vb)

        square_indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        square_ib = IndexBuffer.create(square_indices)
        cls.data.quad_vertex_array.index_buffer = square_ib

        cls.data.flat_color_shader = Shader.create_from_filepath(
            "assets/shaders/FlatColor.glsl")
        cls.data.texture_shader = Shader.create_from_filepath(
            "assets/shaders/Texture.glsl")
        cls.data.texture_shader.bind()
        cls.data.texture_shader.set_int("u_Texture", 0)

    @classmethod
    def shutdown(cls):
        cls.data = None

    @classmethod
    def begin_scene(cls, camera: OrthographicCamera):
        # flat color shader
        shader = cls.data.flat_color_shader
        shader.bind()
        shader.set_mat4(
            "u_ViewProjection",
            camera.view_projection_matrix
        )

        # texture shader
        shader = cls.data.texture_shader
        shader.bind()
        shader.set_mat4(
            "u_ViewProjection",
            camera.view_projection_matrix
        )

    @classmethod
    def end_scene(cls):
        pass

    @classmethod
    def draw_quad(cls, position: glm.vec3, size: glm.vec2, color: glm.vec4):
        shader = cls.data.flat_color_shader
        shader.bind()
        shader.set_float4("u_Color", color)

        transform = glm.translate(
            glm.mat4(1), position) * glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        shader.set_mat4("u_Transform", transform)

        cls.data.quad_vertex_array.bind()
        RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)

    @classmethod
    def draw_texture(cls, position: glm.vec3, size: glm.vec2, texture: Texture2D):
        shader = cls.data.texture_shader
        shader.bind()

        transform = glm.translate(
            glm.mat4(1), position) * glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        shader.set_mat4("u_Transform", transform)

        texture.bind()

        cls.data.quad_vertex_array.bind()
        RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)
