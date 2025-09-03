#include "Square.h"

Square::Square(Vector3 color, float alpha, Shader* shaderProgram) : Mesh(color, alpha, shaderProgram)
{
    vertices =
    {
        squareVertices[0], squareVertices[1], squareVertices[2], color.x, color.y, color.z, alpha, 0.0f, 0.0f,
        squareVertices[3], squareVertices[4], squareVertices[5], color.x, color.y, color.z, alpha, 0.0f, 1.0f,
        squareVertices[6], squareVertices[7], squareVertices[8], color.x, color.y, color.z, alpha, 1.0f, 1.0f,
        squareVertices[9], squareVertices[10], squareVertices[11], color.x, color.y, color.z, alpha, 1.0f, 0.0f
    };

    indices =
    {
        0, 1, 2,  // Define the triangle using vertex indices
        0, 3, 2
    };

    setupBuffers();
}

Square::Square(Vector3 point1, Vector3 point2, Vector3 point3, Vector3 point4, Vector3 color, float alpha, Shader* shaderProgram) : Mesh(color, alpha, shaderProgram)
{
    vertices =
    {
        point1.x, point1.y, point1.z, color.x, color.y, color.z, alpha, 0.0f, 0.0f,
        point2.x, point2.y, point2.z, color.x, color.y, color.z, alpha, 0.0f, 1.0f,
        point3.x, point3.y, point3.z, color.x, color.y, color.z, alpha, 1.0f, 1.0f,
        point4.x, point4.y, point4.z, color.x, color.y, color.z, alpha, 1.0f, 0.0f
    };

    indices =
    {
        0, 1, 2,  // Define the triangle using vertex indices
        0, 3, 2
    };

    setupBuffers();
}