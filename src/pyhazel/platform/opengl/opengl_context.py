from pyhazel.renderer import GraphicsContent
from pyhazel.debug.instrumentor import *
from OpenGL.GL import *
import glfw

__all__ = ["OpenGLContent"]


class OpenGLContent(GraphicsContent):
    def __init__(self, window_handle) -> None:
        super().__init__()
        self.window_handle = window_handle

    @HZ_PROFILE_FUNCTION
    def init(self):
        glfw.make_context_current(self.window_handle)
        print("OpenGL Info:")
        print(f"   Vendor: {glGetString(GL_VENDOR).decode('ascii')}")
        print(f"   Renderer: {glGetString(GL_RENDERER).decode('ascii')}")
        print(f"   Version: {glGetString(GL_VERSION).decode('ascii')}")

    @HZ_PROFILE_FUNCTION
    def swap_buffers(self):
        glfw.swap_buffers(self.window_handle)
