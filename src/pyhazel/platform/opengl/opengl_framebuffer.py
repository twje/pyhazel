from pyhazel.renderer.framebuffer import FramebufferSpecification
from pyhazel.renderer.framebuffer import Framebuffer
from OpenGL.GL import *
import numpy as np


class OpenGLFramebuffer(Framebuffer):
    MAX_FRAMEBUFFER_SIZE = 8192

    def __init__(self, sepcification: FramebufferSpecification) -> None:
        super().__init__()
        self._sepcification = sepcification

        self.renderer_id = np.array([0], dtype=np.uint32)
        self.color_attachement = np.array([0], dtype=np.uint32)
        self.depth_attachement = np.array([0], dtype=np.uint32)

        self.invalidate()

    def cleanup(self):
        glDeleteFramebuffers(1, self.renderer_id[0])
        glDeleteTextures(1, self.color_attachement[0])
        glDeleteTextures(1, self.depth_attachement[0])

    @property
    def color_attachment_renderer_id(self) -> int:
        return self.color_attachement[0]

    @property
    def specification(self) -> FramebufferSpecification:
        return self._sepcification

    def invalidate(self):
        if self.renderer_id[0] != 0:
            self.cleanup()

        self.renderer_id = np.empty(1, dtype=np.uint32)
        glCreateFramebuffers(1, self.renderer_id)
        glBindFramebuffer(GL_FRAMEBUFFER, self.renderer_id[0])

        glCreateTextures(GL_TEXTURE_2D, 1, self.color_attachement)
        glBindTexture(GL_TEXTURE_2D, self.color_attachement[0])
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA8,
            self.specification.width,
            self.specification.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            None
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glFramebufferTexture2D(
            GL_FRAMEBUFFER,
            GL_COLOR_ATTACHMENT0,
            GL_TEXTURE_2D,
            self.color_attachement[0],
            0
        )

        glCreateTextures(GL_TEXTURE_2D, 1, self.depth_attachement)
        glBindTexture(GL_TEXTURE_2D, self.depth_attachement[0])
        glTexStorage2D(
            GL_TEXTURE_2D,
            1,
            GL_DEPTH24_STENCIL8,
            self.specification.width,
            self.specification.height,
        )
        glFramebufferTexture2D(
            GL_FRAMEBUFFER,
            GL_DEPTH_STENCIL_ATTACHMENT,
            GL_TEXTURE_2D,
            self.depth_attachement[0],
            0
        )

        assert glCheckFramebufferStatus(
            GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.renderer_id[0])
        glViewport(0, 0, self.specification.width, self.specification.height)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def resize(self, width: int, height: int):
        if width == 0 or height == 0 or width > self.MAX_FRAMEBUFFER_SIZE or height > self.MAX_FRAMEBUFFER_SIZE:
            # todo: convert to log statement
            print(f"Attempted to rezize framebuffer to {width}, {height}")
            return

        self.specification.width = width
        self.specification.height = height

        self.invalidate()
