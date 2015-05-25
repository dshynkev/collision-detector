#version 330


uniform float radius

in vec2 center;
in vec4 vertex_color;

out vec4 fColor;

void main()
{
    float delta = fwidth(radius);
    float alpha = smoothstep(0.45-delta, 0.45, radius);
    fColor = mix(color, fColor, alpha);
}