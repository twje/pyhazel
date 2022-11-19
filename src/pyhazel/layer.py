from __future__ import annotations

from typing import TYPE_CHECKING
from .events import Event

if TYPE_CHECKING:
    from .timestep import Timestep


class Layer:
    def __init__(self, name: str = "Layer") -> None:
        self.debug_name = name

    def destroy(self):
        pass

    def on_attach(self):
        pass

    def on_detach(self):
        pass

    def on_update(self, time_stamp: Timestep):
        pass

    def on_event(self, event: Event):
        pass

    def on_imgui_render(self):
        pass
