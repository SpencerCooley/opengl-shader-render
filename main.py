import time  # To track elapsed time
import glfw
from OpenGL.GL import *
import numpy as np
from shader import vertex_shader_source, fragment_shader_source

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compile error: {error}")
    return shader

def main():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    window = glfw.create_window(800, 300, "OpenGL 2.1 Shader", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)

    # Compile shaders
    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
        error = glGetProgramInfoLog(shader_program).decode()
        raise RuntimeError(f"Program link error: {error}")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    # Vertex data
    vertices = np.array([
        -1.0, -1.0, 0.0,
         1.0, -1.0, 0.0,
         1.0,  1.0, 0.0,
        -1.0,  1.0, 0.0
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        2, 3, 0
    ], dtype=np.uint32)

    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader_program, "position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, None)

    resolution_location = glGetUniformLocation(shader_program, "resolution")
    time_location = glGetUniformLocation(shader_program, "time")

    start_time = time.time()

    while not glfw.window_should_close(window):
        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader_program)

        # Pass resolution and time uniforms
        glUniform2f(resolution_location, 1500.0, 600.0)
        glUniform1f(time_location, elapsed_time)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO])
    glfw.terminate()

if __name__ == "__main__":
    main()
