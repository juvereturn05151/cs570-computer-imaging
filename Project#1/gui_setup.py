import tkinter as tk
from tkinter import ttk
from commands import execute_command
import os
from image_ops import (
    create_negative_image, add_images, subtract_images, multiply_images,
    log_transform, power_transform, connected_component_labeling, connected_component_labeling_m
)
from image_data import update_output_image

def setup_frames(root):
    """Create and organize all frames in the main window"""
    topFrame = tk.Frame(root)
    operation_frame = tk.Frame(topFrame)
    operation_frame2 = tk.Frame(topFrame)
    input_image_frame = tk.Frame(topFrame)
    input_image_frame2 = tk.Frame(topFrame)
    output_image_frame = tk.Frame(topFrame)
    command_frame = tk.Frame(root)

    topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    operation_frame.pack(side=tk.LEFT, fill=tk.Y)
    operation_frame2.pack(side=tk.LEFT, fill=tk.Y)

    input_image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_image_frame.pack_propagate(False)

    input_image_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_image_frame2.pack_propagate(False)

    output_image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    output_image_frame.pack_propagate(False)

    command_frame.pack(side=tk.BOTTOM, fill=tk.X)

    return topFrame, operation_frame, operation_frame2,input_image_frame, input_image_frame2, output_image_frame, command_frame

def setup_treeview(operation_frame):
    """Create and configure the treeview widget for image selection"""
    treeView = ttk.Treeview(operation_frame, selectmode='browse')
    # Insert root item for image list with empty parent and auto index
    rootIID = treeView.insert('',-1, text="Image List")
    treeView.pack(padx=5, pady=5)
    return treeView, rootIID

def setup_image_labels(input_image_frame, input_image_frame2, output_image_frame, input_image_data, input_image_data2, output_image_data, default_name='apple-20.ppm'):
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

    # setup input image2
    pil_input = input_image_data2[default_name]["pil"]
    tk_input = input_image_data2[default_name]["tk"]


    inputLabel2 = tk.Label(input_image_frame2, image=tk_input)
    inputLabel2.pack(padx=10, pady=10)

    inputLabel2.original_pil = pil_input
    inputLabel2.pil_image = pil_input
    inputLabel2.tk_image = tk_input

    # setup output image
    pil_output = output_image_data[default_name]["pil"]
    tk_output = output_image_data[default_name]["tk"]

    outputLabel = tk.Label(output_image_frame, image=tk_output)
    outputLabel.pack(padx=10, pady=10)

    outputLabel.original_pil = pil_output
    outputLabel.pil_image = pil_output
    outputLabel.tk_image = tk_output

    return inputLabel, inputLabel2, outputLabel


def setup_command_interface(commandFrame, input_image_data, treeView, rootIID, outputImageLabel):
    """
    Sets up the command interface with:
    1. A label showing the current working path.
    2. An entry for user commands.
    """

    # 1️⃣ Show current path at the top
    current_path = os.getcwd()
    path_label = tk.Label(commandFrame, text=f"Current Path: {current_path}", anchor="w", fg="blue")
    path_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

    # 2️⃣ Command label
    commandLabel = tk.Label(commandFrame, text="Execute command:")
    commandLabel.pack(side=tk.LEFT, padx=5, pady=5)

    # 3️⃣ Command entry
    command_entry = ttk.Entry(commandFrame)
    command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

    # Bind Enter key to execute command
    command_entry.bind(
        "<Return>",
        lambda e: execute_command(e, command_entry, input_image_data, treeView, rootIID, outputImageLabel, path_label)
    )

    return command_entry, path_label

def setup_interpolation_options(command_frame):
    interpolation_var = tk.StringVar(value="nearest")

    interp_frame = tk.Frame(command_frame)
    interp_frame.pack(side=tk.LEFT, padx=10, pady=5)

    tk.Label(interp_frame, text="Interpolation:").pack(anchor="w")

    tk.Radiobutton(
        interp_frame, text="Nearest Neighbor", variable=interpolation_var, value="nearest"
    ).pack(anchor="w")

    tk.Radiobutton(
        interp_frame, text="Bilinear", variable=interpolation_var, value="bilinear"
    ).pack(anchor="w")

    return interpolation_var


