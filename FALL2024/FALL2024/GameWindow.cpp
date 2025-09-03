#include "GameWindow.h"

GameWindow::GameWindow(int width, int height, const char* name)
{
	this->width = width;
	this->height = height;
	window_name = name;
}

GameWindow::~GameWindow()
{
	shutdownWindow();
}

GLFWwindow* GameWindow::createWindow() {
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	window = glfwCreateWindow(width, height, window_name, NULL, NULL);

	if (window == nullptr)
	{
		std::cerr << "Failed to create GLFW window" << std::endl;
		return nullptr;
	}

	return window;
}

GLFWwindow* GameWindow::getWindow()
{
	return this->window;
}

void GameWindow::pollEvents() 
{
	glfwPollEvents();
}

bool GameWindow::shouldClose()
{
	if (window == nullptr) 
	{
		return false;
	}

	return glfwWindowShouldClose(window);
}

bool GameWindow::setupGraphicsContext() 
{
	glfwMakeContextCurrent(window);
	return true;
}

void GameWindow::shutdownWindow() 
{
	glfwDestroyWindow(window);
	glfwTerminate();
}

void GameWindow::setWindowHints(const std::function<void()>& hintSetter)
{
	hintSetter();
}

void GameWindow::setResizeCallback(std::function<void(GLFWwindow*, int, int)> callback) 
{
	resizeCallBack = std::move(callback);
	glfwSetFramebufferSizeCallback(window, resizeCallbackWrapper);
	glfwSetWindowUserPointer(window, this);
}

void GameWindow::resizeCallbackWrapper(GLFWwindow* window, int width, int height)
{
	auto* gameWindow = static_cast<GameWindow*>(glfwGetWindowUserPointer(window));
	if (gameWindow && gameWindow->resizeCallBack)
	{
		gameWindow->resizeCallBack(window, width, height);
		std::cout << "Window size: (" << width << ", " << height << ")" << std::endl;
	}
}

int GameWindow::getWidth()
{
	return width;
}

int GameWindow::getHeight()
{
	return height;
}