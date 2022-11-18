from .shader_data_type import ShaderDataType
from dataclasses import dataclass

__all__ = ["BufferElement"]


@dataclass
class BufferElement:
    s_type: ShaderDataType
    name: str
    offset: int = 0
    normalized: bool = False
