import tkinter as tk
from tkinter import ttk
import gc
from gui import on_tree_select, load_image
from image_ops import create_negative_image
from commands import execute_command
from PIL import Image, ImageTk
import os

def main():
    imageData = {}

    root = tk.Tk()
    root.title("CS 570 Project#1")

    # Frames
    topFrame = tk.Frame(root)
    operationFrame = tk.Frame(topFrame)
    imageFrame = tk.Frame(topFrame)
    outputImageFrame = tk.Frame(topFrame)
    commandFrame = tk.Frame(root)

    topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    operationFrame.pack(side=tk.LEFT)
    outputImageFrame.pack(side=tk.RIGHT)
    imageFrame.pack(side=tk.RIGHT)
    commandFrame.pack(side=tk.BOTTOM, fill=tk.X)

    # Tree
    treeView = ttk.Treeview(operationFrame, selectmode='browse')
    rootIID = treeView.insert('', -1, text="Image List")
    treeView.pack(padx=10, pady=10)

    # Load default images
    filenameList = ['data/cameraman.ppm', 'data/butterfly-16.ppm', 'data/apple-20.ppm']
    for filename in filenameList:
        pil_Image = Image.open(filename)
        TkImage = ImageTk.PhotoImage(pil_Image)
        name = os.path.basename(filename)
        imageData[name] = TkImage
        treeView.insert(rootIID, -1, text=name)

    # Image labels
    imageLabel = tk.Label(imageFrame, image=imageData['apple-20.ppm'])
    imageLabel.pack(padx=10, pady=10)

    default_pil = Image.open('data/apple-20.ppm')
    default_negative_pil = create_negative_image(default_pil)
    default_negative_tk = ImageTk.PhotoImage(default_negative_pil)

    outputImageLabel = tk.Label(outputImageFrame, image=default_negative_tk)
    outputImageLabel.tk_image = default_negative_tk
    outputImageLabel.pil_image = default_negative_pil
    outputImageLabel.pack(padx=10, pady=10)

    # Bind events
    treeView.bind('<<TreeviewSelect>>',
                  lambda e: on_tree_select(e, treeView, imageLabel, outputImageLabel, imageData))

    # Command box
    commandLabel = tk.Label(commandFrame, text="Execute command:")
    commandLabel.pack(side=tk.LEFT, padx=5, pady=5)

    command_entry = ttk.Entry(commandFrame)
    command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
    command_entry.bind("<Return>",
                       lambda e: execute_command(e, command_entry, imageData, treeView, rootIID, outputImageLabel))

    root.mainloop()
    gc.collect()

if __name__ == "__main__":
    main()
