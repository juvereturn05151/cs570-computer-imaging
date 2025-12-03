"""
File Name:    gui_setup.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import tkinter as tk
from tkinter import ttk
import os

from utils.commands import execute_command
from images_ops.image_ops import (
    create_negative_image, add_images, subtract_images, multiply_images,
)
from ui.project_1_gui_setup import(
    init_project_1_gui,setup_log_transform_panel,setup_power_transform_panel, setup_connected_component_labeling
)
from ui.project_2_gui_setup import(
    init_project_2_gui,setup_gaussian_smoothing_panel,setup_sobel_filter_panel,setup_unsharp_masking_panel
)

from ui.project_3_gui_setup import(
    init_project_3_gui
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

    top_frame.pack(side="top", fill="both", expand=True)
    operation_frame.pack(side="left", fill="y")
    operation_frame2.pack(side="left", fill="y")

    # add titles above the image frame
    tk.Label(input_image_frame, text="Input Image 1", font=("Arial", 10, "bold")).pack(side="top", pady=(5,0))
    tk.Label(input_image_frame2, text="Input Image 2", font=("Arial", 10, "bold")).pack(side="top", pady=(5,0))
    tk.Label(output_image_frame, text="Output Image", font=("Arial", 10, "bold")).pack(side="top", pady=(5,0))

    input_image_frame.pack(side="left", fill="both", expand=True)
    input_image_frame.pack_propagate(False)
    input_image_frame2.pack(side="left", fill="both", expand=True)
    input_image_frame2.pack_propagate(False)
    output_image_frame.pack(side="right", fill="both", expand=True)
    output_image_frame.pack_propagate(False)

    project_3_fourier_frame = tk.Frame(command_frame)
    project_3_fourier_frame.pack(side="right", fill="y", padx=5)

    project_2_filter_frame = tk.Frame(command_frame)
    project_2_filter_frame.pack(side="right", fill="y")

    command_frame.pack(side="bottom", fill="x")

    return (top_frame, project_2_filter_frame, project_3_fourier_frame, operation_frame, operation_frame2,
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
    pil_input = input_image_data[default_name].pil
    tk_input = input_image_data[default_name].tk
    input_label = tk.Label(input_image_frame, image=tk_input)
    input_label.pack(padx=10, pady=10)
    input_label.original_pil = pil_input
    input_label.pil_image = pil_input
    input_label.tk_image = tk_input

    # setup input image2
    pil_input = input_image_data2[default_name].pil
    tk_input = input_image_data2[default_name].tk
    input_label2 = tk.Label(input_image_frame2, image=tk_input)
    input_label2.pack(padx=10, pady=10)
    input_label2.original_pil = pil_input
    input_label2.pil_image = pil_input
    input_label2.tk_image = tk_input

    # setup output image
    pil_output = output_image_data[default_name].pil
    tk_output = output_image_data[default_name].tk
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
    path_label.pack(side="top", fill="x", padx=5, pady=2)

    # execute command label
    command_label = tk.Label(command_frame, text="Execute command:")
    command_label.pack(side="left", padx=5, pady=5)

    # command entry
    command_entry = ttk.Entry(command_frame)
    command_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    # binding with "Enter" button
    command_entry.bind( "<Return>", lambda e: execute_command(e, command_entry, input_image_data, tree_view, root_id, output_image_label,path_label))

def setup_interpolation_options(command_frame):
    """Create interpolation radio buttons when the images change their sizes due to either expanding and shrinking the window"""
    interpolation_var = tk.StringVar(value="nearest")
    interp_frame = tk.Frame(command_frame)
    interp_frame.pack(side="left", padx=10, pady=5)
    tk.Label(interp_frame, text="Interpolation:").pack(anchor="w")
    tk.Radiobutton(interp_frame, text="Nearest Neighbor", variable=interpolation_var, value="nearest").pack(anchor="w")
    tk.Radiobutton(interp_frame, text="Bilinear", variable=interpolation_var, value="bilinear").pack(anchor="w")
    tk.Radiobutton(interp_frame, text="None", variable=interpolation_var, value="none").pack(anchor="w")
    return interpolation_var

def setup_project_1_operations_panel(command_frame, input_label, input_label2, output_image_label):
    """Create and configure the project 1 panel widget for various operations"""
    ops_frame = tk.Frame(command_frame)
    ops_frame.pack(side="left", padx=10, pady=5)

    tk.Label(ops_frame, text="PROJECT 1: Basic Operations", font=("Arial", 10, "bold")).pack(anchor="center", pady=(0, 10))

    c_var, gamma_var = init_project_1_gui(ops_frame)

    max_val = getattr(input_label, "max_val", 255)

    tk.Button(ops_frame, text="Negative", command=lambda: update_output_image(output_image_label, create_negative_image(input_label.pil_image, max_val))).pack(fill="x")
    tk.Button(ops_frame, text="Addition", command=lambda: update_output_image(output_image_label,add_images(input_label.pil_image,input_label2.pil_image,max_val))).pack(fill="x")
    tk.Button(ops_frame, text="Subtraction", command=lambda: update_output_image(output_image_label,subtract_images(input_label.pil_image,input_label2.pil_image,max_val))).pack(fill="x")
    tk.Button(ops_frame, text="Product", command=lambda: update_output_image(output_image_label,multiply_images(input_label.pil_image,input_label2.pil_image,max_val))).pack(fill="x")

    setup_log_transform_panel(ops_frame, input_label, output_image_label, max_val, c_var)

    setup_power_transform_panel(ops_frame, input_label, output_image_label, max_val, c_var, gamma_var)

    tk.Button(ops_frame, text="Update Input Image w/ Output Image",command=lambda: update_output_image(input_label, output_image_label.pil_image)).pack(fill="x")

    # row2: connected labeling operations
    setup_connected_component_labeling(ops_frame, input_label, output_image_label)

    # add tooltips or information labels
    info_label = tk.Label(ops_frame, text="Enter c and γ values, then click transform buttons", font=("Arial", 8), fg="gray")
    info_label.pack(anchor="w", pady=(5, 0))

    return ops_frame

def setup_project_2_filter_panel(project_2_filter_frame, input_label, output_image_label):
    """Create and configure the project 2 panel widget for various filtering operations"""
    project_2_frame = tk.Frame(project_2_filter_frame)
    project_2_frame.pack(fill="x", pady=(10, 5))

    tk.Label(project_2_frame, text="PROJECT 2: Filtering Operations", font=("Arial", 10, "bold")).pack(anchor="center", pady=(0, 10))

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

def setup_project_3_fourier_panel(command_frame, input_label, input_label2, output_image_label):
    """
    Create and configure the Project 3 UI panel for Fourier Transform operations.

    input_label      -> Original image
    input_label2     -> Spectrum image (magnitude/log)
    output_image_label -> Reconstructed image (inverse FT result)
    """
    project_3_frame = tk.Frame(command_frame)
    project_3_frame.pack(side="right", padx=10, pady=10)

    tk.Label(project_3_frame, text="PROJECT 3: Fourier Transform", font=("Arial", 10, "bold")).pack(anchor="center", pady=(0, 10))

    init_project_3_gui(project_3_frame, input_label, input_label2, output_image_label)

    return project_3_frame