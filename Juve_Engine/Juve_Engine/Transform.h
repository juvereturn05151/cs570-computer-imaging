#pragma once
#include"Vector3.h"
#include "Matrix4.h"

class Transform
{
private:
	Vector3 position;
	Vector3 rotation;
	Vector3 scale;
public:
	Transform();
	~Transform();

	void setPosition(const Vector3& position);
	Vector3 getPosition() const;

	void setRotation(const Vector3& rotation);
	Vector3 getRotation() const;

	void setScale(const Vector3& scale);
	Vector3 getScale() const;

	Matrix4<float> getModelMatrix() const;
};

