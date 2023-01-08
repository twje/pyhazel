from copy import copy
from pyhazel.debug.instrumentor import *
import glm


__all__ = ["OrthographicCamera"]


class OrthographicCamera:
    @HZ_PROFILE_FUNCTION
    def __init__(self, left: float, right: float, bottom: float, top: float) -> None:
        self.projection_matrix = glm.ortho(left, right, bottom, top, -1, 1)
        self.view_matrix = glm.mat4(1)
        self.view_projection_matrix = self.projection_matrix * self.view_matrix

        self._position = glm.vec3(0, 0, 0)
        self._rotation: float = 0

    @property
    def position(self) -> glm.vec3:
        return self._position

    @position.setter
    def position(self, value: glm.vec3):
        self._position = copy(value)
        self._recalculate_view_matric()

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, value: float):
        self._rotation = value
        self._recalculate_view_matric()

    @HZ_PROFILE_FUNCTION
    def set_projection_matrix(self, left: float, right: float, bottom: float, top: float):
        self.projection_matrix = glm.ortho(left, right, bottom, top, -1, 1)
        self.view_projection_matrix = self.projection_matrix * self.view_matrix

    @HZ_PROFILE_FUNCTION
    def _recalculate_view_matric(self):
        transform = glm.translate(glm.mat4(1), self.position) * glm.rotate(
            glm.mat4(1),
            glm.radians(self.rotation),
            glm.vec3(0, 0, 1)
        )
        self.view_matrix = glm.inverse(transform)
        self.view_projection_matrix = self.projection_matrix * \
            self.view_matrix  # column major
