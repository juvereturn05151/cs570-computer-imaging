import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from image_ops import create_negative_image


def select_image(imageName, imageLabel, outputImageLabel, imageData):
    # Update the input image
    imageLabel.config(image=imageData[imageName])

    # Load the original PIL image and create negative
    pil_Image = Image.open('data/' + imageName)
    negative_pil = create_negative_image(pil_Image)  # This should return a PIL Image

    # Convert PIL Image to PhotoImage for display
    negativeTk = ImageTk.PhotoImage(negative_pil)

    # Update the output image label
    outputImageLabel.config(image=negativeTk)
    outputImageLabel.tk_image = negativeTk  # Store reference to prevent garbage collection
    outputImageLabel.pil_image = negative_pil  # Store PIL image for saving

    outputImageLabel.pack(padx=10, pady=10)


def on_tree_select(event, treeView, imageLabel, outputImageLabel, imageData):
    selectedItem = treeView.focus()
    itemDetails = treeView.item(selectedItem)
    itemText = itemDetails['text']
    if itemText in imageData.keys():
        select_image(itemText, imageLabel, outputImageLabel, imageData)


def load_image(loadFilename, imageData, treeView=None, rootIID=None):
    pil_Image = Image.open('data/' + loadFilename)
    tk_Image = ImageTk.PhotoImage(pil_Image)
    name = os.path.basename(loadFilename)
    imageData[name] = tk_Image
    if treeView and rootIID:
        treeView.insert(rootIID, -1, text=name)


def save_output_image(fileName, outputImageLabel):
    # Check if we have a PIL image stored
    if hasattr(outputImageLabel, 'pil_image') is not None:
        print("No OutputImage")


    if hasattr(outputImageLabel, 'pil_image') and outputImageLabel.pil_image:
        if not fileName.endswith('.ppm'):
            fileName += '.ppm'
            print(f"Added .ppm extension. Saving as: {fileName}")

        outputImageLabel.pil_image.save('data/' + fileName)
        print(f"Image saved to save_images/{fileName}")
    else:
        print("No output image to save")