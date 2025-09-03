#include "Renderer.h"
#include "Matrix4.h"
#include "GameWindow.h"
#include "Transform.h"
#include "Node.h"
#include "Mesh.h"

#include<vector>

Renderer::Renderer(GameWindow &game_window) : game_window(game_window)
{
    if (!initializeLibraries()) 
    {
        return;
    }

    GLFWwindow* window = game_window.createWindow();
    if (!window) 
    {
        shutdownLibraries();
        return;
    }

    if (!game_window.setupGraphicsContext())
    {
        game_window.shutdownWindow();
        shutdownLibraries();
        return;
    }

    if (!loadGraphicsAPIFunctions()) 
    {
        game_window.shutdownWindow();
        shutdownLibraries();
        return;
    }

    this->game_window = game_window;

    setupCallbacks();

    initShader();

    glEnable(GL_DEPTH_TEST);

    modelMatrixLoc = glGetUniformLocation(shader->ID, "ModelMatrix");
    viewMatrixLoc = glGetUniformLocation(shader->ID, "ViewMatrix");
    projectionMatrixLoc = glGetUniformLocation(shader->ID, "ProjectionMatrix");

    shader->Activate();
}

Shader* Renderer::GetShader()
{
    return shader;
}

GLint Renderer::GetModelMatrixLoc()
{
    return modelMatrixLoc;
}

GLint Renderer::GetViewMatrixLoc()
{
    return viewMatrixLoc;
}

GLint Renderer::GetProjectionMatrixLoc()
{
    return projectionMatrixLoc;
}

void Renderer::clear(float r, float g, float b, float a)
{
    glClearColor(r, g, b, a);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
}

void Renderer::swapBuffers()
{
    if (game_window.getWindow() != nullptr)
    {
        glfwSwapBuffers(game_window.getWindow());
    }
}

bool Renderer::initializeLibraries() 
{
    if (!glfwInit()) 
    {
        std::cerr << "Failed to initialize GLFW" << std::endl;
        return false;
    }
    return true;
}

bool Renderer::loadGraphicsAPIFunctions() 
{
    if (glewInit() != GLEW_OK)
    {
        std::cerr << "Failed to initialize GLEW" << std::endl;
        return false;
    }
    return true;
}

void Renderer::setupCallbacks() 
{
    game_window.setResizeCallback([this](GLFWwindow* window, int width, int height)
    {
        this->frameBufferSizeCallback(window, width, height);
    });
}

void Renderer::frameBufferSizeCallback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

void Renderer::shutdownLibraries()
{
    glfwTerminate();
}

void Renderer::initShader()
{
    shader = new Shader("default.vert", "default.frag");
}

Renderer::~Renderer()
{
    delete shader;
}