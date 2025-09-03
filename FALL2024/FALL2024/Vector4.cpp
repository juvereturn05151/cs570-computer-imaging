#include "Vector3.h"

#include <iostream>
#include <iomanip>

Vector3 Vector3::operator+(const Vector3& other) const
{
    // Write implementation here
    Vector3 resultVector = Vector3(x + other.x, y + other.y, z + other.z);
    return resultVector;
}

Vector3 Vector3::operator-(const Vector3& other) const
{
    // Write implementation here
    Vector3 resultVector = Vector3(x - other.x, y - other.y, z - other.z);
    return resultVector;
}

Vector3 Vector3::operator*(float scalar) const
{
    // Write implementation here
    Vector3 resultVector = Vector3(x * scalar, y * scalar, z * scalar);
    return resultVector;
}

float Vector3::dot(const Vector3& other) const
{
    // Write implementation here
    float dotResult = x * other.x + y * other.y + z * other.z;
    return dotResult;
}

float Vector3::magnitude() const
{
    // Write implementation here
    float vectorMagnitude = sqrt(pow(x,2) + pow(y, 2) + pow(z, 2));
    return vectorMagnitude;
}

float Vector3::magnitudSquared() const
{
    // Write implementation here
    float vectorSquaredMagnitude = pow(x, 2) + pow(y, 2) + pow(z, 2);
    return vectorSquaredMagnitude;
}

Vector3 Vector3::normalized() const
{
    // Write implementation here
    float vectorMagnitude = magnitude();

    // Handle case where magnitude is zero (return a zero vector or handle error)
    if (vectorMagnitude == 0) {
        return Vector3(0, 0, 0);
    }

    Vector3 normalizedVector = Vector3(x / vectorMagnitude, y / vectorMagnitude, z / vectorMagnitude);
    return normalizedVector;
}

Vector3 Vector3::cross(const Vector3& other) const
{
    // Write implementation here
    float resultVectorX = y * other.z - z * other.y;
    float resultVectorY = z * other.x - x * other.z;
    float resultVectorZ = x * other.y - y * other.x;
    Vector3 resultVector = Vector3(resultVectorX, resultVectorY, resultVectorZ);
    return resultVector;
}

std::ostream& operator<<(std::ostream& os, const Vector3& v) {
    os << std::fixed << std::setprecision(2) << "(" << v.x << ", " << v.y << ", " << v.z << ")";
    return os;
}