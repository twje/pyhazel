from .event import Event
from .event import EventType
from .event import EventCategory

__all__ = [
    "KeyPressedEvent",
    "KeyReleasedEvent",
]


class KeyEvent(Event):
    def __init__(self, keycode: int) -> None:
        super().__init__()
        self.keycode = keycode

    def get_category_flags() -> EventCategory:
        return EventCategory.EventCategoryKeyboard | EventCategory.EventCategoryInput


class KeyPressedEvent(KeyEvent):
    def __init__(self, keycode: int, repeat_count: int) -> None:
        super().__init__(keycode)
        self.repeat_count = repeat_count

    def get_static_type() -> EventType:
        return EventType.KeyPressed

    def __str__(self) -> str:
        return f"KeyTyped: {self.keycode}"


class KeyTypedEvent(KeyEvent):
    def __init__(self, keycode) -> None:
        super().__init__(keycode)

    def get_static_type() -> EventType:
        return EventType.KeyTyped

    def __str__(self) -> str:
        return f"KeyPressedEvent: {self.keycode} ({self.repeat_count} repeats)"


class KeyReleasedEvent(KeyEvent):
    def __init__(self, keycode) -> None:
        super().__init__(keycode)

    def get_static_type() -> EventType:
        return EventType.KeyReleased

    def __str__(self) -> str:
        return f"KeyReleasedEvent: {self.keycode}"
