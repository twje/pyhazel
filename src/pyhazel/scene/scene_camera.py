from enum import IntEnum
from enum import auto
import glm
from pyhazel.renderer.camera import Camera


__all__ = "SceneCamera"


class ProjectionType(IntEnum):
    PERSPECTIVE = 0
    ORTHOGRAPHIC = auto()


class SceneCamera(Camera):
    def __init__(self) -> None:
        super().__init__()
        self._projection_type = ProjectionType.ORTHOGRAPHIC

        self._perspective_vertical_fov = glm.radians(45)
        self._perspective_near = 0.01
        self._perspective_far = 1000

        self.orthographic_size = 10
        self.orthographic_near = -1
        self.orthographic_far = 1

        self.aspect_ratio = 0
        self.recalculate_projection()

    # ----------
    # Properties
    # ----------
    @property
    def projection_type(self) -> ProjectionType:
        return self._projection_type

    @projection_type.setter
    def projection_type(self, value: ProjectionType) -> None:
        self._projection_type = value
        self.recalculate_projection()

    @property
    def perspective_vertical_fov(self) -> float:
        return self._perspective_vertical_fov

    @perspective_vertical_fov.setter
    def perspective_vertical_fov(self, value: float) -> None:
        self._perspective_vertical_fov = value
        self.recalculate_projection()

    @property
    def perspective_near(self) -> float:
        return self._perspective_near

    @perspective_near.setter
    def perspective_near(self, value: float) -> None:
        self._perspective_near = value
        self.recalculate_projection()

    @property
    def perspective_far(self) -> float:
        return self._perspective_far

    @perspective_far.setter
    def perspective_far(self, value: float) -> None:
        self._perspective_far = value
        self.recalculate_projection()

    # -------
    # Methods
    # -------
    def set_orthographic(self, size: float, near_clip: float, far_clap: float):
        self._projection_type = ProjectionType.ORTHOGRAPHIC
        self.orthographic_size = size
        self.orthographic_near = near_clip
        self.orthographic_far = far_clap
        self.recalculate_projection()

    def set_perspective(self, vertical_fov: float, near_clip: float, far_clip: float):
        self._projection_type = ProjectionType.ORTHOGRAPHIC
        self._perspective_fov = vertical_fov
        self._perspective_near = near_clip
        self._perspective_far = far_clip
        self.recalculate_projection()

    def set_orthographic_size(self, size: float):
        self.orthographic_size = size
        self.recalculate_projection()

    def set_viewport_size(self, width: int, height: int) -> None:
        self.aspect_ratio = float(width)/float(height)
        self.recalculate_projection()

    def recalculate_projection(self):
        if self.projection_type == ProjectionType.PERSPECTIVE:
            self.projection = glm.perspective(
                self.perspective_vertical_fov,
                self.aspect_ratio,
                self.perspective_near,
                self.perspective_far
            )
        else:
            ortho_left = -self.orthographic_size * self.aspect_ratio * 0.5
            ortho_right = self.orthographic_size * self.aspect_ratio * 0.5
            ortho_bottom = -self.orthographic_size * 0.5
            ortho_top = self.orthographic_size * 0.5

            self.projection = glm.ortho(
                ortho_left,
                ortho_right,
                ortho_bottom,
                ortho_top
            )
