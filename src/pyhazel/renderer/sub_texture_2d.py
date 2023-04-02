from __future__ import annotations
from typing import TYPE_CHECKING
import glm

if TYPE_CHECKING:
    from pyhazel.renderer import Texture2D


class SubTexture2D:
    def __init__(self, texture: Texture2D, min: glm.vec2, max: glm.vec2) -> None:
        self.texture = texture
        self.tex_coords = [
            glm.vec2(min.x, min.y),
            glm.vec2(max.x, min.y),
            glm.vec2(max.x, max.y),
            glm.vec2(min.x, max.y),
        ]

    @classmethod
    def create_from_coords(cls, texture: Texture2D, coords: glm.vec2, cell_size: glm.vec2, sprite_size=glm.vec2(1, 1)):
        min = glm.vec2(
            (coords.x * cell_size.x) / texture.width,
            (coords.y * cell_size.y) / texture.height
        )
        max = glm.vec2(
            ((coords.x + sprite_size.x) * cell_size.x) / texture.width,
            ((coords.y + sprite_size.y) * cell_size.y) / texture.height
        )
        return cls(texture, min, max)
