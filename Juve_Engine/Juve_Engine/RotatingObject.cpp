#include "RotatingObject.h"

RotatingObject::RotatingObject(Mesh* mesh, GLint modelMatrixLoc) : ObjectMesh(mesh, modelMatrixLoc)
{
	angle = 0;
}

void RotatingObject::update(float deltaTime) 
{
	angle += 0.05f * 0.05f;
	transform->setRotation(Vector3(0.0f, angle, 0.0f));
	Node::update(deltaTime);
}