from .event import Event
from .event import EventType
from .event import EventCategory
from pyhazel.mouse_codes import MouseCode

__all__ = [
    "MouseMovedEvent",
    "MouseScrolledEvent",
    "MouseButtonPressedEvent",
    "MouseButtonReleasedEvent"
]


class MouseMovedEvent(Event):
    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.mouse_x = x
        self.mouse_y = y

    @staticmethod
    def get_static_type() -> EventType:
        return EventType.MouseMoved

    @staticmethod
    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryMouse | EventCategory.EventCategoryInput

    def __str__(self) -> str:
        return f"MouseMovedEvent: {self.mouse_x}, {self.mouse_y}"


class MouseScrolledEvent(Event):
    def __init__(self, x_offset: float, y_offset: float) -> None:
        super().__init__()
        self.x_offset = x_offset
        self.y_offset = y_offset

    @staticmethod
    def get_static_type() -> EventType:
        return EventType.MouseScrolled

    @staticmethod
    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryMouse | EventCategory.EventCategoryInput

    def __str__(self) -> str:
        return f"MouseScrolledEvent: {self.x_offset}, {self.y_offset}"


class MouseButtonEvent(Event):
    def __init__(self, button: MouseCode) -> None:
        super().__init__()
        self.button: MouseCode = button

    @staticmethod
    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryMouseButton | EventCategory.EventCategoryInput


class MouseButtonPressedEvent(MouseButtonEvent):
    def __init__(self, button: MouseCode) -> None:
        super().__init__(button)

    @staticmethod
    def get_static_type() -> EventType:
        return EventType.MouseButtonPressed

    def __str__(self) -> str:
        return f"MouseButtonPressedEvent: {self.button}"


class MouseButtonReleasedEvent(MouseButtonEvent):
    def __init__(self, button: MouseCode) -> None:
        super().__init__(button)

    @staticmethod
    def get_static_type() -> EventType:
        return EventType.MouseButtonReleased

    def __str__(self) -> str:
        return f"MouseButtonReleasedEvent: {self.button}"
