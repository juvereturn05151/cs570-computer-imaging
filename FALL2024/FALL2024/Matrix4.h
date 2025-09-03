#pragma once

#include <cmath>
#include <array>
#include <stdexcept>

#include "Vector3.h"

template <typename T>
class Matrix4 {
private:
    const int matrix_size = 4;
    T data[4][4];

public:
    Matrix4();

    // Multiplication: * Operator Overloads
    Matrix4<T> operator*(const Matrix4<T>& other);
    Vector3 operator*(const Vector3& vec) const;

    // Matrix-specific functions

    void updateElement(int row, int col, T value);
    T getElement(int row, int col) const;
    const T* getData() const;

    // Transformation utilities based on matrix
    // For practicity, I added these in the Matrix API,
    // however, these might be better candidates for a Transform class (think about it)
    // ... That's your homework!
    static Matrix4<T> translation(T tx, T ty, T tz);
    static Matrix4<T> scale(T sx, T sy, T sz);
    static Matrix4<T> rotationX(T angle);
    static Matrix4<T> rotationY(T angle);
    static Matrix4<T> rotationZ(T angle);
    static Matrix4<T> perspective(T fovY, T aspect, T nearPlane, T farPlane);
    static Matrix4<T> orthographic(T left, T right, T bottom, T top, T nearPlane, T farPlane);
    static Matrix4<T> lookAt(const Vector3& eye, const Vector3& center, const Vector3& up);
    static void printMatrix4(const Matrix4<T>& matrix);
    // I encourage to implement the Euler Angles formula: Removes the gimball lock problem
};

#include "Matrix4_impl.h"