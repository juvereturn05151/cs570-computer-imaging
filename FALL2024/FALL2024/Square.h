#pragma once
#include "Mesh.h"
class Square : public Mesh
{
	private:
		std::vector<GLfloat> squareVertices =
		{
			-0.5f, -0.5f, 0.0f,
			-0.5f, 0.5f, 0.0f,
			0.5f, 0.5f, 0.0f,
			0.5f, -0.5f, 0.0f
		};

	public:
		Square(Vector3 color, float alpha, Shader* shaderProgram);
		Square(Vector3 point1, Vector3 point2, Vector3 point3, Vector3 point4, Vector3 color, float alpha, Shader* shaderProgram);
};