def setup_operations_panel(command_frame, inputLabel, inputLabel2, outputImageLabel):

    ops_frame = tk.Frame(command_frame)
    ops_frame.pack(side=tk.LEFT, padx=10, pady=5)

    tk.Label(ops_frame, text="Operations:").pack(anchor="w")

    # Create parameter frame for transform operations
    param_frame = tk.Frame(ops_frame)
    param_frame.pack(fill="x", pady=5)

    # Parameter variables
    c_var = tk.DoubleVar(value=1.0)
    gamma_var = tk.DoubleVar(value=1.0)

    # Parameter input widgets
    tk.Label(param_frame, text="c:").pack(side=tk.LEFT, padx=2)
    c_entry = ttk.Entry(param_frame, textvariable=c_var, width=6)
    c_entry.pack(side=tk.LEFT, padx=2)

    tk.Label(param_frame, text="γ:").pack(side=tk.LEFT, padx=2)
    gamma_entry = ttk.Entry(param_frame, textvariable=gamma_var, width=6)
    gamma_entry.pack(side=tk.LEFT, padx=2)

    update_param_btn = tk.Button(param_frame, text="Update Params", command=lambda: update_parameters(c_var, gamma_var))
    update_param_btn.pack(side=tk.LEFT, padx=5)

    # Store current parameters for operations
    current_c = tk.DoubleVar(value=1.0)
    current_gamma = tk.DoubleVar(value=1.0)

    def update_parameters(c_var, gamma_var):
        try:
            c_value = float(c_var.get())
            gamma_value = float(gamma_var.get())
            current_c.set(c_value)
            current_gamma.set(gamma_value)
            print(f"Parameters updated: c={c_value}, γ={gamma_value}")
        except ValueError:
            print("Invalid parameter values. Please enter numbers.")

    tk.Button(ops_frame, text="Negative", command=lambda: update_output_image(outputImageLabel, create_negative_image(inputLabel))).pack(fill="x")

    tk.Button(ops_frame, text="Addition", command=lambda: update_output_image(outputImageLabel, add_images(inputLabel, inputLabel2))).pack(fill="x")

    tk.Button(ops_frame, text="Subtraction", command=lambda: update_output_image(outputImageLabel,subtract_images(inputLabel, inputLabel2))).pack(fill="x")

    tk.Button(ops_frame, text="Product", command=lambda: update_output_image(outputImageLabel,multiply_images(inputLabel, inputLabel2))).pack(fill="x")

    def execute_log_transform():
        try:
            c_value = current_c.get()
            result = log_transform(inputLabel, c_value)
            update_output_image(outputImageLabel, result)
            print(f"Applied Log Transform with c={c_value}")
        except Exception as e:
            print(f"Error in Log Transform: {e}")

    tk.Button(ops_frame, text="Log Transform", command=execute_log_transform).pack(fill="x")

    # Power Transform with parameters
    def execute_power_transform():
        try:
            c_value = current_c.get()
            gamma_value = current_gamma.get()
            result = power_transform(inputLabel, gamma_value, c_value)
            update_output_image(outputImageLabel, result)
            print(f"Applied Power Transform with γ={gamma_value}, c={c_value}")
        except Exception as e:
            print(f"Error in Power Transform: {e}")

    tk.Button(ops_frame, text="Power Transform", command=execute_power_transform).pack(fill="x")

    # Row 2: topology operations
    topology_frame = tk.Frame(ops_frame)
    topology_frame.pack(fill="x", pady=(10, 0))

    tk.Label(topology_frame, text="Topology:").pack(anchor="w")

    topology_btn_frame = tk.Frame(topology_frame)
    topology_btn_frame.pack(fill="x")

    tk.Button(topology_btn_frame, text="4-Connected",
              command=lambda: update_output_image(outputImageLabel, connected_component_labeling(inputLabel, 4))).pack(
        side=tk.LEFT, fill="x", expand=True, padx=2)

    tk.Button(topology_btn_frame, text="8-Connected",
              command=lambda: update_output_image(outputImageLabel, connected_component_labeling(inputLabel, 8))).pack(
        side=tk.LEFT, fill="x", expand=True, padx=2)

    tk.Button(topology_btn_frame, text="M-Connected",
              command=lambda: update_output_image(outputImageLabel, connected_component_labeling_m(inputLabel))).pack(
        side=tk.LEFT, fill="x", expand=True, padx=2)

    # Add tooltips or information labels
    info_label = tk.Label(ops_frame, text="Set c and γ values above, then click transform buttons",
                          font=("Arial", 8), fg="gray")
    info_label.pack(anchor="w", pady=(5, 0))

    return ops_frame