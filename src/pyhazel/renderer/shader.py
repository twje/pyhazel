from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *
import glm

__all__ = ["Shader"]


class Shader:
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

    def upload_uniform_mat4(self, name: str, matrix: glm.mat4):
        location = glGetUniformLocation(self.renderer_id, name)
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(matrix))
