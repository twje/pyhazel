from __future__ import annotations

from .shader import Shader

__all__ = ["ShaderLibrary"]


class ShaderLibrary:
    def __init__(self) -> None:
        self.shaders = {}

    def add(self, name: str | None, shader: Shader) -> None:
        assert not self.exists(name), "Shader already exists!"
        if name is None:
            name = shader.name
        self.shaders[name] = shader

    def load(self, name: str | None, filepath: str) -> Shader:
        shader = Shader.create_from_file(filepath)
        self.add(name, shader)
        return shader

    def __getitem__(self, name: str):
        assert self.exists(name), "Shader not found!"
        return self.shaders[name]

    def exists(self, name: str):
        return name in self.shaders
