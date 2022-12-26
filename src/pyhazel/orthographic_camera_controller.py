from __future__ import annotations

from typing import TYPE_CHECKING
from pyhazel.renderer import OrthographicCamera
from pyhazel.input import Input
from pyhazel.key_codes import *
from pyhazel.events import EventDispatcher
from pyhazel.events.mouse_events import MouseScrolledEvent
from pyhazel.events.application_event import WindowResizeEvent
import glm

if TYPE_CHECKING:
    from pyhazel.timestep import Timestep
    from pyhazel.events import Event


__all__ = ["OrthographicCameraController"]


class OrthographicCameraController:
    def __init__(self, aspect_ratio, is_rotation_enabled=False) -> None:
        self.aspect_ratio = aspect_ratio
        self.is_rotation_enabled = is_rotation_enabled
        self.zoom_level = 1.0

        self.camera_position = glm.vec3()
        self.camera_rotation = 0

        self.camera_rotation_speed = 180.0
        self.camera_translation_speed = 5

        self.camera = OrthographicCamera(
            -aspect_ratio * self.zoom_level,
            aspect_ratio * self.zoom_level,
            -self.zoom_level,
            self.zoom_level
        )

    def update(self, ts: Timestep):
        if Input.is_key_pressed(HZ_KEY_A):
            self.camera_position.x -= self.camera_translation_speed * ts.seconds
        elif Input.is_key_pressed(HZ_KEY_D):
            self.camera_position.x += self.camera_translation_speed * ts.seconds

        if Input.is_key_pressed(HZ_KEY_W):
            self.camera_position.y += self.camera_translation_speed * ts.seconds
        elif Input.is_key_pressed(HZ_KEY_S):
            self.camera_position.y -= self.camera_translation_speed * ts.seconds

        if self.is_rotation_enabled:
            if Input.is_key_pressed(HZ_KEY_Q):
                self.camera_rotation += self.camera_rotation_speed * ts.seconds
            elif Input.is_key_pressed(HZ_KEY_E):
                self.camera_rotation -= self.camera_rotation_speed * ts.seconds

            self.camera.rotation = self.camera_rotation

        self.camera.position = self.camera_position

        self.camera_translation_speed = self.zoom_level

    def on_event(self, event: Event):
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(MouseScrolledEvent, self.on_mouse_scrolled)
        dispatcher.dispatch(WindowResizeEvent, self.on_window_resized)

    def on_mouse_scrolled(self, e: MouseScrolledEvent):
        self.zoom_level -= e.y_offset * 0.25
        self.zoom_level = max(self.zoom_level, 0.25)
        self.camera.set_projection_matrix(
            -self.aspect_ratio * self.zoom_level,
            self.aspect_ratio * self.zoom_level,
            -self.zoom_level,
            self.zoom_level
        )

        return False

    def on_window_resized(self, e: WindowResizeEvent):
        self.aspect_ratio = e.width/e.height
        self.camera.set_projection_matrix(
            -self.aspect_ratio * self.zoom_level,
            self.aspect_ratio * self.zoom_level,
            -self.zoom_level,
            self.zoom_level
        )

        return False
