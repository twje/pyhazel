from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional
from typing import TypeVar

if TYPE_CHECKING:
    from pyhazel.scene.scene import Scene


__name__ = ["Entity"]


T = TypeVar("T")


class Entity:
    def __init__(self, handle: int, scene: Scene) -> None:
        self.handle = handle
        self.scene = scene

    def add_component(self, component_instance: T) -> T:
        self.scene.registry.add_component(self.handle, component_instance)
        return component_instance

    def get_component(self, component_type: type[T]) -> T:
        return self.scene.registry.component_for_entity(self.handle, component_type)

    def has_component(self, component_type: type[T]) -> bool:
        return self.scene.registry.has_component(self.handle, component_type)

    def remove_component(self, component_type) -> None:
        self.scene.registry.remove_component(self.handle, component_type)

    def __bool__(self) -> bool:
        return self.handle != 0

    def __eq__(self, other: Optional[Entity]) -> bool:
        if other is None:
            return False
        return self.handle == other.handle and self.scene is other.scene
