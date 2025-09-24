# Implement your code here and upload the Jupyter notebook to Moodle assignment
import os, gc
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps

####################################################
def select_image(imageName):
    imageLabel.config(image=imageData[imageName])
    imageLabel.pack(padx=10, pady=10)

    pil_Image = Image.open('data/' + imageName)
    negativeTk = create_negative_image(pil_Image)
    outputImageLabel.config(image=negativeTk)
    outputImageLabel.image = negativeTk
    outputImageLabel.pack(padx=10, pady=10)

####################################################
def on_tree_select(event):
    selectedItem = treeView.focus()
    itemDetails = treeView.item(selectedItem)
    print(itemDetails)
    itemText = itemDetails['text']
    if itemText in imageData.keys():
        select_image(itemText)

####################################################
def create_negative_image(pil_image):
    pil_RGB = pil_image.convert('RGB')
    negative_pil = ImageOps.invert(pil_RGB)
    negative_tk = ImageTk.PhotoImage(negative_pil)

    return negative_tk

####################################################
def execute_command(event=None):
    cmd = command_entry.get().strip()
    command_entry.delete(0, tk.END)

    if cmd.startswith("load "):
        filename = cmd.split(" ", 1)[1]
        load_image(filename);
        print(f"Loaded {filename}")
    else:
        print(f"Unknown command: {cmd}")

####################################################
def load_image(loadFilename):
    print(f"Loading image {loadFilename}")
    pil_Image = Image.open('data/' + loadFilename)

    tk_Image = ImageTk.PhotoImage(pil_Image)
    name = os.path.basename(loadFilename)
    imageData[name] = tk_Image

    treeView.insert(rootIID, -1, text=name)
####################################################

imageData = {}

root = tk.Tk()

root.title("CS 370 Census Application, part deux")
#top
topFrame = tk.Frame(root)
operationFrame = tk.Frame(topFrame)
imageFrame = tk.Frame(topFrame)
outputImageFrame = tk.Frame(topFrame)
#bottom
commandFrame = tk.Frame(root)

#top
topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
operationFrame.pack(side=tk.LEFT)
outputImageFrame.pack(side=tk.RIGHT)
imageFrame.pack(side=tk.RIGHT)
#bottom
commandFrame.pack(side=tk.BOTTOM, fill=tk.X)

# Add a command line box to the bottom frame
treeView = ttk.Treeview(operationFrame, selectmode='browse')
rootIID = treeView.insert('', -1, text="Image List")
treeView.pack(padx=10, pady=10)

# Instead of loading one image file, we are loading multiple files here
filenameList = [
    'data/cameraman.ppm',
    'data/butterfly-16.ppm',
    'data/apple-20.ppm'
]

# Load all the images
for filename in filenameList:
    # Open the image using PIL
    print(f"Loading image {filename}")
    PILImage = Image.open(filename)

    # Convert the PIL image to a Tkinter PhotoImage
    TkImage = ImageTk.PhotoImage(PILImage)
    name = os.path.basename(filename)
    imageData[name] = TkImage

    treeView.insert(rootIID, -1, text=name)

# Create a Label widget to display the image
imageLabel = tk.Label(imageFrame, image=imageData['apple-20.ppm'])
imageLabel.pack(padx=10, pady=10)

# Output Image, make it negative at the start
default_pil = Image.open('data/apple-20.ppm')
default_negative = create_negative_image(default_pil)

outputImageLabel = tk.Label(outputImageFrame, image=default_negative)
outputImageLabel.image = default_negative  # keep reference!
outputImageLabel.pack(padx=10, pady=10)

treeView.bind('<<TreeviewSelect>>', on_tree_select)

# For Command
commandLabel = tk.Label(commandFrame, text="Execute command:")
commandLabel.pack(side=tk.LEFT, padx=5, pady=5)

command_entry = ttk.Entry(commandFrame)
command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
command_entry.bind("<Return>", execute_command)

root.mainloop()
gc.collect()