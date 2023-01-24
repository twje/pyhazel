from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union
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
from pyhazel.debug.instrumentor import *

import numpy as np
import glm

if TYPE_CHECKING:
    from .orthographic_camera import OrthographicCamera

__all__ = ["Renderer2D"]


class QuadVertexData:
    layout = BufferLayout(
        BufferElement(ShaderDataType.FLOAT3, "a_Position"),
        BufferElement(ShaderDataType.FLOAT4, "a_Color"),
        BufferElement(ShaderDataType.FLOAT2, "a_TexCoord"),
    )

    def __init__(self, max_vertices: int) -> None:
        self.max_vertices = max_vertices
        self.vertex_count = 0
        self.internal_buffer = np.zeros(
            max_vertices * self.layout.count,
            dtype=np.float32
        )

    @property
    def index_count(self) -> int:
        return int(self.vertex_count / 4 * 6)

    @property
    def size(self) -> int:
        return self.vertex_count * self.layout.stride

    @property
    def max_size(self) -> int:
        return self.max_vertices * self.layout.stride

    def clear(self):
        self.vertex_count = 0

    def add_vertex(self, position: glm.vec3, color: glm.vec4, tex_coord: glm.vec2):
        # position
        offset = self.get_element_offset(0)
        self.internal_buffer[offset + 0] = position.x
        self.internal_buffer[offset + 1] = position.y
        self.internal_buffer[offset + 2] = position.z

        # color
        offset = self.get_element_offset(1)
        self.internal_buffer[offset + 0] = color.x
        self.internal_buffer[offset + 1] = color.y
        self.internal_buffer[offset + 2] = color.z
        self.internal_buffer[offset + 3] = color.w

        # tex_coord
        offset = self.get_element_offset(2)
        self.internal_buffer[offset + 0] = tex_coord.x
        self.internal_buffer[offset + 1] = tex_coord.y

        self.vertex_count += 1

    def get_element_offset(self, index: int) -> int:
        return self.vertex_count * self.layout.count + int(self.layout.elements[index].offset / 4)

    def is_full(self) -> bool:
        return self.vertex_count >= self.max_vertices


class QuadVertexBuffer:
    def __init__(self, max_vertices: int) -> None:
        self.data = QuadVertexData(max_vertices)
        self.buffer = VertexBuffer.create(self.data.max_size)
        self.buffer.buffer_layout = self.data.layout

    @property
    def index_count(self) -> int:
        return self.data.index_count

    @property
    def max_size(self) -> int:
        return self.data.max_size

    def bind_to_vao(self, vao: VertexArray):
        vao.add_vertex_buffer(self.buffer)

    def add_vertex(self, position: glm.vec3, color: glm.vec4, tex_coord: glm.vec2):
        self.data.add_vertex(position, color, tex_coord)

    def clear(self):
        self.data.clear()

    def submit_data(self):
        self.buffer.set_data(
            self.data.internal_buffer,
            self.data.size
        )


@dataclass
class Renderer2DStorage:
    max_quads: int = 1000
    max_verticies: int = max_quads * 4
    max_indicies: int = max_quads * 6

    quad_vertex_array: Optional[VertexArray] = None
    quad_vertex_buffer: Optional[QuadVertexBuffer] = None
    texture_shader: Optional[Shader] = None
    white_texture: Optional[Texture2D] = None


