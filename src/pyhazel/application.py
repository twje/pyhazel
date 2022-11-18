from .events import Event
from .events import EventDispatcher
from .events import WindowCloseEvent
from .window import Window
from .layer_stack import LayerStack
from .imgui_layer import ImGuiLayer
from .layer import Layer
from OpenGL.GL import *
from .renderer import VertexArray
from .renderer import VertexBuffer
from .renderer import BufferLayout
from .renderer import BufferElement
from .renderer import IndexBuffer
from .renderer import ShaderDataType
from .renderer import Shader
from .renderer import Renderer
from .renderer import RenderCommand
import numpy as np


class Application:
    instance = None

    def __init__(self) -> None:
        # Singleton (explore more pythonic options)
        assert Application.instance is None
        Application.instance = self

        self.window = Window.create()
        self.window.set_event_callback(self.on_event)
        self.layer_stack = LayerStack()
        self.running = True

        self.imgui_layer = ImGuiLayer()
        self.push_overlay(self.imgui_layer)

        # -------------------------------
        # Renderer Setup (todo: refactor)
        # -------------------------------
        # VAO 1
        self.vertex_array = VertexArray.create()

        vertices = np.array([
            -0.5, -0.5, 0.0, 0.8, 0.2, 0.8, 1.0,
            0.5, -0.5, 0.0, 0.2, 0.3, 0.8, 1.0,
            0.0,  0.5, 0.0, 0.8, 0.8, 0.2, 1.0
        ], dtype=np.float32)

        vertex_buffer = VertexBuffer.create(vertices)
        vertex_buffer.buffer_layout = BufferLayout(
            BufferElement(ShaderDataType.FLOAT3, "a_Position"),
            BufferElement(ShaderDataType.FLOAT4, "a_Color"),
        )
        self.vertex_array.add_vertex_buffer(vertex_buffer)

        indices = np.array([0, 1, 2], dtype=np.uint32)
        index_buffer = IndexBuffer.create(indices)
        self.vertex_array.index_buffer = index_buffer

        # VAO 2
        self.square_vertex_array = VertexArray.create()

        self.square_vertices = np.array([
            -0.75, -0.75, 0.0,
            0.75, -0.75, 0.0,
            0.75,  0.75, 0.0,
            -0.75,  0.75, 0.0
        ], dtype=np.float32)

        self.square_vertex_buffer = VertexBuffer.create(self.square_vertices)
        self.square_vertex_buffer.buffer_layout = BufferLayout(
            BufferElement(ShaderDataType.FLOAT3, "a_Position")
        )
        self.square_vertex_array.add_vertex_buffer(self.square_vertex_buffer)

        square_indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        square_index_buffer = IndexBuffer.create(square_indices)
        self.square_vertex_array.index_buffer = square_index_buffer

        # shaders
        vertex_src = """
            #version 330 core
			
			layout(location = 0) in vec3 a_Position;
			layout(location = 1) in vec4 a_Color;

			out vec3 v_Position;
			out vec4 v_Color;

			void main()
			{
				v_Position = a_Position;
				v_Color = a_Color;
				gl_Position = vec4(a_Position, 1.0);
			}
        """

        fragment_src = """
            #version 330 core
			
			layout(location = 0) out vec4 color;
			
			in vec3 v_Position;
			in vec4 v_Color;

			void main()
			{
                //color = vec4(1, 1, 1, 1);
				color = vec4(v_Position * 0.5 + 0.5, 1.0);
				color = v_Color;
			}
        """

        self.shader = Shader(vertex_src, fragment_src)

        square_vertex_src = """
            #version 330 core
			
			layout(location = 0) in vec3 a_Position;

			out vec3 v_Position;

			void main()
			{
				v_Position = a_Position;
				gl_Position = vec4(a_Position, 1.0);	
			}
        """

        square_fragment_src = """
            #version 330 core
			
			layout(location = 0) out vec4 color;

			in vec3 v_Position;

			void main()
			{
				color = vec4(0.2, 0.3, 0.8, 1.0);
			}
        """

        self.blue_shader = Shader(square_vertex_src, square_fragment_src)

    def run(self):
        while self.running:
            import glm
            RenderCommand.set_clear_color(glm.vec4(0.1, 0.1, 0.1, 1))
            RenderCommand.clear()

            Renderer.begin_scene()

            self.blue_shader.bind()
            Renderer.submit(self.square_vertex_array)

            self.shader.bind()
            Renderer.submit(self.vertex_array)

            Renderer.end_scene()

            for layer in self.layer_stack:
                layer.on_update()

            self.imgui_layer.begin()
            for layer in self.layer_stack:
                layer.on_imgui_render()
            self.imgui_layer.end()

            self.window.on_update()

    def on_event(self, event: Event) -> None:
        dispatcher = EventDispatcher(event)
        dispatcher.dispatch(WindowCloseEvent, self.on_window_close)

        for layer in reversed(self.layer_stack):
            layer.on_event(event)
            if event.handled:
                break

    def push_layer(self, layer: Layer):
        self.layer_stack.push_layer(layer)

    def push_overlay(self, layer: Layer):
        self.layer_stack.push_overlay(layer)

    def on_window_close(self, event: WindowCloseEvent) -> bool:
        self.running = False
        return True
