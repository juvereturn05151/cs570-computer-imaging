"""
File Name:    project_2_gui_setup.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import tkinter as tk
from tkinter import ttk

from images_ops.image_ops import (
    apply_histogram_equalization,apply_histogram_equalization_opencv,apply_gaussian_smoothing,apply_edge_detection,apply_unsharp_masking
)
from image_data import update_output_image
from utils.frequent_used_ops import validate_gaussian_smoothing_input_variables, validate_unsharp_masking_input_variables, get_max_value

def init_project_2_gui(project_2_frame, input_label, output_image_label):
    max_val = get_max_value(input_label)

    tk.Button(project_2_frame, text="Histogram Equalization", command=lambda: update_output_image(output_image_label,apply_histogram_equalization(input_label.pil_image,max_val))).pack(fill="x")
    tk.Button(project_2_frame, text="Histogram Equalization OpenCV",command=lambda: update_output_image(output_image_label,apply_histogram_equalization_opencv(input_label.pil_image,max_val))).pack(fill="x")
    tk.Label(project_2_frame, text="Gaussian Smoothing:", font=("Arial", 9, "bold")).pack(anchor="w")

    # gaussian parameters frame
    gauss_param_frame = tk.Frame(project_2_frame)
    gauss_param_frame.pack(fill="x", pady=2)

    # kernel size input
    kernel_frame = tk.Frame(gauss_param_frame)
    kernel_frame.pack(fill="x")
    tk.Label(kernel_frame, text="Kernel Size:").pack(side="left")
    kernel_var = tk.StringVar(value="5")
    kernel_entry = ttk.Entry(kernel_frame, textvariable=kernel_var, width=8)
    kernel_entry.pack(side="left", padx=5)

    # sigma input
    sigma_frame = tk.Frame(gauss_param_frame)
    sigma_frame.pack(fill="x", pady=2)
    tk.Label(sigma_frame, text="Sigma:").pack(side="left")
    sigma_var = tk.StringVar(value="1.0")
    sigma_entry = ttk.Entry(sigma_frame, textvariable=sigma_var, width=8)
    sigma_entry.pack(side="left", padx=5)

    # padding mode
    padding_frame = tk.Frame(gauss_param_frame)
    padding_frame.pack(fill="x", pady=2)
    tk.Label(padding_frame, text="Padding:").pack(side="left")
    padding_var = tk.StringVar(value="reflect")
    padding_combo = ttk.Combobox(padding_frame, textvariable=padding_var,
                                 values=["reflect", "constant", "nearest"],
                                 width=10, state="readonly")
    padding_combo.pack(side="left", padx=5)

    return kernel_var, sigma_var, padding_var

def setup_gaussian_smoothing_panel(gaussian_frame, input_label, output_image_label, kernel_var, sigma_var, padding_var):
    """Setup Gaussian Panel"""
    # apply Gaussian smoothing button
    def apply_gaussian_smoothing_operation():
        try:
            kernel_size = int(kernel_var.get())
            sigma = float(sigma_var.get())
            padding_mode = padding_var.get()

            if not validate_gaussian_smoothing_input_variables(kernel_size, sigma):
                return

            result = apply_gaussian_smoothing(input_label.pil_image, kernel_size, sigma, padding_mode, get_max_value(input_label))
            update_output_image(output_image_label, result)
            print(f"Applied Gaussian smoothing: N={kernel_size}, σ={sigma}, padding={padding_mode}")
        except ValueError as e:
            print(f"Error in Gaussian smoothing: {e}")
        except Exception as e:
            print(f"Unexpected error in Gaussian smoothing: {e}")

    gaussian_btn = tk.Button(gaussian_frame, text="Apply Gaussian Smoothing",
                             command=apply_gaussian_smoothing_operation, bg="lightblue")
    gaussian_btn.pack(fill="x", pady=2)

def setup_sobel_filter_panel(parent_frame, input_label, output_image_label):
    """Setup Sobel edge detection panel below Gaussian filter"""
    sobel_frame = tk.Frame(parent_frame)
    sobel_frame.pack(fill="x", pady=(10, 5))

    tk.Label(sobel_frame, text="Sobel Edge Detection:", font=("Arial", 9, "bold")).pack(anchor="w")

    # sobel parameters frame
    sobel_param_frame = tk.Frame(sobel_frame)
    sobel_param_frame.pack(fill="x", pady=2)

    # scaling factor input
    scale_frame = tk.Frame(sobel_param_frame)
    scale_frame.pack(fill="x")
    tk.Label(scale_frame, text="Scaling Factor:").pack(side="left")
    sobel_scale_var = tk.StringVar(value="1.0")
    sobel_scale_entry = ttk.Entry(scale_frame, textvariable=sobel_scale_var, width=8)
    sobel_scale_entry.pack(side="left", padx=5)

    # apply Sobel edge detection button
    def apply_sobel_edge_detection():
        try:
            scaling_factor = float(sobel_scale_var.get())
            if scaling_factor <= 0:
                raise ValueError("Scaling factor must be positive")

            result = apply_edge_detection(input_label.pil_image, scaling_factor, get_max_value(input_label))
            update_output_image(output_image_label, result)
            print(f"Applied Sobel Edge Detection with scaling factor={scaling_factor}")
        except ValueError as e:
            print(f"Error in Sobel Edge Detection: {e}")
        except Exception as e:
            print(f"Unexpected error in Sobel Edge Detection: {e}")

    sobel_btn = tk.Button(sobel_frame, text="Apply Sobel Edge Detection",command=apply_sobel_edge_detection, bg="lightgreen")
    sobel_btn.pack(fill="x", pady=2)

def setup_unsharp_masking_panel(parent_frame, input_label, output_image_label, kernel_var, sigma_var, padding_var):
    """Setup Unsharp Masking panel below Sobel edge detection"""
    unsharp_frame = tk.Frame(parent_frame)
    unsharp_frame.pack(fill="x", pady=(10, 5))

    tk.Label(unsharp_frame, text="Unsharp Masking:", font=("Arial", 9, "bold")).pack(anchor="w")

    # unsharp Masking parameters frame
    unsharp_param_frame = tk.Frame(unsharp_frame)
    unsharp_param_frame.pack(fill="x", pady=2)

    # scaling factor k input
    k_frame = tk.Frame(unsharp_param_frame)
    k_frame.pack(fill="x")
    tk.Label(k_frame, text="Scaling Factor k:").pack(side="left")
    k_var = tk.StringVar(value="1.0")
    k_entry = ttk.Entry(k_frame, textvariable=k_var, width=8)
    k_entry.pack(side="left", padx=5)

    # info label explaining the parameters
    info_label = tk.Label(unsharp_param_frame,text="Uses Gaussian params above for blurring",font=("Arial", 7), fg="gray")
    info_label.pack(anchor="w", pady=(2, 0))

    # apply Unsharp Masking button
    def apply_unsharp_masking_operation():
        try:
            kernel_size = int(kernel_var.get())
            sigma = float(sigma_var.get())
            padding_mode = padding_var.get()
            k_value = float(k_var.get())

            if not validate_unsharp_masking_input_variables(kernel_size, sigma, k_value):
                return

            result = apply_unsharp_masking(input_label.pil_image, kernel_size, sigma, k_value, padding_mode, get_max_value(input_label))
            update_output_image(output_image_label, result)
            print(f"Applied Unsharp Masking: N={kernel_size}, σ={sigma}, k={k_value}, padding={padding_mode}")
        except Exception as e:
            print(f"Unexpected error in Unsharp Masking: {e}")

    unsharp_btn = tk.Button(unsharp_frame, text="Apply Unsharp Masking", command=apply_unsharp_masking_operation, bg="lightcoral")
    unsharp_btn.pack(fill="x", pady=2)