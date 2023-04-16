from typing import Optional
import glm

__name__ = "Camera"


class Camera:
    def __init__(self) -> None:
        self.projection = glm.mat4(1)

    @classmethod
    def create_camera(cls, projection: glm.mat4):
        camera = cls()
        camera.projection = projection
        return camera
