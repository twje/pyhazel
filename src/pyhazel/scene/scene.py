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
        self.viewport_width: int = 0
        self.viewport_height: int = 0

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

    def on_viewport_resize(self, width: int, height: int) -> None:
        self.viewport_width = width
        self.viewport_height = height

        # Resize our non-FixedAspectRatio cameras
        for _, camera_comp in self.registry.get_component(
            components.CameraComponent
        ):
            if not camera_comp.fixed_aspect_ratio:
                camera_comp.camera.set_viewport_size(width, height)
