#version 400

//Scaling matrix will adjust the size with respect to the radius, which is not processed here in shaders, and keep horizontal/vertical ratio constant.
uniform mat4 scaleMatrix;

//The center of the circle, pre-transformed in consideration of the scaling factor (so that, when multiplied by scaleMatrix, it yields the correcr coords.
uniform vec2 center;		

//Texture coordinates: x=[-1; 1], y=[-1; 1]; use these to set each texel's color individually, as needed to draw a circle.
layout(location=0) in vec2 vertex;


//Passthrough to fragment shader.
out vec2 fPos;

void main()
{
  //Fragment shader will receive the coordinate unchanged, as it only draws generic x^2+y^2=1 circles, which are then resized and translated.
  fPos = vertex;
  
  //Here, translate the coord to the position of the actual center, then scale it accordingly.
  gl_Position = scaleMatrix * vec4(vertex+center, 0.0, 1.0);
}