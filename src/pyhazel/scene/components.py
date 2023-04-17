from typing import TypeVar
from typing import Optional
from typing import Callable
import glm
from pyhazel.scene.scene_camera import SceneCamera
from pyhazel.scene.scriptable_entity import ScriptableEntity


T = TypeVar("T")


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
