import glm
from pyhazel.renderer.camera import Camera


class TagComponent:
    def __init__(self, tag: str) -> None:
        self.tag = tag


class TransformComponent:
    def __init__(self) -> None:
        self.transform = glm.mat4(1)


class SpriteRendererComponent:
    def __init__(self, color=glm.vec4(1)) -> None:
        self.color = glm.vec4(color)


class CameraComponent:
    def __init__(self, projection: glm.mat4) -> None:
        self.primary = True
        self.camera = Camera(projection)
