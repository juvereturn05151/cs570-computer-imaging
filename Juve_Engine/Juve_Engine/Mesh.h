#pragma once
#include "Vector3.h"
#include <vector>
#include <glew/glew.h>
#include "VAO.h"
#include "EBO.h"
#include "Texture.h"
#include "Shader.h"

class Mesh 
{
protected:
    VAO* VAO1;
    VBO* VBO1;
    EBO* EBO1;
    Texture* texture;
    std::vector<GLfloat> vertices;
    std::vector<GLuint> indices;
    Vector3 color;
    float alpha;
    bool hasTexture;
    Shader* shader;

public:
    Mesh(Vector3 color, float alpha, Shader* shaderProgram);
    void setupBuffers(); // Setup VBO, VAO, etc.
    void cleanup(); // Cleanup resources
    virtual void draw();
    void AddTexture();
    void SetShader(Shader* shaderProgram);
};