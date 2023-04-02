from .events import Event
from .events import EventDispatcher
from .events import WindowCloseEvent
from .events import WindowResizeEvent
from .window import Window
from .layer_stack import LayerStack
from .imgui_layer import ImGuiLayer
from .layer import Layer
from .timestep import Timestep
from .renderer import Renderer
from pyhazel.debug.instrumentor import *
import glfw


class Application:
    instance = None

    @HZ_PROFILE_FUNCTION
    def __init__(self) -> None:
        # Singleton (explore more pythonic options)
        assert Application.instance is None
        Application.instance = self

        self.window = Window.create()
        self.window.set_event_callback(self.on_event)
        self.layer_stack = LayerStack()
        self.running = True
        self.minimized = False
        self.last_frame_time = 0

        Renderer.init()

        self.imgui_layer = ImGuiLayer()
        self.push_overlay(self.imgui_layer)

    @HZ_PROFILE_FUNCTION
    def destroy(self):
        """This method replicates the semantics a C/C++ destructor."""
        # Todo: propogate destroy to clean up resources before exiiting application
        pass

    @HZ_PROFILE_FUNCTION
    def run(self):
        while self.running:
            with HZ_PROFILE_SCOPE("RunLoop"):
                time = glfw.get_time()
                timestamp = Timestep(time - self.last_frame_time)
                self.last_frame_time = time

                if not self.minimized:
                    with HZ_PROFILE_SCOPE("LayerStack OnUpdate"):
                        for layer in self.layer_stack:
                            layer.on_update(timestamp)

                self.imgui_layer.begin()
                with HZ_PROFILE_SCOPE("LayerStack OnImGuiRender"):
                    for layer in self.layer_stack:
                        layer.on_imgui_render()
                self.imgui_layer.end()

                self.window.on_update()

    @HZ_PROFILE_FUNCTION
    def on_event(self, event: Event) -> None:
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(WindowCloseEvent, self.on_window_close)
        dispatcher.dispatch(WindowResizeEvent, self.on_window_resize)

        for layer in reversed(self.layer_stack):
            if event.handled:
                break
            layer.on_event(event)

    @HZ_PROFILE_FUNCTION
    def push_layer(self, layer: Layer):
        self.layer_stack.push_layer(layer)

    @HZ_PROFILE_FUNCTION
    def push_overlay(self, layer: Layer):
        self.layer_stack.push_overlay(layer)

    def on_window_close(self, event: WindowCloseEvent) -> bool:
        self.running = False
        return True

    @HZ_PROFILE_FUNCTION
    def on_window_resize(self, event: WindowResizeEvent) -> bool:
        if event.width == 0 or event.height == 0:
            self.minimized = True
            return False

        self.minimized = False
        Renderer.on_window_resize(event.width, event.height)

        return False
