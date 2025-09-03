#include "Node.h"

Node::Node()
{
    transform = new Transform();
}

Node::~Node()
{

}

void Node::update(float deltaTime)
{
    for (Node* child : children)
    {
        child->update(deltaTime);
    }
}

void Node::draw()
{
    for (Node* child : children)
    {
        child->draw();
    }
}

Transform* Node::getTransform()
{
    return transform;
}

Matrix4<float> Node::getGlobalModelMatrix() const {
    // Get the local model matrix from the transform
    Matrix4<float> localModelMatrix = transform->getModelMatrix();

    // If this object has a parent, multiply the parent's global matrix with the local matrix
    if (parent) 
    {
        return localModelMatrix * parent->getGlobalModelMatrix(); // Parent's transform * Local transform
    }

    // If no parent, return the local matrix
    return localModelMatrix;
}

void Node::setParent(Node* parent)
{
    this->parent = parent;
}

void Node::addChild(Node* child)
{
    child->setParent(this);
    children.push_back(child);
}