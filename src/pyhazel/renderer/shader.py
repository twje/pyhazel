from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *

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
