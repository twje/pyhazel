from abc import ABC
from abc import abstractmethod
from enum import Enum
from enum import Flag
from enum import auto

__all__ = [
    "EventType",
    "EventCategory",
    "Event",
    "EventDispatcher"
]


class EventType(Enum):
    Null = auto()
    WindowClose = auto()
    WindowResize = auto()
    WindowFocus = auto()
    WindowLostFocus = auto()
    WindowMoved = auto()
    AppTick = auto()
    AppUpdate = auto()
    AppRender = auto()
    KeyPressed = auto()
    KeyReleased = auto()
    KeyTyped = auto()
    MouseButtonPressed = auto()
    MouseButtonReleased = auto()
    MouseMoved = auto()
    MouseScrolled = auto()


class EventCategory(Flag):
    Null = auto()
    EventCategoryApplication = auto()
    EventCategoryInput = auto()
    EventCategoryKeyboard = auto()
    EventCategoryMouse = auto()
    EventCategoryMouseButton = auto()


class Event(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.handled: bool = False

    def get_event_type(self) -> EventType:
        return type(self).get_static_type()

    @staticmethod
    @abstractmethod
    def get_static_type() -> EventType:
        pass

    @abstractmethod
    def get_category_flags() -> EventCategory:
        pass


class EventDispatcher:
    def __init__(self, event: Event) -> None:
        self.event = event

    def dispatch(self, event_type: Event, callback) -> bool:
        if self.event.get_event_type() == event_type.get_static_type():
            self.event.handled = callback(self.event)
            return True
        return False
