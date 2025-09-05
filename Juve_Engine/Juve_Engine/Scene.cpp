#include "Scene.h"
#include "ObjectMesh.h"
#include "Triangle.h"
#include "Square.h"
#include "RotatingObject.h"

// Constructor initializes camera and renderer
Scene::Scene(Camera* cam, Renderer& rend) : camera(cam), renderer(rend) {}

void Scene::assignObjects()
{
    //Create Rotating Triangle Which is the root
    Triangle* triangleMesh = new Triangle(Vector3(0.0f, 0.0f, 1.0f), 0.5f, renderer.GetShader());
    RotatingObject* rotatingObject = new RotatingObject(triangleMesh, renderer.GetModelMatrixLoc());
    rotatingObject->getTransform()->setPosition(Vector3(0.0f, 0.0f, 0.0f));
    rotatingObject->getTransform()->setScale(Vector3(1.0f, 1.0f, 1.0f));

    //A still object, but since it will inherit rotation from triangle mesh, it should rotate accordingly
    Square* mesh = new Square(Vector3(0.0f, 1.0f, 0.0f), 0.1f, renderer.GetShader());
    mesh->AddTexture();
    ObjectMesh * stationaryObject = new ObjectMesh(mesh, renderer.GetModelMatrixLoc());
    stationaryObject->getTransform()->setPosition(Vector3(2.0f, 0.0f, 0.0f));
    stationaryObject->getTransform()->setScale(Vector3(1.0f, 1.0f, 1.0f));

    rotatingObject->addChild(stationaryObject);

    addObject(rotatingObject);
}

// Add objects to the scene
void Scene::addObject(Node* obj) 
{
    objects.push_back(obj);
}

// Update objects in the scene (animations, physics, etc.)
void Scene::update(float deltaTime) {
    //angle += 0.05f * 0.05f;
    for (Node* obj : objects) 
    {
        //obj->getTransform()->setRotation(Vector3(0.0f, angle, 0.0f));
        obj->update(deltaTime);  // Assuming objects have an update method
    }
}

// Render the scene
void Scene::draw() {
    // First, clear the screen
    renderer.clear(0.2f, 0.3f, 0.3f, 1.0f);

    // Get the camera's view and projection matrices
    camera->updateCamera();

    // Render all objects
    for (Node* obj : objects) 
    {
        obj->draw();
    }
}

void Scene::swapBuffers() {
    renderer.swapBuffers();
}

// Destructor to clean up dynamically allocated memory
Scene::~Scene() {
    for (Node* obj : objects) 
    {
        delete obj;
    }
}