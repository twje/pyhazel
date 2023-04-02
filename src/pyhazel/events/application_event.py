from .event import Event
from .event import EventType
from .event import EventCategory

__all__ = [
    "WindowResizeEvent",
    "WindowCloseEvent",
    "AppTickEvent",
    "AppUpdateEvent",
    "AppRenderEvent",
]


class WindowResizeEvent(Event):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.width = width
        self.height = height

    @staticmethod
    def get_static_type() -> EventType:
        return EventType.WindowResize

    @staticmethod
    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryApplication

    def __str__(self) -> str:
        return f"WindowResizeEvent: {self.width}, {self.height}"


class WindowCloseEvent(Event):
    @staticmethod
    def get_static_type() -> EventType:
        return EventType.WindowClose

    @staticmethod
    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryApplication

    def __str__(self) -> str:
        return f"WindowCloseEvent"


class AppTickEvent(Event):
    def get_static_type() -> EventType:
        return EventType.AppTick

    @staticmethod
    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryApplication

    def __str__(self) -> str:
        return f"AppTickEvent"


class AppUpdateEvent(Event):
    @staticmethod
    def get_static_type() -> EventType:
        return EventType.AppUpdate

    @staticmethod
    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryApplication

    def __str__(self) -> str:
        return f"AppUpdateEvent"


class AppRenderEvent(Event):
    @staticmethod
    def get_static_type() -> EventType:
        return EventType.AppRender

    @staticmethod
    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryApplication

    def __str__(self) -> str:
        return f"AppRenderEvent"
