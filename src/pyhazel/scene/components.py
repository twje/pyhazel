import glm


class TransformComponent:
    def __init__(self) -> None:
        self.transform = glm.mat4(1)


class SpriteRendererComponent:
    def __init__(self, color=glm.vec4(1)) -> None:
        self.color = glm.vec4(color)
