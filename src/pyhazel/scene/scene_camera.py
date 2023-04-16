from pyhazel.renderer.camera import Camera
import glm

__all__ = "SceneCamera"


class SceneCamera(Camera):
    def __init__(self) -> None:
        super().__init__()
        self.orthographic_size = 10
        self.orthographic_near = -1
        self.orthographic_far = 1
        self.aspect_ratio = 0
        self.recalculate_projection()

    def set_orthographic(self, size: float, near_clip: float, far_clap: float):
        self.orthographic_size = size
        self.orthographic_near = near_clip
        self.orthographic_far = far_clap
        self.recalculate_projection()

    def set_orthographic_size(self, size: float):
        self.orthographic_size = size
        self.recalculate_projection()

    def set_viewport_size(self, width: int, height: int) -> None:
        self.aspect_ratio = float(width)/float(height)
        self.recalculate_projection()

    def recalculate_projection(self):
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
