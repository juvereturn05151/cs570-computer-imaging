"""
File Name:    unsharp_masking.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

from image_data import get_ppm_maxvalue

def select_image(imageName, imageLabel, outputImageLabel, imageData, output_image_frame):
    # Update input image
    pil_input = imageData[imageName]["pil"]
    tk_input = imageData[imageName]["tk"]
    imageLabel.config(image=tk_input)
    imageLabel.tk_image = tk_input
    imageLabel.original_pil = pil_input
    imageLabel.pil_image = pil_input

def select_image2(imageName, imageLabel, imageData):
    pil_input = imageData[imageName]["pil"]
    tk_input = imageData[imageName]["tk"]
    imageLabel.config(image=tk_input)
    imageLabel.tk_image = tk_input
    imageLabel.original_pil = pil_input
    imageLabel.pil_image = pil_input

def on_tree_select(event, treeView, imageLabel, outputImageLabel, input_image_data, output_image_data):
    selectedItem = treeView.focus()
    itemDetails = treeView.item(selectedItem)
    itemText = itemDetails['text']
    if itemText in input_image_data.keys():
        select_image(itemText, imageLabel, outputImageLabel, input_image_data, output_image_data)

def on_tree_select2(event, treeView, imageLabel, input_image_data):
    selectedItem = treeView.focus()
    itemDetails = treeView.item(selectedItem)
    itemText = itemDetails['text']
    if itemText in input_image_data.keys():
        select_image2(itemText, imageLabel, input_image_data)


def load_image(loadFilename, imageData, treeView=None, rootIID=None):
    import os
    from PIL import Image, ImageTk

    pil_image = Image.open( loadFilename)
    tk_image = ImageTk.PhotoImage(pil_image)
    name = os.path.basename(loadFilename)

    # Get maxval for PPM (you already have a helper function get_ppm_maxvalue)
    try:
        maxval = get_ppm_maxvalue('data/' + loadFilename)
    except Exception:
        maxval = None  # fallback if not a PPM or error occurs

    # Store in same structure as load_default_images
    imageData[name] = {
        "pil": pil_image,
        "tk": tk_image,
        "maxval": maxval,
    }

    # Insert into TreeView if provided
    if treeView is not None and rootIID is not None:
        treeView.insert(rootIID, -1, text=name)



def save_output_image(fileName, outputImageLabel):
    # Check if we have a PIL image stored
    if hasattr(outputImageLabel, 'pil_image') is not None:
        print("No OutputImage")


    if hasattr(outputImageLabel, 'pil_image') and outputImageLabel.pil_image:
        if not fileName.endswith('.ppm'):
            fileName += '.ppm'
            print(f"Added .ppm extension. Saving as: {fileName}")

        outputImageLabel.pil_image.save(fileName)
        print(f"Image saved to save_images/{fileName}")
    else:
        print("No output image to save")