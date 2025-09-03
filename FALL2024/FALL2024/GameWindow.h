#pragma once

/*
	Auther: Ju-ve Chankasemporn
	E-mail: juvereturn@gmail.com
	Brief: Managing window: creating, updating events, and cleaning up when shutting down
*/

#include <glew/glew.h>
#include <glfw/glfw3.h>

#include <iostream>
#include <functional>

class GameWindow
{
private:
	int width;
	int height;
	const char* window_name;
	GLFWwindow* window;
	std::function <void(GLFWwindow*, int, int)> resizeCallBack;

public:
	//Functions
	GameWindow(int width, int height, const char* name);
	~GameWindow();
	GLFWwindow* createWindow();
	GLFWwindow* getWindow();
	void pollEvents();
	bool shouldClose();
	bool setupGraphicsContext();
	void shutdownWindow();
	void setWindowHints(const std::function<void()>& hintSetter);
	void setResizeCallback(std::function<void(GLFWwindow*, int, int)> callback);
	int getWidth();
	int getHeight();

private: 
	static void resizeCallbackWrapper(GLFWwindow* window, int width, int height);
};