class Renderer2D:
    data: Renderer2DStorage = None

    @classmethod
    @HZ_PROFILE_FUNCTION
    def init(cls):
        cls.data = Renderer2DStorage()

        # VAO
        cls.data.quad_vertex_array = VertexArray.create()

        # VBO
        cls.data.quad_vertex_buffer = QuadVertexBuffer(cls.data.max_verticies)
        cls.data.quad_vertex_buffer.bind_to_vao(cls.data.quad_vertex_array)

        # IBO
        square_indices = np.zeros(cls.data.max_indicies, dtype=np.uint32)
        offset = 0
        for index in range(0, cls.data.max_indicies, 6):
            square_indices[index + 0] = offset + 0
            square_indices[index + 1] = offset + 1
            square_indices[index + 2] = offset + 2

            square_indices[index + 3] = offset + 2
            square_indices[index + 4] = offset + 3
            square_indices[index + 5] = offset + 0

            offset += 4

        square_ib = IndexBuffer.create(square_indices)
        cls.data.quad_vertex_array.index_buffer = square_ib

        # White texture
        cls.data.white_texture = Texture2D.create(1, 1)

        # Shader
        shader = Shader.create_from_filepath("assets/shaders/Texture.glsl")
        shader.bind()
        shader.set_int("u_Texture", 0)
        cls.data.texture_shader = shader

    @classmethod
    def create_single_pixel_white_texture(self) -> Texture2D:
        texture = Texture2D.create(1, 1)
        texture_data = np.frombuffer(
            bytes.fromhex('ffffffff'),
            dtype=np.uint32
        )
        texture.set_data(texture_data, texture_data.nbytes)
        return texture

    @classmethod
    @HZ_PROFILE_FUNCTION
    def shutdown(cls):
        pass

    @classmethod
    @HZ_PROFILE_FUNCTION
    def begin_scene(cls, camera: OrthographicCamera):
        # Shader
        shader = cls.data.texture_shader
        shader.bind()
        shader.set_mat4(
            "u_ViewProjection",
            camera.view_projection_matrix
        )

        # Quad
        cls.data.quad_vertex_buffer.clear()

    @classmethod
    @HZ_PROFILE_FUNCTION
    def end_scene(cls):
        cls.data.quad_vertex_buffer.submit_data()
        cls.flush()

    @classmethod
    def flush(cls):
        RenderCommand.draw_vertex_array(
            cls.data.quad_vertex_array,
            cls.data.quad_vertex_buffer.index_count
        )

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_quad(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, color: glm.vec4 = glm.vec4(1.0)):  # tested
        if isinstance(position, glm.vec2):
            position = glm.vec3(position.x, position.y, 0)

        cls.data.quad_vertex_buffer.add_vertex(
            position,
            color,
            glm.vec2(0.0, 0.0)
        )
        cls.data.quad_vertex_buffer.add_vertex(
            glm.vec3(position.x + size.x, position.y, 0),
            color,
            glm.vec2(1.0, 0.0)
        )
        cls.data.quad_vertex_buffer.add_vertex(
            glm.vec3(position.x + size.x, position.y + size.y, 0),
            color,
            glm.vec2(1.0, 1.0)
        )
        cls.data.quad_vertex_buffer.add_vertex(
            glm.vec3(position.x, position.y + size.y, 0),
            color,
            glm.vec2(0.0, 1.0)
        )

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_rotated_quad(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, rotation_rad: float, color: glm.vec4 = glm.vec4(1.0)):
        raise NotImplemented()
        # if isinstance(position, glm.vec2):
        #     position = glm.vec3(position.x, position.y, 0)

        # shader = cls.data.texture_shader
        # texture = cls.data.white_texture

        # # set uniforms
        # shader.set_float4("u_Color", color)
        # shader.set_float("u_TilingFactor", 1.0)
        # texture.bind()

        # # compute transform
        # translate = glm.translate(glm.mat4(1), position)
        # rotate = glm.rotate(glm.mat4(1), rotation_rad, glm.vec3(0, 0, 1))
        # scale = glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        # transform = translate * rotate * scale
        # shader.set_mat4("u_Transform", transform)

        # cls.data.quad_vertex_array.bind()
        # RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_texture(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, texture: Texture2D, tilingFactor: float = 1, tintColor: glm.vec4 = glm.vec4(1.0)):  # tested
        raise NotImplemented()
        # if isinstance(position, glm.vec2):
        #     position = glm.vec3(position.x, position.y, 0)

        # # set uniforms
        # shader = cls.data.texture_shader
        # shader.set_float4("u_Color", tintColor)
        # shader.set_float("u_TilingFactor", tilingFactor)
        # texture.bind()

        # # compute transform
        # translate = glm.translate(glm.mat4(1), position)
        # scale = glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        # transform = translate * scale
        # shader.set_mat4("u_Transform", transform)

        # cls.data.quad_vertex_array.bind()
        # RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_rotated_texture(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, rotation_rad: float, texture: Texture2D, tilingFactor: float = 1, tintColor: glm.vec4 = glm.vec4(1.0)):
        raise NotImplemented()
        # if isinstance(position, glm.vec2):
        #     position = glm.vec3(position.x, position.y, 0)

        # # set uniforms
        # shader = cls.data.texture_shader
        # shader.set_float4("u_Color", tintColor)
        # shader.set_float("u_TilingFactor", tilingFactor)
        # texture.bind()

        # # compute transform
        # translate = glm.translate(glm.mat4(1), position)
        # rotate = glm.rotate(glm.mat4(1), rotation_rad, glm.vec3(0, 0, 1))
        # scale = glm.scale(glm.mat4(1), glm.vec3(size.x, size.y, 1))
        # transform = translate * rotate * scale
        # shader.set_mat4("u_Transform", transform)

        # cls.data.quad_vertex_array.bind()
        # RenderCommand.draw_vertex_array(cls.data.quad_vertex_array)
