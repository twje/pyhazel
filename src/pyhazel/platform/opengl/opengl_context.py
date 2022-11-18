from pyhazel.renderer import GraphicsContent
from OpenGL.GL import *
import glfw

__all__ = ["OpenGLContent"]


class OpenGLContent(GraphicsContent):
    def __init__(self, window_handle) -> None:
        super().__init__()
        self.window_handle = window_handle

    def init(self):
        glfw.make_context_current(self.window_handle)
        print("OpenGL Info:")
        print(f"   Vendor: {glGetString(GL_VENDOR)}")
        print(f"   Renderer: {glGetString(GL_RENDERER)}")
        print(f"   Version: {glGetString(GL_VERSION)}")

    def swap_buffers(self):
        glfw.swap_buffers(self.window_handle)
