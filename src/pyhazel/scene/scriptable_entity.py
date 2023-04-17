from typing import TYPE_CHECKING
from typing import Optional
from typing import TypeVar
from pyhazel.timestep import Timestep

if TYPE_CHECKING:
    from pyhazel.scene.entity import Entity


__name__ = ["ScriptableEntity"]


T = TypeVar("T")


class ScriptableEntity:
    def __init__(self) -> None:
        self.entity: Optional[Entity] = None

    def get_component(self, component_type: type[T]) -> T:
        return self.entity.get_component(component_type)

    # -----
    # Hooks
    # -----
    def on_create(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def on_update(self, ts: Timestep) -> None:
        pass
