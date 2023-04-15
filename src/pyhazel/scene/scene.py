from __future__ import annotations

from typing import TYPE_CHECKING

from pyhazel.scene import components
from pyhazel.scene.entity import Entity
from pyhazel import Renderer2D
import esper

if TYPE_CHECKING:
    from pyhazel import Timestep


class Scene:
    def __init__(self) -> None:
        self.registry = esper.World()

    def create_entity(self, name: str = "") -> Entity:
        entity = Entity(self.registry.create_entity(), self)
        entity.add_component(components.TransformComponent())
        entity.add_component(components.TagComponent(
            "Entity" if name == "" else name)
        )
        return entity

    def update(self, ts: Timestep) -> None:
        for _, (transform, sprite) in self.registry.get_components(
            components.TransformComponent,
            components.SpriteRendererComponent
        ):
            Renderer2D.draw_quad_impl(transform.transform, sprite.color)
