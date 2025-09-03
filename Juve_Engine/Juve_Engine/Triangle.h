#pragma once
#include "Mesh.h"
#include "Vector3.h"
class Triangle : public Mesh
{
private:
	std::vector<GLfloat> triangleVertices =
	{
		-0.5f, -0.5f, 0.0f,
		0.5f, -0.5f, 0.0f,
		0.0f, 0.5f, 0.0f,
	};

public:
	Triangle(Vector3 point1, Vector3 point2, Vector3 point3, Vector3 color, float alpha, Shader* shaderProgram);
	Triangle(Vector3 color, float alpha, Shader* shaderProgram);
};

