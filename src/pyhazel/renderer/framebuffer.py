from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pyhazel.renderer import RendererAPI


@dataclass
class FramebufferSpecification:
    width: int = 0
    height: int = 0
    samples: int = 1
    swap_chain_target: bool = False


class Framebuffer(ABC):
    @classmethod
    def create(cls, spec: FramebufferSpecification) -> Framebuffer:
        if RendererAPI.api == RendererAPI.API.NONE:
            print("RendererAPI.API.NONE is not supported")
            return
        elif RendererAPI.api == RendererAPI.API.OpenGL:
            from pyhazel.platform.opengl import OpenGLFramebuffer
            return OpenGLFramebuffer(spec)

        assert False, "Framebuffer type is undefined"

    @property
    @abstractmethod
    def color_attachment_renderer_id(self) -> int:
        pass

    @property
    @abstractmethod
    def specification(self) -> FramebufferSpecification:
        pass

    @abstractmethod
    def bind(self):
        pass

    @abstractmethod
    def unbind(self):
        pass

    @abstractmethod
    def resize(self, width: int, height: int):
        pass
