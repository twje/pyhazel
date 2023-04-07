from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from .key_codes import KeyCode
from .mouse_codes import MouseCode
from .config import *

__all__ = ["Input"]


class Input(ABC):
    # ----------
    # Client API
    # ----------
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
    def get_mouse_position() -> tuple[int, int]:
        pass

    @staticmethod
    @abstractmethod
    def get_mouse_x() -> int:
        pass

    @staticmethod
    @abstractmethod
    def get_mouse_y() -> int:
        pass
