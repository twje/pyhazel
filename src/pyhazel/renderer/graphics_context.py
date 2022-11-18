from abc import ABC
from abc import abstractmethod

__all__ = ["GraphicsContent"]


class GraphicsContent(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def swap_buffers(self):
        pass
