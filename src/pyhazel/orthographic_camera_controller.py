from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass
import math


from pyhazel.renderer import OrthographicCamera
from pyhazel.input import Input
from pyhazel.key_codes import KeyCode
from pyhazel.events import EventDispatcher
from pyhazel.events.mouse_events import MouseScrolledEvent
from pyhazel.events.application_event import WindowResizeEvent
from pyhazel.debug.instrumentor import *
import glm

if TYPE_CHECKING:
    from pyhazel.timestep import Timestep
    from pyhazel.events import Event


__all__ = ["OrthographicCameraController"]


@dataclass
class OrthographicCameraBounds:
    left: int = 0
    right: int = 0
    bottom: int = 0
    top: int = 0

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.top - self.bottom


class OrthographicCameraController:
    @HZ_PROFILE_FUNCTION
    def __init__(self, aspect_ratio, is_rotation_enabled=False) -> None:
        self.aspect_ratio = aspect_ratio
        self.is_rotation_enabled = is_rotation_enabled
        self._zoom_level = 1.0

        self.camera_position = glm.vec3()
        self.camera_rotation = 0

        self.camera_rotation_speed = 180.0
        self.camera_translation_speed = 5

        self.bounds = OrthographicCameraBounds(
            -aspect_ratio * self._zoom_level,
            aspect_ratio * self._zoom_level,
            -self._zoom_level,
            self._zoom_level
        )
        self.camera = OrthographicCamera(
            self.bounds.left,
            self.bounds.right,
            self.bounds.bottom,
            self.bounds.top
        )

    @property
    def zoom_level(self) -> float:
        return self._zoom_level

    @zoom_level.setter
    def zoom_level(self, value: float) -> None:
        self._zoom_level = value
        self.set_camera_projection_matrix()

    def update(self, ts: Timestep):
        if Input.is_key_pressed(KeyCode.KEY_A):
            self.camera_position.x -= self.calc_anti_cos_rotate(ts)
            self.camera_position.y -= self.calc_anti_sin_rotate(ts)
        elif Input.is_key_pressed(KeyCode.KEY_D):
            self.camera_position.x += self.calc_anti_cos_rotate(ts)
            self.camera_position.y += self.calc_anti_sin_rotate(ts)
        if Input.is_key_pressed(KeyCode.KEY_W):
            self.camera_position.x += -self.calc_anti_sin_rotate(ts)
            self.camera_position.y += self.calc_anti_cos_rotate(ts)
        elif Input.is_key_pressed(KeyCode.KEY_S):
            self.camera_position.x -= -self.calc_anti_sin_rotate(ts)
            self.camera_position.y -= self.calc_anti_cos_rotate(ts)

        if self.is_rotation_enabled:
            if Input.is_key_pressed(KeyCode.KEY_Q):
                self.camera_rotation += self.camera_rotation_speed * ts.seconds
            elif Input.is_key_pressed(KeyCode.KEY_E):
                self.camera_rotation -= self.camera_rotation_speed * ts.seconds

            if self.camera_position > 180:
                self.camera_rotation -= 360
            elif self.camera_rotation <= -180:
                self.camera_rotation += 360

            self.camera.rotation = self.camera_rotation

        self.camera.position = self.camera_position

        self.camera_translation_speed = self.zoom_level

    def calc_anti_cos_rotate(self, ts: Timestep):
        return math.cos(glm.radians(self.camera_rotation)) * self.camera_translation_speed * ts.seconds

    def calc_anti_sin_rotate(self, ts: Timestep):
        return math.sin(glm.radians(self.camera_rotation)) * self.camera_translation_speed * ts.seconds

    @HZ_PROFILE_FUNCTION
    def on_event(self, event: Event):
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(MouseScrolledEvent, self.on_mouse_scrolled)
        dispatcher.dispatch(WindowResizeEvent, self.on_window_resized)

    def on_resize(self, width: float, height: float) -> None:
        self.aspect_ratio = width/height
        self.set_camera_projection_matrix()

    @HZ_PROFILE_FUNCTION
    def on_mouse_scrolled(self, e: MouseScrolledEvent):
        self.zoom_level -= e.y_offset * 0.25
        self.zoom_level = max(self.zoom_level, 0.25)

        self.set_camera_projection_matrix()
        return False

    @HZ_PROFILE_FUNCTION
    def on_window_resized(self, e: WindowResizeEvent):
        if e.height == 0:
            return False

        self.on_resize(float(e.width), float(e.height))
        return False

    @HZ_PROFILE_FUNCTION
    def set_camera_projection_matrix(self):
        self.bounds.left = -self.aspect_ratio * self.zoom_level
        self.bounds.right = self.aspect_ratio * self.zoom_level
        self.bounds.bottom = -self.zoom_level
        self.bounds.top = self.zoom_level

        self.camera.set_projection_matrix(
            self.bounds.left,
            self.bounds.right,
            self.bounds.bottom,
            self.bounds.top
        )
