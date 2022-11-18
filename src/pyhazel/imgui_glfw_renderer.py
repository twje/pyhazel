from types import SimpleNamespace
from imgui.integrations.glfw import GlfwRenderer
import glfw


__all__ = ["ImGuiGlfwRenderer"]


class ImGuiGlfwRenderer(GlfwRenderer):
    """
    This is an ImGUI GLFW adapter class to propogate glfw events to previous event handlers.
    """

    def __init__(self, window, install_callbacks=True):
        super().__init__(window, False)
        self.window = window
        self.install_callbacks = install_callbacks
        self.callback_registry = {}

        self.register_callbacks()

    def register_callback(self, callback_registrator, callback):
        previous_callback = callback_registrator(
            self.window,
            callback
        )

        self.callback_registry[callback] = SimpleNamespace(
            callback_registrator=callback_registrator,
            previous_callback=previous_callback
        )

    def register_callbacks(self):
        self.register_callback(
            glfw.set_key_callback,
            self.keyboard_callback_adapter
        )
        self.register_callback(
            glfw.set_cursor_pos_callback,
            self.mouse_callback_adapter
        )
        self.register_callback(
            glfw.set_window_size_callback,
            self.resize_callback_adapter
        )
        self.register_callback(
            glfw.set_char_callback,
            self.char_callback_adapter
        )
        self.register_callback(
            glfw.set_scroll_callback,
            self.scroll_callback_adapter
        )

    def get_previous_callback(self, key):
        if not self.install_callbacks:
            return self.null_callback

        item = self.callback_registry.get(key)
        if item is None:
            return self.null_callback

        previous_callback = item.previous_callback
        if previous_callback is None:
            return self.null_callback

        return previous_callback

    def null_callback(self, *args, **kwargs):
        pass

    def shutdown(self):
        for item in self.callback_registry.values():
            callback_registrator = item.callback_registrator
            previous_callback = item.previous_callback

            if self.install_callbacks:
                callback_registrator(self.window, previous_callback)
            else:
                callback_registrator(self.window, None)

        super().shutdown()

    # -----------------
    # Callbacks Methods
    # -----------------
    def keyboard_callback_adapter(self, window, key, scancode, action, mods):
        super().keyboard_callback(window, key, scancode, action, mods)

        callback = self.get_previous_callback(self.keyboard_callback_adapter)
        callback(window, key, scancode, action, mods)

    def char_callback_adapter(self, window, char):
        super().char_callback(window, char)

        callback = self.get_previous_callback(self.char_callback_adapter)
        callback(window, char)

    def resize_callback_adapter(self, window, width, height):
        super().resize_callback(window, width, height)

        callback = self.get_previous_callback(self.resize_callback_adapter)
        callback(window, width, height)

    def mouse_callback_adapter(self, *args, **kwargs):
        super().mouse_callback(*args, **kwargs)

        callback = self.get_previous_callback(self.mouse_callback_adapter)
        callback(*args, **kwargs)

    def scroll_callback_adapter(self, window, x_offset, y_offset):
        super().scroll_callback(window, x_offset, y_offset)

        callback = self.get_previous_callback(self.scroll_callback_adapter)
        callback(window, x_offset, y_offset)
