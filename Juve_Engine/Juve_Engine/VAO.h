#ifndef VAO_CLASS_H
#define VAO_CLASS_H

#include <glew/glew.h>
#include <glfw/glfw3.h>
#include"VBO.h"

class VAO
{
private:
	bool isInit;

public:
	// ID reference for the Vertex Array Object
	GLuint ID;
	// Constructor that generates a VAO ID
	VAO();

	// Links a VBO Attribute such as a position or color to the VAO
	void LinkAttrib(VBO& VBO, GLuint layout, GLuint numComponents, GLenum type, GLsizeiptr stride, void* offset);
	// Binds the VAO
	void Bind();
	// Unbinds the VAO
	void Unbind();
	// Deletes the VAO
	void Delete();
};

#endif
