from pyhazel.renderer.shader import Shader
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm


__all__ = ["OpenGLShader"]


class OpenGLShader(Shader):
    def __init__(self, vertex_src: str, fragment_src: str) -> None:
        self.renderer_id = compileProgram(
            compileShader(
                vertex_src,
                GL_VERTEX_SHADER
            ),
            compileShader(
                fragment_src,
                GL_FRAGMENT_SHADER
            ),
        )
        glUseProgram(self.renderer_id)

    def bind(self):
        glUseProgram(self.renderer_id)

    def unbind(self):
        glUseProgram(0)

    def upload_uniform_int(self, name: str, value: int):
        self.bind()
        location = glGetUniformLocation(self.renderer_id, name)
        glUniform1i(location, value)

    def upload_uniform_float(self, name: str, value: float):
        self.bind()
        location = glGetUniformLocation(self.renderer_id, name)
        glUniform1f(location, value)

    def upload_uniform_float2(self, name: str, value: glm.vec2):
        self.bind()
        location = glGetUniformLocation(self.renderer_id, name)
        glUniform2f(location, value.x, value.y)

    def upload_uniform_float3(self, name: str, value: glm.vec3):
        self.bind()
        location = glGetUniformLocation(self.renderer_id, name)
        glUniform3f(location, value.x, value.y, value.z)

    def upload_uniform_float4(self, name: str, value: glm.vec4):
        self.bind()
        location = glGetUniformLocation(self.renderer_id, name)
        glUniform4f(location, value.x, value.y, value.z, value.w)

    def upload_uniform_mat3(self, name: str, matrix: glm.mat3):
        self.bind()
        location = glGetUniformLocation(self.renderer_id, name)
        glUniformMatrix3fv(location, 1, GL_FALSE, glm.value_ptr(matrix))

    def upload_uniform_mat4(self, name: str, matrix: glm.mat4):
        self.bind()
        location = glGetUniformLocation(self.renderer_id, name)
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(matrix))
