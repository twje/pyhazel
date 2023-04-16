
import glm

__name__ = "Camera"


class Camera:
    def __init__(self, projection: glm.mat4) -> None:
        self.projection = projection
