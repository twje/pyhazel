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
import glfw


class Application:
    instance = None

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

    def run(self):
        while self.running:
            time = glfw.get_time()
            timestamp = Timestep(time - self.last_frame_time)
            self.last_frame_time = time

            if not self.minimized:
                for layer in self.layer_stack:
                    layer.on_update(timestamp)

            self.imgui_layer.begin()
            for layer in self.layer_stack:
                layer.on_imgui_render()
            self.imgui_layer.end()

            self.window.on_update()

    def destroy(self):
        """This method replicates the semantics a C/C++ destructor."""
        pass

    def on_event(self, event: Event) -> None:
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(WindowCloseEvent, self.on_window_close)
        dispatcher.dispatch(WindowResizeEvent, self.on_window_resize)

        for layer in reversed(self.layer_stack):
            layer.on_event(event)
            if event.handled:
                break

    def push_layer(self, layer: Layer):
        self.layer_stack.push_layer(layer)

    def push_overlay(self, layer: Layer):
        self.layer_stack.push_overlay(layer)

    def on_window_close(self, event: WindowCloseEvent) -> bool:
        self.running = False
        return True

    def on_window_resize(self, event: WindowResizeEvent) -> bool:
        if event.width == 0 or event.height == 0:
            self.minimized = True
            return False

        self.minimized = False
        Renderer.on_window_resize(event.width, event.height)

        return False
