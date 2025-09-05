#include "Material.h"
#include <cstring> 

Material::Material(Shader* shaderProgram) : shader(shaderProgram)
{

}

void Material::Draw()
{
    if (shader != NULL)
    {
        GLint isUsingTexture = glGetUniformLocation(shader->ID, "useTexture");
        glUniform1i(isUsingTexture, hasTexture);
    }

    if (texture != NULL)
    {
        texture->Bind();
    }
}

void Material::Delete()
{
    if (texture != NULL)
    {
        texture->Delete();
    }
}

void Material::SetShader(Shader* shaderProgram)
{
    shader = shaderProgram;
}

void Material::AddTexture()
{
    hasTexture = true;
    std::string fullPath = textureLocation + "pop_cat.png";

    texture = new Texture(fullPath.c_str(), GL_TEXTURE_2D, GL_TEXTURE0, GL_RGBA, GL_UNSIGNED_BYTE);
    texture->texUnit(*shader, "tex0", 0);
}

void Material::AddTexture(std::string textureName)
{
    hasTexture = true;
    std::string fullPath = textureLocation + textureName;

    // Directly use the std::string's c_str() method
    texture = new Texture(fullPath.c_str(), GL_TEXTURE_2D, GL_TEXTURE0, GL_RGBA, GL_UNSIGNED_BYTE);
    texture->texUnit(*shader, "tex0", 0);
}

void Material::AddTexture(std::string textureName, GLenum format)
{
    hasTexture = true;
    std::string fullPath = textureLocation + textureName;

    // Directly use the std::string's c_str() method
    texture = new Texture(fullPath.c_str(), GL_TEXTURE_2D, GL_TEXTURE0, format, GL_UNSIGNED_BYTE);
    texture->texUnit(*shader, "tex0", 0);
}