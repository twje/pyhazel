from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union
from dataclasses import dataclass
from dataclasses import field

from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .buffer_layout import BufferLayout
from .buffer_element import BufferElement
from .shader_data_type import ShaderDataType
from .index_buffer import IndexBuffer
from .texture import Texture2D
from .sub_texture_2d import SubTexture2D
from .shader import Shader
from .render_command import RenderCommand
from pyhazel.debug.instrumentor import *

import numpy as np
import glm

if TYPE_CHECKING:
    from .orthographic_camera import OrthographicCamera

__all__ = [
    "Renderer2D",
    "Statistics"
]


class Statistics:
    def __init__(self) -> None:
        self.draw_calls: int = 0
        self.quad_count: int = 0

    @property
    def total_vertex_count(self):
        return self.quad_count * 4

    @property
    def total_index_count(self):
        return self.quad_count * 6

    def reset(self):
        self.draw_calls = 0
        self.quad_count = 0


class QuadVertexData:
    layout = BufferLayout(
        BufferElement(ShaderDataType.FLOAT3, "a_Position"),
        BufferElement(ShaderDataType.FLOAT4, "a_Color"),
        BufferElement(ShaderDataType.FLOAT2, "a_TexCoord"),
        BufferElement(ShaderDataType.FLOAT, "a_TexIndex"),
        BufferElement(ShaderDataType.FLOAT, "a_TilingFactor"),
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

    def add_vertex(self, position: glm.vec3, color: glm.vec4, tex_coord: glm.vec2, tex_index: float, tiling_factor: float):
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

        # tex_index
        offset = self.get_element_offset(3)
        self.internal_buffer[offset + 0] = tex_index

        # tiling_factor
        offset = self.get_element_offset(4)
        self.internal_buffer[offset + 0] = tiling_factor

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

    def is_full(self) -> bool:
        return self.data.is_full()

    def bind_to_vao(self, vao: VertexArray):
        vao.add_vertex_buffer(self.buffer)

    def add_vertex(self, position: glm.vec3, color: glm.vec4, tex_coord: glm.vec2, tex_index: float, tiling_factor: float):
        self.data.add_vertex(
            position,
            color,
            tex_coord,
            tex_index,
            tiling_factor
        )

    def clear(self):
        self.data.clear()

    def submit_data(self):
        self.buffer.set_data(
            self.data.internal_buffer,
            self.data.size
        )


@dataclass
class Renderer2DData:  # todo: rename
    max_quads: int = 20000
    max_verticies: int = max_quads * 4
    max_indicies: int = max_quads * 6
    max_texture_slots: int = 32  # todo: render caps

    quad_vertex_array: Optional[VertexArray] = None
    quad_vertex_buffer: Optional[QuadVertexBuffer] = None
    texture_shader: Optional[Shader] = None
    white_texture: Optional[Texture2D] = None

    texture_slots: list[Optional[Texture2D]] = field(default_factory=lambda: [
                                                     None for _ in range(Renderer2DData.max_texture_slots)])
    texture_slot_index: int = 1  # 0 = white texture

    quad_vertex_positions: list[Optional[glm.vec4]] = field(
        default_factory=lambda: [None for _ in range(4)])

    stats: Statistics = field(default_factory=Statistics)


class Renderer2D:
    data: Renderer2DData = None

    @classmethod
    @HZ_PROFILE_FUNCTION
    def init(cls):
        cls.data = Renderer2DData()

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
        cls.data.white_texture = cls.create_single_pixel_white_texture()

        # Samplers
        samplers = np.arange(0, cls.data.max_texture_slots, dtype=np.int32)

        # Shader
        shader = Shader.create_from_filepath("assets/shaders/Texture.glsl")
        shader.bind()
        shader.set_int_array(
            "u_Textures",
            samplers,
            cls.data.max_texture_slots
        )

        cls.data.texture_shader = shader

        # Set all texture slots to 0
        cls.data.texture_slots[0] = cls.data.white_texture

        cls.data.quad_vertex_positions[0] = glm.vec4(-0.5, -0.5, 0.0, 1.0)
        cls.data.quad_vertex_positions[1] = glm.vec4(0.5, -0.5, 0.0, 1.0)
        cls.data.quad_vertex_positions[2] = glm.vec4(0.5,  0.5, 0.0, 1.0)
        cls.data.quad_vertex_positions[3] = glm.vec4(-0.5,  0.5, 0.0, 1.0)

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
    def bind_texture_slots(cls):
        for index in range(cls.data.texture_slot_index):
            cls.data.texture_slots[index].bind(index)

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
        cls.data.texture_slot_index = 1

    @classmethod
    @HZ_PROFILE_FUNCTION
    def end_scene(cls):
        cls.data.quad_vertex_buffer.submit_data()
        cls.flush()

    @classmethod
    def flush(cls):
        cls.bind_texture_slots()

        RenderCommand.draw_vertex_array(
            cls.data.quad_vertex_array,
            cls.data.quad_vertex_buffer.index_count
        )
        cls.data.stats.draw_calls += 1

    @classmethod
    def flush_and_reset(cls):
        cls.end_scene()
        cls.data.quad_vertex_buffer.clear()
        cls.data.texture_slot_index = 1

    @classmethod
    @HZ_PROFILE_FUNCTION
    def compute_transform(self, position: glm.vec3, size: glm.vec2, rotation_rad: float):
        translate = glm.translate(glm.mat4(1.0), position)
        if rotation_rad == 0:
            rotate = glm.mat4(1)
        else:
            rotate = glm.rotate(
                glm.mat4(1.0),
                rotation_rad,
                glm.vec3(0, 0, 1)
            )
        scale = glm.scale(glm.mat4(1.0), glm.vec3(size.x, size.y, 1.0))

        return translate * rotate * scale

    @classmethod
    def get_texture_slot(cls, texture: Texture2D):
        tex_index = 0

        for index in range(1, cls.data.texture_slot_index):
            if cls.data.texture_slots[index] == texture:
                tex_index = index
                break
        else:
            if cls.data.texture_slot_index >= cls.data.max_texture_slots:
                cls.flush_and_reset()

            tex_index = cls.data.texture_slot_index
            cls.data.texture_slots[tex_index] = texture
            cls.data.texture_slot_index += 1

        return tex_index

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_quad(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, rotation_rad: float, color: glm.vec4 = glm.vec4(1.0)):
        if isinstance(position, glm.vec2):
            position = glm.vec3(position.x, position.y, 0)

        if cls.data.quad_vertex_buffer.is_full():
            cls.flush_and_reset()

        texture_coords = [
            glm.vec2(0, 0),
            glm.vec2(1, 0),
            glm.vec2(1, 1),
            glm.vec2(0, 1)
        ]
        transform = cls.compute_transform(position, size, rotation_rad)
        tex_index = 0  # white texture
        tiling_factor = 1

        for index, texture_coord in enumerate(texture_coords):
            cls.data.quad_vertex_buffer.add_vertex(
                transform * cls.data.quad_vertex_positions[index],
                color,
                texture_coord,
                tex_index,
                tiling_factor
            )

        cls.data.stats.quad_count += 1

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_texture(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, rotation_rad: float, texture: Texture2D, tiling_factor: float = 1, tint_color: glm.vec4 = glm.vec4(1.0)):
        if isinstance(position, glm.vec2):
            position = glm.vec3(position.x, position.y, 0)

        if cls.data.quad_vertex_buffer.is_full():
            cls.flush_and_reset()

        texture_index = cls.get_texture_slot(texture)
        texture_coords = [
            glm.vec2(0, 0),
            glm.vec2(1, 0),
            glm.vec2(1, 1),
            glm.vec2(0, 1)
        ]
        transform = cls.compute_transform(position, size, rotation_rad)

        for index, texture_coord in enumerate(texture_coords):
            cls.data.quad_vertex_buffer.add_vertex(
                transform * cls.data.quad_vertex_positions[index],
                tint_color,
                texture_coord,
                texture_index,
                tiling_factor
            )

        cls.data.stats.quad_count += 1

    @classmethod
    @HZ_PROFILE_FUNCTION
    def draw_sub_texture(cls, position: Union[glm.vec2, glm.vec3], size: glm.vec2, rotation_rad: float, sub_texture: SubTexture2D, tiling_factor: float = 1, tint_color: glm.vec4 = glm.vec4(1.0)):
        if isinstance(position, glm.vec2):
            position = glm.vec3(position.x, position.y, 0)

        if cls.data.quad_vertex_buffer.is_full():
            cls.flush_and_reset()

        texture_index = cls.get_texture_slot(sub_texture.texture)
        texture_coords = sub_texture.tex_coords
        transform = cls.compute_transform(position, size, rotation_rad)

        for index, texture_coord in enumerate(texture_coords):
            cls.data.quad_vertex_buffer.add_vertex(
                transform * cls.data.quad_vertex_positions[index],
                tint_color,
                texture_coord,
                texture_index,
                tiling_factor
            )

        cls.data.stats.quad_count += 1

    @classmethod
    def reset_stats(cls):
        cls.data.stats.reset()

    @classmethod
    def get_stats(cls) -> Statistics:
        return cls.data.stats
