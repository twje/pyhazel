from __future__ import annotations

from typing import TYPE_CHECKING
from pathlib import Path
from pyhazel.renderer.shader import Shader
from pyhazel.debug.instrumentor import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm


if TYPE_CHECKING:
    from numpy import ndarray

__all__ = ["OpenGLShader"]


def shader_type_from_string(shader_type: str) -> GLenum:
    if shader_type == "vertex":
        return GL_VERTEX_SHADER
    elif shader_type in ("fragment", "pixel"):
        return GL_FRAGMENT_SHADER

    assert False, "Unknown shader type"


class OpenGLShader(Shader):
    def __init__(self) -> None:
        super().__init__()
        self._renderer_id: int = -1
        self._name = ""

    @HZ_PROFILE_FUNCTION
    def destroy(self):
        pass
        # todo: wire up to parent class and implement

    @property
    def name(self):
        return self._name

    @classmethod
    @HZ_PROFILE_FUNCTION
    def create_from_filepath(cls, filepath: str):
        shader = cls()
        source = shader.read_file(filepath)
        shader_sources = shader.pre_process(source)
        shader._renderer_id = shader.compile(shader_sources)
        shader._name = Path(filepath).stem
        return shader

    @classmethod
    @HZ_PROFILE_FUNCTION
    def create_from_source(cls, name: str, vertex_src: str, fragment_src: str):
        shader_sources: dict[GLenum, str] = {
            GL_VERTEX_SHADER: vertex_src,
            GL_FRAGMENT_SHADER: fragment_src
        }
        shader = cls()
        shader._name = name
        shader._renderer_id = shader.compile(shader_sources)

        return shader

    @HZ_PROFILE_FUNCTION
    def read_file(self, filepath) -> str:
        source = ""
        try:
            with open(filepath, "r", encoding="utf-8") as fp:
                source = fp.read()
        except:
            print(f"Could not open file {filepath}")

        return source

    @HZ_PROFILE_FUNCTION
    def pre_process(self, source) -> dict[GLenum, str]:
        shader_sources: dict[GLenum, str] = {}
        is_parsing = False

        for line in (value.strip() for value in source.split("\n")):
            if line == "":
                continue

            if line.startswith("#type"):
                shader_type = shader_type_from_string(line.split(" ")[1])
                shader_sources[shader_type] = ""
                is_parsing = True
                continue

            if is_parsing:
                shader_sources[shader_type] += line + "\n"

        return shader_sources

    @HZ_PROFILE_FUNCTION
    def compile(self, shader_sources: dict[GLenum, str]) -> int:
        compiled_shaders = []
        for shader_type, source in shader_sources.items():
            compiled_shader = compileShader(
                source,
                shader_type
            )
            compiled_shaders.append(compiled_shader)

        _renderer_id = compileProgram(*compiled_shaders)
        glUseProgram(_renderer_id)

        return _renderer_id

    @HZ_PROFILE_FUNCTION
    def bind(self):
        glUseProgram(self._renderer_id)

    @HZ_PROFILE_FUNCTION
    def unbind(self):
        glUseProgram(0)

    @HZ_PROFILE_FUNCTION
    def set_int(self, name: str, value: int):
        self.upload_uniform_int(name, value)

    @HZ_PROFILE_FUNCTION
    def set_int_array(self, name: str, values: ndarray, count: int):
        self.upload_uniform_int_array(name, values, count)

    @HZ_PROFILE_FUNCTION
    def set_float(self, name: str, value: float):
        self.upload_uniform_float(name, value)

    @HZ_PROFILE_FUNCTION
    def set_float2(self, name: str, value: glm.vec2):
        self.upload_uniform_float2(name, value)

    @HZ_PROFILE_FUNCTION
    def set_float3(self, name: str, value: glm.vec3):
        self.upload_uniform_float3(name, value)

    @HZ_PROFILE_FUNCTION
    def set_float4(self, name: str, value: glm.vec4):
        self.upload_uniform_float4(name, value)

    @HZ_PROFILE_FUNCTION
    def set_mat4(self, name: str, value: glm.mat4):
        self.upload_uniform_mat4(name, value)

    def upload_uniform_int(self, name: str, value: int):
        self.bind()
        location = glGetUniformLocation(self._renderer_id, name)
        glUniform1i(location, value)

    # todo get np type
    def upload_uniform_int_array(self, name: str, values: ndarray, count: int):
        location = glGetUniformLocation(self._renderer_id, name)
        glUniform1iv(location, count, values)

    def upload_uniform_float(self, name: str, value: float):
        self.bind()
        location = glGetUniformLocation(self._renderer_id, name)
        glUniform1f(location, value)

    def upload_uniform_float2(self, name: str, value: glm.vec2):
        self.bind()
        location = glGetUniformLocation(self._renderer_id, name)
        glUniform2f(location, value.x, value.y)

    def upload_uniform_float3(self, name: str, value: glm.vec3):
        self.bind()
        location = glGetUniformLocation(self._renderer_id, name)
        glUniform3f(location, value.x, value.y, value.z)

    def upload_uniform_float4(self, name: str, value: glm.vec4):
        self.bind()
        location = glGetUniformLocation(self._renderer_id, name)
        glUniform4f(location, value.x, value.y, value.z, value.w)

    def upload_uniform_mat3(self, name: str, matrix: glm.mat3):
        self.bind()
        location = glGetUniformLocation(self._renderer_id, name)
        glUniformMatrix3fv(location, 1, GL_FALSE, glm.value_ptr(matrix))

    def upload_uniform_mat4(self, name: str, matrix: glm.mat4):
        self.bind()
        location = glGetUniformLocation(self._renderer_id, name)
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(matrix))
