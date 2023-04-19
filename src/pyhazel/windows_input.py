from .application import Application
from .input import Input
from pyhazel.key_codes import KeyCode
from pyhazel.mouse_codes import MouseCode
import glfw
import glm

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

    def get_mouse_position() -> glm.vec2:
        window = Application.instance.window.native_window
        return glm.vec2(glfw.get_cursor_pos(window))

    def get_mouse_x() -> int:
        return WindowsInput.get_mouse_position().x

    def get_mouse_y() -> int:
        return WindowsInput.get_mouse_position().y
