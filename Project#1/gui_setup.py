import tkinter as tk
from tkinter import ttk
from commands import execute_command

def setup_frames(root):
    """Create and organize all frames in the main window"""
    topFrame = tk.Frame(root)
    operation_frame = tk.Frame(topFrame)
    input_image_frame = tk.Frame(topFrame)
    input_image_frame2 = tk.Frame(topFrame)
    output_image_frame = tk.Frame(topFrame)
    command_frame = tk.Frame(root)

    topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    operation_frame.pack(side=tk.LEFT, fill=tk.Y)

    input_image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_image_frame.pack_propagate(False)

    input_image_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_image_frame2.pack_propagate(False)

    output_image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    output_image_frame.pack_propagate(False)

    command_frame.pack(side=tk.BOTTOM, fill=tk.X)

    return topFrame, operation_frame, input_image_frame, input_image_frame2, output_image_frame, command_frame

def setup_treeview(operation_frame):
    """Create and configure the treeview widget for image selection"""
    treeView = ttk.Treeview(operation_frame, selectmode='browse')
    # Insert root item for image list with empty parent and auto index
    rootIID = treeView.insert('',-1, text="Image List")
    treeView.pack(padx=5, pady=5)
    return treeView, rootIID

def setup_image_labels(input_image_frame, output_image_frame, input_image_data, output_image_data, default_name='apple-20.ppm'):
    if default_name not in input_image_data:
        raise ValueError(f"Default image '{default_name}' not found in imageData")

    # setup input image
    pil_input = input_image_data[default_name]["pil"]
    tk_input = input_image_data[default_name]["tk"]

    inputLabel = tk.Label(input_image_frame, image=tk_input)
    inputLabel.pack(padx=10, pady=10)

    inputLabel.original_pil = pil_input
    inputLabel.pil_image = pil_input
    inputLabel.tk_image = tk_input

    pil_output = output_image_data[default_name]["pil"]
    tk_output = output_image_data[default_name]["tk"]

    outputLabel = tk.Label(output_image_frame, image=tk_output)
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
