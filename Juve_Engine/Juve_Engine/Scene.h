#pragma once
#include <vector>
#include "Camera.h"
#include "Renderer.h"
#include "Node.h" // A class representing individual 3D objects

class Scene {
private:
    std::vector<Node*> objects;  // List of objects in the scene
    Camera* camera;                // Pointer to the camera
    Renderer& renderer;            // Pointer to the renderer
public:
    // Constructor
    Scene(Camera* cam, Renderer& rend);

    void assignObjects();

    // Add objects to the scene
    void addObject(Node* obj);

    // Render all objects in the scene
    void draw();

    // Update the scene (e.g., for animations or physics)
    void update(float deltaTime);

	void swapBuffers();

    // Destructor to clean up dynamically allocated objects
    ~Scene();
};
