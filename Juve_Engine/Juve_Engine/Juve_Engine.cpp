#include"imgui.h"
#include"imgui_impl_glfw.h"
#include"imgui_impl_opengl3.h"

#include <iostream>
#include "GameWindow.h"
#include "Renderer.h"
#include "Camera.h"
#include "Scene.h"

int main() 
{
    try {
        GameWindow window(800, 600, "OpenGL Window");
        Renderer renderer(window);
        Camera * camera = new Camera(renderer.GetViewMatrixLoc(), renderer.GetProjectionMatrixLoc(), window);
        Scene * scene = new Scene(camera,renderer);

        scene->assignObjects();

		IMGUI_CHECKVERSION();
		ImGui::CreateContext();
		ImGuiIO& io = ImGui::GetIO(); (void)io;
		ImGui::StyleColorsDark();
		ImGui_ImplOpenGL3_Init("#version 330");

        while (!window.shouldClose()) {
            window.pollEvents();

            scene->update(1.0f);
            scene->draw();
        }

        delete camera;
        delete scene;
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return -1;
    }

    return 0;

}
