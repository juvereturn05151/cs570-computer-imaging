#include "Transform.h"

Transform::Transform() : position(Vector3(0.0f, 0.0f, 0.0f)), rotation(Vector3(0.0f, 0.0f, 0.0f)), scale(Vector3(1.0f, 1.0f, 1.0f))
{

}

Transform::~Transform() {}

void Transform::setPosition(const Vector3& position)
{
    this->position = position;
}

Vector3 Transform::getPosition() const
{
    return position;
}

void Transform::setRotation(const Vector3& rotation)
{
    this->rotation = rotation;
}

Vector3 Transform::getRotation() const
{
    return rotation;
}

void Transform::setScale(const Vector3& scale)
{
    this->scale = scale;
}

Vector3 Transform::getScale() const
{
    return scale;
}

Matrix4<float> Transform::getModelMatrix() const
{
    return Matrix4<float>::translation(position.x, position.y, position.z) *
        Matrix4<float>::rotationX(rotation.x) *
        Matrix4<float>::rotationY(rotation.y) *
        Matrix4<float>::rotationZ(rotation.z) *
        Matrix4<float>::scale(scale.x, scale.y, scale.z);
}