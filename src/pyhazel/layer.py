from .events import Event


class Layer:
    def __init__(self, name: str = "Layer") -> None:
        self.debug_name = name

    def destroy(self):
        pass

    def on_attach(self):
        pass

    def on_detach(self):
        pass

    def on_update(self):
        pass

    def on_event(self, event: Event):
        pass

    def on_imgui_render(self):
        pass
