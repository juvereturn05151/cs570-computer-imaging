#include "Camera.h"
#include <cmath>

Camera::Camera(GLint viewMatrixLoc, GLint projectionMatrixLoc, GameWindow& game_window) : position(0.0f, 0.0f, -5.0f), target(0.0f, 0.0f, 0.0f), up(0.0f, 1.0f, 0.0f),
viewMatrixLoc(viewMatrixLoc), projectionMatrixLoc(projectionMatrixLoc), game_window(game_window)
{

}

Camera::~Camera() {}

void Camera::update(float deltaTime)
{

}

void Camera::setPosition(const Vector3& position) 
{
    this->position = position;
}

void Camera::setTarget(const Vector3& target) 
{
    this->target = target;
}

void Camera::setUpVector(const Vector3& up) 
{
    this->up = up;
}

void Camera::setPerspective(float fov, float near, float far)
{
    this->fov = fov;
    this->near = near;
    this->far = far;
}

void Camera::updateAspectRatio(int windowHeight, int windowWidth)
{
    Matrix4<float> viewMatrix = getViewMatrix();

    aspectRatio = (windowHeight != 0) ?
        static_cast<float>(windowWidth) / static_cast<float>(windowHeight) : 1.0f;

    Matrix4<float> projectionMatrix = getProjectionMatrix(45.0f * 3.14159f / 180.0f, aspectRatio, 1.0f, 100.0f);

    glUniformMatrix4fv(viewMatrixLoc, 1, GL_FALSE, viewMatrix.getData());

    glUniformMatrix4fv(projectionMatrixLoc, 1, GL_FALSE, projectionMatrix.getData());
}

void Camera::updateCamera()
{
    Matrix4<float> viewMatrix = getViewMatrix();

    aspectRatio = (game_window.getHeight() != 0) ?
        static_cast<float>(game_window.getWidth()) / static_cast<float>(game_window.getHeight()) : 1.0f;

    Matrix4<float> projectionMatrix = getProjectionMatrix(45.0f * 3.14159f / 180.0f, aspectRatio, 1.0f, 100.0f);

    glUniformMatrix4fv(viewMatrixLoc, 1, GL_FALSE, viewMatrix.getData());

    glUniformMatrix4fv(projectionMatrixLoc, 1, GL_FALSE, projectionMatrix.getData());
}

const Matrix4<float>& Camera::getViewMatrix() const {
    return Matrix4<float>::lookAt(position, target, up);
}

const Matrix4<float>& Camera::getProjectionMatrix(float fov, float aspectRatio, float near, float far) const {
    return Matrix4<float>::perspective(fov, aspectRatio, near, far);
}