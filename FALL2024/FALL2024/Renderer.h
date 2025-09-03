#pragma once

/*
	Auther: Ju-ve Chankasemporn
	E-mail: juvereturn@gmail.com
	Brief: Initialize graphic library, clear the screen, and swap the buffer
*/

#include <glew/glew.h>
#include <glfw/glfw3.h>

#include <iostream>

#include "GameWindow.h"
#include "Vector3.h"
#include "Shader.h"
#include "VAO.h"
#include "VBO.h"
#include "EBO.h"
#include "Camera.h"
#include "ObjectMesh.h"

class Renderer
{
private:
	GameWindow &game_window;
	Shader* shader;
	GLint modelMatrixLoc;
	GLint viewMatrixLoc;
	GLint projectionMatrixLoc;

public:
	Renderer(GameWindow &game_window);
	~Renderer();
	Shader* GetShader();
	GLint GetModelMatrixLoc();
	GLint GetViewMatrixLoc();
	GLint GetProjectionMatrixLoc();
	void clear(float r, float g, float b, float a);
	void swapBuffers();
	void setColor(Vector3 color, float alpha);

private:
	bool initializeLibraries();
	bool loadGraphicsAPIFunctions();
	void setupCallbacks();
	void frameBufferSizeCallback(GLFWwindow* window, int width, int height);
	void shutdownLibraries();
	void initShader();
};