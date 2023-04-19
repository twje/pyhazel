from __future__ import annotations
from typing import Optional
from abc import ABC
from abc import abstractmethod
from .key_codes import KeyCode
from .mouse_codes import MouseCode
from .config import *
import glm

__all__ = ["Input"]


class BaseInput(ABC):
    @staticmethod
    @abstractmethod
    def is_key_pressed(keycode: KeyCode) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def is_mouse_button_pressed(button: MouseCode) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def get_mouse_position() -> glm.vec2:
        pass

    @staticmethod
    @abstractmethod
    def get_mouse_x() -> int:
        pass

    @staticmethod
    @abstractmethod
    def get_mouse_y() -> int:
        pass


class Input(ABC):
    instance: Optional[BaseInput] = None

    @staticmethod
    def create():
        from pyhazel.windows_input import WindowsInput
        Input.instance = WindowsInput

    @staticmethod
    def is_key_pressed(keycode: KeyCode) -> bool:
        return Input.instance.is_key_pressed(keycode)

    @staticmethod
    def is_mouse_button_pressed(button: MouseCode) -> bool:
        return Input.instance.is_mouse_button_pressed(button)

    @staticmethod
    def get_mouse_position() -> glm.vec2:
        return Input.instance.get_mouse_position()

    @staticmethod
    def get_mouse_x() -> int:
        return Input.instance.get_mouse_x()

    @staticmethod
    def get_mouse_y() -> int:
        return Input.instance.get_mouse_y()


Input.create()
