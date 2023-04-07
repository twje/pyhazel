from .application import Application
from .input import Input
from pyhazel.key_codes import KeyCode
from pyhazel.mouse_codes import MouseCode
import glfw

__all__ = ["WindowsInput"]


class WindowsInput(Input):
    def is_key_pressed(keycode: KeyCode) -> bool:
        window = Application.instance.window.native_window
        state = glfw.get_key(window, int(keycode))
        return state == glfw.PRESS or state == glfw.REPEAT

    def is_mouse_button_pressed(button: MouseCode) -> bool:
        window = Application.instance.window.native_window
        state = glfw.get_mouse_button(window, int(button))
        return state == glfw.PRESS

    def get_mouse_position() -> tuple[int, int]:
        window = Application.instance.window.native_window
        return glfw.get_cursor_pos(window)

    def get_mouse_x() -> int:
        x, _ = WindowsInput.get_mouse_position()
        return x

    def get_mouse_y() -> int:
        _, y = WindowsInput.get_mouse_position()
        return y
