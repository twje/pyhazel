from abc import ABC
from abc import abstractmethod
from .key_codes import KeyCode
from .mouse_codes import MouseCode

__all__ = ["Input"]


class Input(ABC):
    instance: "Input" = None

    @classmethod
    def init_singleton(cls) -> "Input":
        assert cls.instance is None
        from .windows_input import WindowsInput
        cls.instance = WindowsInput()

    # ----------
    # Client API
    # ----------
    @classmethod
    def is_key_pressed(cls, keycode: KeyCode) -> bool:
        return cls.instance.is_key_pressed_impl(keycode)

    @classmethod
    def is_mouse_button_pressed(cls, button: MouseCode) -> bool:
        return cls.instance.is_mouse_button_pressed_impl(button)

    @classmethod
    def get_mouse_position(cls) -> tuple[int, int]:
        return cls.instance.get_mouse_position_impl()

    @classmethod
    def get_mouse_x(cls) -> int:
        return cls.instance.get_mouse_x_impl()

    @classmethod
    def get_mouse_y(cls) -> int:
        return cls.instance.get_mouse_y_impl()

    # ----------------
    # Abstract Methods
    # ----------------
    @abstractmethod
    def is_key_pressed_impl(self, keycode: KeyCode) -> bool:
        pass

    @abstractmethod
    def is_mouse_button_pressed_impl(self, button: MouseCode) -> bool:
        pass

    @abstractmethod
    def get_mouse_position_impl(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_mouse_x_impl(self) -> int:
        pass

    @abstractmethod
    def get_mouse_y_impl(self) -> int:
        pass


Input.init_singleton()
