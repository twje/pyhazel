from typing import TypeVar
from typing import Optional
from typing import Callable
import glm
from pyhazel.scene.scene_camera import SceneCamera
from pyhazel.scene.scriptable_entity import ScriptableEntity


T = TypeVar("T")  # remove


class TagComponent:
    def __init__(self, tag: str) -> None:
        self.tag = tag


class TransformComponent:
    def __init__(self) -> None:
        self.translate = glm.vec3(0)
        self.rotation = glm.vec3(0)
        self.scale = glm.vec3(1)

    def get_transform(self):
        rotation = (
            glm.rotate(glm.mat4(1.0), self.rotation.x, glm.vec3(1, 0, 0)) *
            glm.rotate(glm.mat4(1.0), self.rotation.y, glm.vec3(0, 1, 0)) *
            glm.rotate(glm.mat4(1.0), self.rotation.z, glm.vec3(0, 0, 1))
        )
        return glm.translate(glm.mat4(1.0), self.translate) * rotation * glm.scale(glm.mat4(1.0), self.scale)


class SpriteRendererComponent:
    def __init__(self, color=glm.vec4(1)) -> None:
        self.color = glm.vec4(color)


class CameraComponent:
    def __init__(self) -> None:
        self.primary = True
        self.fixed_aspect_ratio = False
        self.camera = SceneCamera()


ScriptableEntityFactoryType = Optional[Callable[[], ScriptableEntity]]


class NativeScriptComponent:
    def __init__(self) -> None:
        self.instance: Optional[ScriptableEntity] = None
        self.instantiate_script: ScriptableEntityFactoryType = None

    def bind(self, scriptable_entity_type: type[ScriptableEntity]) -> None:
        self.instantiate_script = lambda: scriptable_entity_type()
