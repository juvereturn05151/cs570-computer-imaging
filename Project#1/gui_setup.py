import tkinter as tk
from tkinter import ttk
from commands import execute_command

def setup_frames(root):
    """Create and organize all frames in the main window"""
    topFrame = tk.Frame(root)
    operationFrame = tk.Frame(topFrame)
    inputFrame = tk.Frame(topFrame)
    outputFrame = tk.Frame(topFrame)
    commandFrame = tk.Frame(root)

    topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    operationFrame.pack(side=tk.LEFT, fill=tk.Y)

    inputFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    inputFrame.pack_propagate(False)

    outputFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    outputFrame.pack_propagate(False)

    commandFrame.pack(side=tk.BOTTOM, fill=tk.X)

    return topFrame, operationFrame, inputFrame, outputFrame, commandFrame

def setup_treeview(operationFrame):
    """Create and configure the treeview widget for image selection"""
    treeView = ttk.Treeview(operationFrame, selectmode='browse')
    # Insert root item for image list with empty parent and auto index
    rootIID = treeView.insert('',-1, text="Image List")
    treeView.pack(padx=5, pady=5)
    return treeView, rootIID

def setup_image_labels(inputFrame, outputFrame, imageData, default_name='apple-20.ppm'):
    if default_name not in imageData:
        raise ValueError(f"Default image '{default_name}' not found in imageData")

    # setup input image
    pil_input = imageData[default_name]["input"]["pil"]
    tk_input = imageData[default_name]["input"]["tk"]

    inputLabel = tk.Label(inputFrame, image=tk_input)
    inputLabel.pack(padx=10, pady=10)

    inputLabel.original_pil = pil_input
    inputLabel.pil_image = pil_input
    inputLabel.tk_image = tk_input

    pil_output = imageData[default_name]["output"]["pil"]
    tk_output = imageData[default_name]["output"]["tk"]

    outputLabel = tk.Label(outputFrame, image=tk_output)
    outputLabel.pack(padx=10, pady=10)

    outputLabel.original_pil = pil_output
    outputLabel.pil_image = pil_output
    outputLabel.tk_image = tk_output

    return inputLabel, outputLabel

def setup_command_interface(commandFrame, imageData, treeView, rootIID, outputImageLabel):
    commandLabel = tk.Label(commandFrame, text="Execute command:")
    commandLabel.pack(side=tk.LEFT, padx=5, pady=5)

    command_entry = ttk.Entry(commandFrame)
    command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
    command_entry.bind("<Return>",
                       lambda e: execute_command(e, command_entry, imageData, treeView, rootIID, outputImageLabel))
    return command_entry
