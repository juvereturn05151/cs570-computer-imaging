#pragma once
#include "ObjectMesh.h"
#include "Mesh.h"
class RotatingObject : public ObjectMesh
{
private:
	float angle;

public:
	RotatingObject(Mesh* mesh, GLint modelMatrixLoc);
	void update(float deltaTime) override;
};

