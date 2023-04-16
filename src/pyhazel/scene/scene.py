from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional
from pyhazel.scene import components
from pyhazel.scene.entity import Entity
from pyhazel.renderer.camera import Camera
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
        # Render 2D
        main_camera: Optional[Camera] = None
        camera_transform = None

        for _, (transform, camera) in self.registry.get_components(
            components.TransformComponent,
            components.CameraComponent
        ):
            if camera.primary:
                main_camera = camera.camera
                camera_transform = transform.transform
                break

        if main_camera is not None:
            Renderer2D.begin_scene_from_camera(
                main_camera,
                camera_transform
            )

            for _, (transform, sprite) in self.registry.get_components(
                components.TransformComponent,
                components.SpriteRendererComponent
            ):
                Renderer2D.draw_quad_impl(transform.transform, sprite.color)

            Renderer2D.end_scene()
