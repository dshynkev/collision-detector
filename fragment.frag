#version 400

//The coordinate of current texel.
in vec2 fPos;

/** As the draw call attributes carry no actual payload (it merely invokes the processing sequence,
 * and, being  a texture draw, allows us to process individual texels), we have to pass the color as uniform.
**/
uniform vec4 circleColor;

//The color to display
out vec4 fColor;

void main()
{
  //Determine the distance from center. Since fPos.xy = [-1; 1], dist = [0; sqrt(2)], reflecting x^2+y^2, which is <=1 for all points inside the circle.
  float dist = distance(fPos, vec2(0, 0));
  
  //Delta is the width of the smooth border area. fwidth() returns the total derivative, i.e. how fast dist changes within current fragment.
  //1.5 is a magic coefficient, chosen arbitrarily.
  float delta = fwidth(dist)*1.5;
  
  //If dist is within 1-delta...1, dist will hold a value [0...1], describing a stage of smooth transition.
  float alpha = smoothstep(1-delta, 1, dist);
  
  //Mix target color with transparent in proportion alpha.
  fColor = mix(circleColor, vec4(0.0, 0.0, 0.0, 0.0), alpha);
}