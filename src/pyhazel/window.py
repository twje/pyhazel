
from abc import ABC
from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from .events import Event


__all__ = [
    "Window",
    "EventCallbackType",
    "WindowProps"
]

EventCallbackType = Callable[[Event], bool]


@dataclass
class WindowProps:
    title: str = "Hazel Engine"
    width: int = 1280
    height: int = 720


class Window(ABC):
    @staticmethod
    def create(window_props: WindowProps = WindowProps()) -> "Window":
        # avoid circular reference
        from .windows_window import WindowsWindow
        return WindowsWindow(window_props)

    @abstractmethod
    def set_event_callback(self, event_callback: EventCallbackType) -> None:
        pass

    @abstractmethod
    def on_update(self) -> None:
        pass

    @property
    @abstractmethod
    def width(self):
        pass

    @property
    @abstractmethod
    def height(self):
        pass

    @property
    @abstractmethod
    def is_vsync(self) -> bool:
        pass

    @is_vsync.setter
    @abstractmethod
    def is_vsync(self, value: bool):
        pass

    @property
    @abstractmethod
    def native_window(self) -> bool:
        pass
