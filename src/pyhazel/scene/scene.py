from __future__ import annotations

from typing import TYPE_CHECKING

from pyhazel.scene.components import TransformComponent
from pyhazel.scene.components import SpriteRendererComponent
from pyhazel import Renderer2D
import esper

if TYPE_CHECKING:
    from pyhazel import Timestep


class Scene:
    def __init__(self) -> None:
        self.registry = esper.World()

    def create_entity(self) -> int:
        return self.registry.create_entity()

    def update(self, ts: Timestep) -> None:
        for _, (transform, sprite) in self.registry.get_components(TransformComponent, SpriteRendererComponent):
            Renderer2D.draw_quad_impl(transform.transform, sprite.color)
