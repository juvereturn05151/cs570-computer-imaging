"""
File Name:    unsharp_masking.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import tkinter as tk
from tkinter import ttk
import os

from utils.commands import execute_command
from images_ops.image_ops import (
    create_negative_image, add_images, subtract_images, multiply_images,
    log_transform, power_transform, connected_component_labeling,
    connected_component_labeling_m,
)
from ui.project_2_gui_setup import(
    init_project_2_gui,setup_gaussian_smoothing_panel,setup_sobel_filter_panel,setup_unsharp_masking_panel
)
from image_data import update_output_image

def setup_frames(root):
    """Create and organize all frames in the main window"""
    top_frame = tk.Frame(root)
    operation_frame = tk.Frame(top_frame)
    operation_frame2 = tk.Frame(top_frame)
    input_image_frame = tk.Frame(top_frame)
    input_image_frame2 = tk.Frame(top_frame)
    output_image_frame = tk.Frame(top_frame)
    command_frame = tk.Frame(root)

    top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    operation_frame.pack(side=tk.LEFT, fill=tk.Y)
    operation_frame2.pack(side=tk.LEFT, fill=tk.Y)
    input_image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_image_frame.pack_propagate(False)
    input_image_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_image_frame2.pack_propagate(False)
    output_image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    output_image_frame.pack_propagate(False)

    project_2_filter_frame = tk.Frame(command_frame)
    project_2_filter_frame.pack(side=tk.RIGHT, fill=tk.Y)

    command_frame.pack(side=tk.BOTTOM, fill=tk.X)

    return (top_frame, project_2_filter_frame, operation_frame, operation_frame2,
            input_image_frame, input_image_frame2, output_image_frame, command_frame)

def setup_treeview(operation_frame):
    """Create and configure the treeview widget for image selection"""
    tree_view = ttk.Treeview(operation_frame, selectmode='browse')

    # insert root item for image list with empty parent and auto index
    root_id = tree_view.insert('', -1, text="Image List")
    tree_view.pack(padx=5, pady=5)
    return tree_view, root_id

def setup_image_labels(input_image_frame, input_image_frame2, output_image_frame, input_image_data, input_image_data2, output_image_data, default_name='apple-20.ppm'):
    """Create and configure the labels widget for image selection"""
    
    if default_name not in input_image_data:
        raise ValueError(f"Default image '{default_name}' not found in imageData")

    # setup input image
    pil_input = input_image_data[default_name]["pil"]
    tk_input = input_image_data[default_name]["tk"]
    input_label = tk.Label(input_image_frame, image=tk_input)
    input_label.pack(padx=10, pady=10)
    input_label.original_pil = pil_input
    input_label.pil_image = pil_input
    input_label.tk_image = tk_input

    # setup input image2
    pil_input = input_image_data2[default_name]["pil"]
    tk_input = input_image_data2[default_name]["tk"]
    input_label2 = tk.Label(input_image_frame2, image=tk_input)
    input_label2.pack(padx=10, pady=10)
    input_label2.original_pil = pil_input
    input_label2.pil_image = pil_input
    input_label2.tk_image = tk_input

    # setup output image
    pil_output = output_image_data[default_name]["pil"]
    tk_output = output_image_data[default_name]["tk"]
    output_label = tk.Label(output_image_frame, image=tk_output)
    output_label.pack(padx=10, pady=10)
    output_label.original_pil = pil_output
    output_label.pil_image = pil_output
    output_label.tk_image = tk_output

    return input_label, input_label2, output_label

def setup_command_interface(command_frame, input_image_data, tree_view, root_id, output_image_label):
    """Create and configure the command interface widget for various operations"""

    # show current path at the top
    current_path = os.getcwd()
    path_label = tk.Label(command_frame, text=f"Current Path: {current_path}", anchor="w", fg="blue")
    path_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

    # execute command label
    command_label = tk.Label(command_frame, text="Execute command:")
    command_label.pack(side=tk.LEFT, padx=5, pady=5)

    # command entry
    command_entry = ttk.Entry(command_frame)
    command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

    # binding with "Enter" button
    command_entry.bind( "<Return>", lambda e: execute_command(e, command_entry, input_image_data, tree_view, root_id, output_image_label,path_label))

def setup_interpolation_options(command_frame):
    """Create interpolation radio buttons when the images change their sizes due to either expanding and shrinking the window"""
    interpolation_var = tk.StringVar(value="nearest")
    interp_frame = tk.Frame(command_frame)
    interp_frame.pack(side=tk.LEFT, padx=10, pady=5)
    tk.Label(interp_frame, text="Interpolation:").pack(anchor="w")
    tk.Radiobutton(interp_frame, text="Nearest Neighbor", variable=interpolation_var, value="nearest").pack(anchor="w")
    tk.Radiobutton(interp_frame, text="Bilinear", variable=interpolation_var, value="bilinear").pack(anchor="w")
    return interpolation_var

def setup_project_2_filter_panel(project_2_filter_frame, input_label, output_image_label):
    project_2_frame = tk.Frame(project_2_filter_frame)
    project_2_frame.pack(fill="x", pady=(10, 5))

    kernel_var, sigma_var, padding_var = init_project_2_gui(project_2_frame, input_label, output_image_label)

    setup_gaussian_smoothing_panel(project_2_frame, input_label, output_image_label, kernel_var, sigma_var, padding_var)

    # add separator between Gaussian and Sobel
    separator1 = ttk.Separator(project_2_frame, orient='horizontal')
    separator1.pack(fill='x', pady=10)

    # sobel Edge Detection section
    setup_sobel_filter_panel(project_2_frame, input_label, output_image_label)

    # add separator between Sobel and Unsharp Masking
    separator2 = ttk.Separator(project_2_frame, orient='horizontal')
    separator2.pack(fill='x', pady=10)

    # unsharp Masking section
    setup_unsharp_masking_panel(project_2_frame, input_label, output_image_label, kernel_var, sigma_var, padding_var)

def setup_operations_panel(command_frame, inputLabel, inputLabel2, output_image_label):
    ops_frame = tk.Frame(command_frame)
    ops_frame.pack(side=tk.LEFT, padx=10, pady=5)

    tk.Label(ops_frame, text="Operations:").pack(anchor="w")

    # create parameter frame for transform operations
    param_frame = tk.Frame(ops_frame)
    param_frame.pack(fill="x", pady=5)

    # parameter variables
    c_var = tk.DoubleVar(value=1.0)
    gamma_var = tk.DoubleVar(value=1.0)

    # parameter input widgets
    tk.Label(param_frame, text="c:").pack(side=tk.LEFT, padx=2)
    c_entry = ttk.Entry(param_frame, textvariable=c_var, width=6)
    c_entry.pack(side=tk.LEFT, padx=2)

    tk.Label(param_frame, text="γ:").pack(side=tk.LEFT, padx=2)
    gamma_entry = ttk.Entry(param_frame, textvariable=gamma_var, width=6)
    gamma_entry.pack(side=tk.LEFT, padx=2)

    update_param_btn = tk.Button(param_frame, text="Update Params", command=lambda: update_parameters(c_var, gamma_var))
    update_param_btn.pack(side=tk.LEFT, padx=5)

    # store current parameters for operations
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

    max_val = getattr(inputLabel, "max_val", 255)

    tk.Button(ops_frame, text="Negative", command=lambda: update_output_image(output_image_label, create_negative_image(inputLabel.pil_image, max_val))).pack(fill="x")
    tk.Button(ops_frame, text="Addition", command=lambda: update_output_image(output_image_label,add_images(inputLabel.pil_image,inputLabel2.pil_image,max_val))).pack(fill="x")
    tk.Button(ops_frame, text="Subtraction", command=lambda: update_output_image(output_image_label,subtract_images(inputLabel.pil_image,inputLabel2.pil_image,max_val))).pack(fill="x")
    tk.Button(ops_frame, text="Product", command=lambda: update_output_image(output_image_label,multiply_images(inputLabel.pil_image,inputLabel2.pil_image,max_val))).pack(fill="x")
    tk.Button(ops_frame, text="Update Input Image w/ Output Image", command=lambda: update_output_image(inputLabel, output_image_label.pil_image)).pack(fill="x")

    def execute_log_transform():
        try:
            c_value = current_c.get()
            result = log_transform(inputLabel.pil_image, max_val, c_value)
            update_output_image(output_image_label, result)
            print(f"Applied Log Transform with c={c_value}")
        except Exception as e:
            print(f"Error in Log Transform: {e}")

    tk.Button(ops_frame, text="Log Transform", command=execute_log_transform).pack(fill="x")

    # power transform with parameters
    def execute_power_transform():
        try:
            c_value = current_c.get()
            gamma_value = current_gamma.get()
            result = power_transform(inputLabel.pil_image, max_val, gamma_value, c_value)
            update_output_image(output_image_label, result)
            print(f"Applied Power Transform with γ={gamma_value}, c={c_value}")
        except Exception as e:
            print(f"Error in Power Transform: {e}")

    tk.Button(ops_frame, text="Power Transform", command=execute_power_transform).pack(fill="x")

    # row2: connected labeling operations
    connected_labeling_frame = tk.Frame(ops_frame)
    connected_labeling_frame.pack(fill="x", pady=(10, 0))
    tk.Label(connected_labeling_frame, text="Connected-Labeling:").pack(anchor="w")

    connected_labeling_frame = tk.Frame(connected_labeling_frame)
    connected_labeling_frame.pack(fill="x")
    tk.Button(connected_labeling_frame, text="4-Connected",command=lambda: update_output_image(output_image_label, connected_component_labeling(inputLabel, 4))).pack(side=tk.LEFT, fill="x", expand=True, padx=2)
    tk.Button(connected_labeling_frame, text="8-Connected",command=lambda: update_output_image(output_image_label, connected_component_labeling(inputLabel, 8))).pack(side=tk.LEFT, fill="x", expand=True, padx=2)
    tk.Button(connected_labeling_frame, text="M-Connected",command=lambda: update_output_image(output_image_label, connected_component_labeling_m(inputLabel))).pack(side=tk.LEFT, fill="x", expand=True, padx=2)

    # add tooltips or information labels
    info_label = tk.Label(ops_frame, text="Set c and γ values above, then click transform buttons", font=("Arial", 8), fg="gray")
    info_label.pack(anchor="w", pady=(5, 0))

    return ops_frame