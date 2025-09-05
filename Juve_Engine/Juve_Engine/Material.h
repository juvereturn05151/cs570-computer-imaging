#pragma once
#include "Texture.h"
#include "Shader.h"
#include "Matrix4.h"
class Material
{
private:
	Shader* shader;
	bool hasTexture;
	Texture* texture;
	Matrix4<float> modelMatrix;
	const std::string textureLocation = "textures/";
public:
	Material(Shader* shaderProgram);
	void Draw();
	void Delete();
	void AddTexture();
	void AddTexture(std::string textureName);
	void AddTexture(std::string textureName, GLenum format);
	void SetShader(Shader* shaderProgram);
};

