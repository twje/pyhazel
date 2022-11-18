from .application import Application
from .input import Input
import glfw

__all__ = ["WindowsInput"]


class WindowsInput(Input):
    def is_key_pressed_impl(self, keycode: int) -> bool:
        window = Application.instance.window.native_window
        state = glfw.get_key(window, keycode)
        return state == glfw.PRESS or state == glfw.REPEAT

    def is_mouse_button_pressed_impl(self, button: int) -> bool:
        window = Application.instance.window.native_window
        state = glfw.get_mouse_button(window, button)
        return state == glfw.PRESS

    def get_mouse_position_impl(self) -> tuple[int, int]:
        window = Application.instance.window.native_window
        return glfw.get_cursor_pos(window)

    def get_mouse_x_impl(self) -> int:
        x, _ = self.get_mouse_position_impl()
        return x

    def get_mouse_y_impl(self) -> int:
        _, y = self.get_mouse_position_impl()
        return y
