#version 400

#define SMOOTH_FACTOR 2

//The coordinate of current texel.
in vec2 fPos;

/* As the draw call attributes carry no actual payload (it merely invokes the processing sequence,
 * and, being  a texture draw, allows us to process individual texels), we have to pass the colors as uniforms.
**/
uniform vec4 circleColor;
uniform vec4 borderColor;

// Whether a border should be painted
uniform float paintBorder;

// Width of the border in pixels.
uniform float borderWidth;
// Width of transition in pixels
uniform float smoothWidth;

// The color to display
out vec4 fColor;

void main()
{
	// Determine the distance from center. Since fPos.xy = [-1; 1], dist = [0; sqrt(2)], reflecting x^2+y^2, which is <=1 for all points inside the circle.
	float dist = distance(fPos, vec2(0, 0));

	// fwidth() returns the total derivative, i.e. how fast dist changes within current fragment.
	// Therefore, fwidth(dist) is the width of one pixel in OpenGL coordinates.
	// border and outer are respective widths in OpenGL coords.
	float border = fwidth(dist)*borderWidth;
	float outer = fwidth(dist)*smoothWidth;

	if(paintBorder<1)
	{
		// If dist is within 1-2delta...1, dist will hold a value [0...1], describing a stage of smooth transition.
		float alpha = smoothstep(1-border-outer, 1-border, dist);

		// Mix target color with transparent in proportion alpha.
		fColor = mix(circleColor, vec4(0.0, 0.0, 0.0, 0.0), alpha);
	}
	else
	{
		// alpha_main is now the outer rim, border->void transition
		float alpha_main = smoothstep(1-outer, 1, dist);
		
		// alpha_border indicates the stage of circle->border transition
		float alpha_border = smoothstep(1-border-outer, 1-outer, dist);

		// Mix circle with border
		vec4 color = mix(circleColor, borderColor, alpha_border);
		
		// Mix border with void
		fColor = mix(color, vec4(0.0, 0.0, 0.0, 0.0), alpha_main);
	}
}
