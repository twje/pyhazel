from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass
from copy import copy
from . import RenderCommand
import glm

if TYPE_CHECKING:
    from . import Shader
    from . import OrthographicCamera
    from . import VertexArray

__all__ = ["Renderer"]


@dataclass
class SceneData:
    view_projection_matrix: glm.mat4 = None


class Renderer:
    scene_data = SceneData()

    @classmethod
    def begin_scene(cls, camera: OrthographicCamera):
        matrix = copy(camera.view_projection_matrix)
        cls.scene_data.view_projection_matrix = matrix

    @staticmethod
    def end_scene():
        pass

    @classmethod
    def submit(cls, shader: Shader, vertex_array: VertexArray, transform=glm.mat4(1)):
        shader.bind()
        shader.upload_uniform_mat4(
            "u_ViewProjection",
            cls.scene_data.view_projection_matrix
        )
        shader.upload_uniform_mat4(
            "u_Transform",
            transform
        )

        vertex_array.bind()
        RenderCommand.draw_vertex_array(vertex_array)
