#version 400

#define SMOOTH_FACTOR 2

//The coordinate of current texel.
in vec2 fPos;

/* As the draw call attributes carry no actual payload (it merely invokes the processing sequence,
 * and, being  a texture draw, allows us to process individual texels), we have to pass the colors as uniforms.
**/
uniform vec4 circleColor;
uniform vec4 borderColor;

//Whether a border should be painted
uniform float paintBorder;

//Width of the border in pixels.
uniform float borderWidth;

//The color to display
out vec4 fColor;

void main()
{
	//Determine the distance from center. Since fPos.xy = [-1; 1], dist = [0; sqrt(2)], reflecting x^2+y^2, which is <=1 for all points inside the circle.
	float dist = distance(fPos, vec2(0, 0));

	//Delta is the width of the smooth border area. fwidth() returns the total derivative, i.e. how fast dist changes within current fragment.
	//Therefore, fwidth(dist) is the width of one pixel in OpenGL coordinates.
	float delta = fwidth(dist)*borderWidth;
	
	if(paintBorder<1)
	{
		//If dist is within 1-delta...1, dist will hold a value [0...1], describing a stage of smooth transition.
		float alpha = smoothstep(1-2*delta, 1, dist);

		//Mix target color with transparent in proportion alpha.
		fColor = mix(circleColor, vec4(0.0, 0.0, 0.0, 0.0), alpha);
	}
	else
	{
		//alpha_main is the same as alpha in previous clause.
		float alpha_main = smoothstep(1-delta, 1, dist);
		
		//alpha_border signifies 
		float alpha_border = smoothstep(1-2*delta, 1-delta, dist);
		vec4 color = mix(circleColor, borderColor, alpha_border);
		fColor = mix(color, vec4(0.0, 0.0, 0.0, 0.0), alpha_main);
	}
}