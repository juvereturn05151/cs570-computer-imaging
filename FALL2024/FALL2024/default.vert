#version 330 core
// Positions/Coordinates
layout (location = 0) in vec3 position;
// Colors  // Expecting RGBA here
layout (location = 1) in vec4 vertexColor;

layout (location = 2) in vec2 aTex;

uniform mat4 ModelMatrix;
uniform mat4 ViewMatrix;
uniform mat4 ProjectionMatrix;

//Outputs the color for the Fragment Shader
out vec4 color;
out vec2 texCoord;

void main()
{
	gl_Position = ProjectionMatrix *  ViewMatrix *  ModelMatrix *  vec4(position.x, position.y, position.z, 1.0);
	color = vertexColor;
	texCoord = aTex;
}