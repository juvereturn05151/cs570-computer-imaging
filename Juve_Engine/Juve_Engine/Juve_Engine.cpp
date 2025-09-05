#include "CustomImgui.h"

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

		CustomImgui* customImgui = new CustomImgui();
		customImgui->init(window.getWindow());

        while (!window.shouldClose()) {
            window.pollEvents();

            scene->update(1.0f);

            customImgui->newFrame();

            scene->draw();

			customImgui->render();

			scene->swapBuffers();
        }

		delete customImgui;
        delete camera;
        delete scene;
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return -1;
    }

    return 0;

}
