#version 330

uniform mat4 projectionMatrix
uniform mat4 modelviewMatrix
uniform vec2 offset

layout(location=0) in vec2 vertex;

out vec4 vertex_color

void main()
{
  gl_Position = projectionMatrix * modelviewMatrix * (vertex+offset);
  vertex_color = gl_Color;
}