from dataclasses import dataclass


from .window import Window
from .window import EventCallbackType
from .window import WindowProps
from .events import WindowCloseEvent
from .events import WindowResizeEvent
from .events import KeyPressedEvent
from .events import KeyReleasedEvent
from .events import MouseButtonPressedEvent
from .events import MouseButtonReleasedEvent
from .events import MouseMovedEvent
from .events import MouseScrolledEvent
from .events.key_event import KeyTypedEvent
from .platform.opengl import OpenGLContent
from pyhazel.key_codes import KeyCode
from pyhazel.mouse_codes import MouseCode
from pyhazel.debug.instrumentor import *
from .config import *
import glfw


def glfw_error_callback(error: int, description: str):
    # todo: log instead
    print(f"GLFW Error ({error}: {description})")


class WindowsWindow(Window):
    is_glfw_initialized = False

    @dataclass
    class WindowData:
        title: str
        width: int
        height: int

        is_vsync: bool = False
        event_callback: EventCallbackType = None

    @HZ_PROFILE_FUNCTION
    def __init__(self, props: WindowProps) -> None:
        super().__init__()
        self.data = self.WindowData(
            props.title,
            props.width,
            props.height
        )

        # todo: log instead
        print(f"Creating window {props.title} ({props.width}, {props.height})")

        # ensure glfw is initialized only once
        if not self.is_glfw_initialized:
            HZ_PROFILE_SCOPE("glfwInit")
            if not glfw.init():
                raise Exception("glfw can not be initialized")
            glfw.set_error_callback(glfw_error_callback)
            self.is_glfw_initialized = True

        HZ_PROFILE_SCOPE("glfwCreateWindow")
        if DEBUG:
            glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, glfw.TRUE)

        self.window = glfw.create_window(
            props.width,
            props.height,
            props.title,
            None,
            None
        )

        self.context = OpenGLContent(self.window)
        self.context.init()

        if not self.window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        glfw.make_context_current(self.window)
        glfw.set_window_user_pointer(self.window, self.data)
        self.glfw_callbacks()
        self.is_vsync = True

    @HZ_PROFILE_FUNCTION
    def destroy(self):
        """This method replicates the semantics a C/C++ destructor."""
        # Todo: propogate destroy to clean up resources before exiiting application
        pass

    def glfw_callbacks(self):
        glfw.set_window_size_callback(self.window, self.window_size_callback)
        glfw.set_window_close_callback(self.window, self.window_close_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_pos_callback)
        glfw.set_char_callback(self.window, self.char_callback)

    def set_event_callback(self, event_callback: EventCallbackType) -> None:
        self.data.event_callback = event_callback

    @HZ_PROFILE_FUNCTION
    def on_update(self) -> None:
        glfw.poll_events()
        self.context.swap_buffers()

    @property
    def width(self):
        return self.data.width

    @property
    def height(self):
        return self.data.height

    @property
    def is_vsync(self) -> bool:
        return self.data.is_vsync

    @is_vsync.setter
    @HZ_PROFILE_FUNCTION
    def is_vsync(self, value: bool):
        if value:
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

        self.data.is_vsync = value

    @property
    def native_window(self) -> bool:
        return self.window

    @HZ_PROFILE_FUNCTION
    def shutdown(self):
        glfw.destroy_window(self.window)

    def destroy(self):
        self.shutdown()

    # --------------
    # GLFW Callbacks
    # --------------
    def window_size_callback(self, window: glfw._GLFWwindow, width: int, height: int):
        data = glfw.get_window_user_pointer(window)
        data.width = width
        data.height = height

        event = WindowResizeEvent(width, height)
        data.event_callback(event)

    def window_close_callback(self, window: glfw._GLFWwindow):
        data = glfw.get_window_user_pointer(window)
        event = WindowCloseEvent()
        data.event_callback(event)

    def key_callback(self, window: glfw._GLFWwindow, key: int, scancode: int, action: int, mods: int):
        data = glfw.get_window_user_pointer(window)

        if action == glfw.PRESS:
            event = KeyPressedEvent(KeyCode(key), 0)
            data.event_callback(event)
        elif action == glfw.RELEASE:
            event = KeyReleasedEvent(KeyCode(key))
            data.event_callback(event)
        elif action == glfw.REPEAT:
            event = KeyPressedEvent(KeyCode(key), 1)
            data.event_callback(event)

    def mouse_button_callback(self, window: glfw._GLFWwindow, button: int, action: int, mods: int):
        data = glfw.get_window_user_pointer(window)

        if action == glfw.PRESS:
            event = MouseButtonPressedEvent(MouseCode(button))
            data.event_callback(event)
        elif action == glfw.RELEASE:
            event = MouseButtonReleasedEvent(MouseCode(button))
            data.event_callback(event)

    def scroll_callback(self, window: glfw._GLFWwindow, x_offset: float, y_offset: float):
        data = glfw.get_window_user_pointer(window)
        event = MouseScrolledEvent(x_offset, y_offset)
        data.event_callback(event)

    def cursor_pos_callback(self, window: glfw._GLFWwindow, x_pos: float, y_pos: float):
        data = glfw.get_window_user_pointer(window)
        event = MouseMovedEvent(x_pos, y_pos)
        data.event_callback(event)

    def char_callback(self,  window: glfw._GLFWwindow, key: int):
        data = glfw.get_window_user_pointer(window)
        event = KeyTypedEvent(KeyCode(key))
        data.event_callback(event)
