from .imgui_glfw_renderer import ImGuiGlfwRenderer
from .layer import Layer
from pyhazel.debug.instrumentor import *
import imgui


__all__ = ["ImGuiLayer"]


class ImGuiLayer(Layer):
    def __init__(self) -> None:
        super().__init__("ImGuiLayer")
        self.renderer: ImGuiGlfwRenderer = None

    @HZ_PROFILE_FUNCTION
    def on_attach(self):
        self.imgui_context = imgui.create_context()
        io = imgui.get_io()
        # io.backend_flags |= imgui.BACKEND_HAS_MOUSE_CURSORS
        # io.backend_flags |= imgui.BACKEND_HAS_SET_MOUSE_POS

        imgui.style_colors_dark()

        from .application import Application  # prevent circular import
        app = Application.instance
        self.renderer = ImGuiGlfwRenderer(app.window.native_window)

    @HZ_PROFILE_FUNCTION
    def on_detach(self):
        self.renderer.shutdown()
        imgui.destroy_context(self.imgui_context)

    @HZ_PROFILE_FUNCTION
    def begin(self):
        imgui.new_frame()

    @HZ_PROFILE_FUNCTION
    def end(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    @HZ_PROFILE_FUNCTION
    def on_imgui_render(self):
        self.renderer.process_inputs()
