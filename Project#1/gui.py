import os
from PIL import Image, ImageTk


def select_image(imageName, imageLabel, outputImageLabel, imageData, output_image_frame):
    # Update input image
    pil_input = imageData[imageName]["pil"]
    tk_input = imageData[imageName]["tk"]
    imageLabel.config(image=tk_input)
    imageLabel.tk_image = tk_input
    imageLabel.original_pil = pil_input
    imageLabel.pil_image = pil_input

    # Update output image
    pil_output = output_image_frame[imageName]["pil"]
    tk_output = output_image_frame[imageName]["tk"]
    outputImageLabel.config(image=tk_output)
    outputImageLabel.tk_image = tk_output
    outputImageLabel.original_pil = pil_output
    outputImageLabel.pil_image = pil_output



def on_tree_select(event, treeView, imageLabel, outputImageLabel, imageData, output_image_frame):
    selectedItem = treeView.focus()
    itemDetails = treeView.item(selectedItem)
    itemText = itemDetails['text']
    if itemText in imageData.keys():
        select_image(itemText, imageLabel, outputImageLabel, imageData, output_image_frame)


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