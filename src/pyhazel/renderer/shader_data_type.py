from typing import Optional
from enum import Enum


__all__ = ["ShaderDataType"]


class ShaderDataType(Enum):
    NONE = None, None
    FLOAT = 4, 1
    FLOAT2 = 4 * 2, 2
    FLOAT3 = 4 * 3, 3
    FLOAT4 = 4 * 4, 4
    MAT3 = 4 * 3 * 3, 3  # 3* float3
    MAT4 = 4 * 4 * 4, 4  # 4* float4
    INT = 4, 1
    INT2 = 4 * 2, 2
    INT3 = 4 * 3, 3
    INT4 = 4 * 4, 4
    BOOL = 1, 1

    def __init__(self, size: Optional[int], count: Optional[int]):
        self.size = size
        self.count = count
