from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union
from dataclasses import dataclass
import math

from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .buffer_layout import BufferLayout
from .buffer_element import BufferElement
from .shader_data_type import ShaderDataType
from .index_buffer import IndexBuffer
from .texture import Texture2D
from .shader import Shader
from .render_command import RenderCommand
from pyhazel.debug.instrumentor import *

import numpy as np
import glm

if TYPE_CHECKING:
    from .orthographic_camera import OrthographicCamera

__all__ = ["Renderer2D"]


@dataclass
class Renderer2DStorage:
    quad_vertex_array: VertexArray = None
    flat_color_shader: Shader = None  # remove
    texture_shader: Optional[Shader] = None
    white_texture: Texture2D = None


class Renderer2D:
    data: Renderer2DStorage = None

    @classmethod
    @HZ_PROFILE_FUNCTION
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

        cls.data.white_texture = Texture2D.create(1, 1)
        white_texture_data = np.frombuffer(
            bytes.fromhex('ffffffff'),
            dtype=np.uint32
        )

        indicies = np.array([
            0, 1, 2,
            2, 3, 0,
        ], dtype=np.uint32)

        cls.data.white_texture.set_data(
            white_texture_data, white_texture_data.nbytes)

        cls.data.texture_shader = Shader.create_from_filepath(
            "assets/shaders/Texture.glsl")
        cls.data.texture_shader.bind()
        cls.data.texture_shader.set_int("u_Texture", 0)

    @classmethod
    @HZ_PROFILE_FUNCTION
    def shutdown(cls):
        cls.data = None

    @classmethod
    @HZ_PROFILE_FUNCTION
    def begin_scene(cls, camera: OrthographicCamera):
        shader = cls.data.texture_shader
        shader.bind()
        shader.set_mat4(
            "u_ViewProjection",
            camera.view_projection_matrix
        )

    @classmethod
    @HZ_PROFILE_FUNCTION
    def end_scene(cls):
        pass

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_quad(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, color: glm.vec4 = glm.vec4(1.0)):  # tested
        if isinstance(position, glm.vec2):
            position = glm.vec3(position.x, position.y, 0)

        shader = cls.data.texture_shader
        texture = cls.data.white_texture

        # set uniforms
        shader.set_float4("u_Color", color)
        shader.set_float("u_TilingFactor", 1.0)
        texture.bind()

        # compute transform
        translate = glm.translate(glm.mat4(1), position)
        scale = glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        transform = translate * scale
        shader.set_mat4("u_Transform", transform)

        cls.data.quad_vertex_array.bind()
        RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_rotated_quad(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, rotation_deg: float, color: glm.vec4 = glm.vec4(1.0)):
        if isinstance(position, glm.vec2):
            position = glm.vec3(position.x, position.y, 0)

        shader = cls.data.texture_shader
        texture = cls.data.white_texture
        rotation_rad = math.radians(rotation_deg)

        # set uniforms
        shader.set_float4("u_Color", color)
        shader.set_float("u_TilingFactor", 1.0)
        texture.bind()

        # compute transform
        translate = glm.translate(glm.mat4(1), position)
        rotate = glm.rotate(glm.mat4(1), rotation_rad, glm.vec3(0, 0, 1))
        scale = glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        transform = translate * rotate * scale
        shader.set_mat4("u_Transform", transform)

        cls.data.quad_vertex_array.bind()
        RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_texture(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, texture: Texture2D, tilingFactor: float = 1, tintColor: glm.vec4 = glm.vec4(1.0)):  # tested
        if isinstance(position, glm.vec2):
            position = glm.vec3(position.x, position.y, 0)

        # set uniforms
        shader = cls.data.texture_shader
        shader.set_float4("u_Color", tintColor)
        shader.set_float("u_TilingFactor", tilingFactor)
        texture.bind()

        # compute transform
        translate = glm.translate(glm.mat4(1), position)
        scale = glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        transform = translate * scale
        shader.set_mat4("u_Transform", transform)

        cls.data.quad_vertex_array.bind()
        RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_rotated_texture(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, rotation_deg: float, texture: Texture2D, tilingFactor: float = 1, tintColor: glm.vec4 = glm.vec4(1.0)):
        if isinstance(position, glm.vec2):
            position = glm.vec3(position.x, position.y, 0)

        rotation_rad = math.radians(rotation_deg)

        # set uniforms
        shader = cls.data.texture_shader
        shader.set_float4("u_Color", tintColor)
        shader.set_float("u_TilingFactor", tilingFactor)
        texture.bind()

        # compute transform
        translate = glm.translate(glm.mat4(1), position)
        rotate = glm.rotate(glm.mat4(1), rotation_rad, glm.vec3(0, 0, 1))
        scale = glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        transform = translate * rotate * scale
        shader.set_mat4("u_Transform", transform)

        cls.data.quad_vertex_array.bind()
        RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)
