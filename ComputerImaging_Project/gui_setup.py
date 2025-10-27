import tkinter as tk
from tkinter import ttk
from commands import execute_command
import os
from image_ops import (
    create_negative_image, add_images, subtract_images, multiply_images,
    log_transform, power_transform, connected_component_labeling,
    connected_component_labeling_m, apply_histogram_equalization,
    apply_gaussian_smoothing, apply_edge_detection
)
from image_data import update_output_image


# create and organize all frames in the main window
def setup_frames(root):
    top_frame = tk.Frame(root)
    # Existing frames
    operation_frame = tk.Frame(top_frame)
    operation_frame2 = tk.Frame(top_frame)
    input_image_frame = tk.Frame(top_frame)
    input_image_frame2 = tk.Frame(top_frame)
    output_image_frame = tk.Frame(top_frame)
    command_frame = tk.Frame(root)

    top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # Gaussian frame is already packed to the left
    operation_frame.pack(side=tk.LEFT, fill=tk.Y)
    operation_frame2.pack(side=tk.LEFT, fill=tk.Y)
    input_image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_image_frame.pack_propagate(False)
    input_image_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_image_frame2.pack_propagate(False)
    output_image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    output_image_frame.pack_propagate(False)

    # Create Gaussian filter frame on the left
    gaussian_filter_frame = tk.Frame(command_frame)  # Fixed width for controls
    gaussian_filter_frame.pack(side=tk.RIGHT, fill=tk.Y)

    command_frame.pack(side=tk.BOTTOM, fill=tk.X)

    return (top_frame, gaussian_filter_frame, operation_frame, operation_frame2,
            input_image_frame, input_image_frame2, output_image_frame, command_frame)


# create and configure the treeview widget for image selection
def setup_treeview(operation_frame):
    tree_view = ttk.Treeview(operation_frame, selectmode='browse')
    # insert root item for image list with empty parent and auto index
    root_ID = tree_view.insert('', -1, text="Image List")
    tree_view.pack(padx=5, pady=5)
    return tree_view, root_ID


def setup_image_labels(input_image_frame, input_image_frame2, output_image_frame, input_image_data, input_image_data2,
                       output_image_data, default_name='apple-20.ppm'):
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


def setup_command_interface(command_frame, input_image_data, tree_view, root_ID, output_image_label):
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

    # binding
    command_entry.bind(
        "<Return>",
        lambda e: execute_command(e, command_entry, input_image_data, tree_view, root_ID, output_image_label,
                                  path_label)
    )


def setup_interpolation_options(command_frame):
    interpolation_var = tk.StringVar(value="nearest")
    interp_frame = tk.Frame(command_frame)
    interp_frame.pack(side=tk.LEFT, padx=10, pady=5)
    tk.Label(interp_frame, text="Interpolation:").pack(anchor="w")
    tk.Radiobutton(interp_frame, text="Nearest Neighbor", variable=interpolation_var, value="nearest").pack(anchor="w")
    tk.Radiobutton(interp_frame, text="Bilinear", variable=interpolation_var, value="bilinear").pack(anchor="w")
    return interpolation_var


def setup_gaussian_filter_panel(gaussian_filter_frame, inputLabel, outputImageLabel):
    gaussian_frame = tk.Frame(gaussian_filter_frame)
    gaussian_frame.pack(fill="x", pady=(10, 5))

    tk.Label(gaussian_frame, text="Gaussian Smoothing:", font=("Arial", 9, "bold")).pack(anchor="w")

    # Gaussian parameters frame - simplified
    gauss_param_frame = tk.Frame(gaussian_frame)
    gauss_param_frame.pack(fill="x", pady=2)

    # Kernel size input
    kernel_frame = tk.Frame(gauss_param_frame)
    kernel_frame.pack(fill="x")
    tk.Label(kernel_frame, text="Kernel Size:").pack(side=tk.LEFT)
    kernel_var = tk.StringVar(value="5")
    kernel_entry = ttk.Entry(kernel_frame, textvariable=kernel_var, width=8)
    kernel_entry.pack(side=tk.LEFT, padx=5)

    # Sigma input
    sigma_frame = tk.Frame(gauss_param_frame)
    sigma_frame.pack(fill="x", pady=2)
    tk.Label(sigma_frame, text="Sigma:").pack(side=tk.LEFT)
    sigma_var = tk.StringVar(value="1.0")
    sigma_entry = ttk.Entry(sigma_frame, textvariable=sigma_var, width=8)
    sigma_entry.pack(side=tk.LEFT, padx=5)

    # Padding mode
    padding_frame = tk.Frame(gauss_param_frame)
    padding_frame.pack(fill="x", pady=2)
    tk.Label(padding_frame, text="Padding:").pack(side=tk.LEFT)
    padding_var = tk.StringVar(value="reflect")
    padding_combo = ttk.Combobox(padding_frame, textvariable=padding_var,
                                 values=["reflect", "constant", "nearest"],
                                 width=10, state="readonly")
    padding_combo.pack(side=tk.LEFT, padx=5)

    # Apply Gaussian smoothing button
    def apply_gaussian_smoothing_operation():
        try:
            kernel_size = int(kernel_var.get())
            sigma = float(sigma_var.get())
            padding_mode = padding_var.get()

            # Validate kernel size (must be odd)
            if kernel_size % 2 == 0:
                raise ValueError("Kernel size must be odd")
            if kernel_size < 3:
                raise ValueError("Kernel size must be at least 3")
            if sigma <= 0:
                raise ValueError("Sigma must be positive")

            result = apply_gaussian_smoothing(inputLabel.pil_image, kernel_size, sigma, padding_mode)
            update_output_image(outputImageLabel, result)
            print(f"Applied Gaussian smoothing: N={kernel_size}, σ={sigma}, padding={padding_mode}")
        except ValueError as e:
            print(f"Error in Gaussian smoothing: {e}")
        except Exception as e:
            print(f"Unexpected error in Gaussian smoothing: {e}")

    gaussian_btn = tk.Button(gaussian_frame, text="Apply Gaussian Smoothing",
                             command=apply_gaussian_smoothing_operation, bg="lightblue")
    gaussian_btn.pack(fill="x", pady=2)

    # Add separator between Gaussian and Sobel
    separator = ttk.Separator(gaussian_frame, orient='horizontal')
    separator.pack(fill='x', pady=10)

    # Sobel Edge Detection section
    setup_sobel_filter_panel(gaussian_frame, inputLabel, outputImageLabel)


def setup_sobel_filter_panel(parent_frame, inputLabel, outputImageLabel):
    """Setup Sobel edge detection panel below Gaussian filter"""
    sobel_frame = tk.Frame(parent_frame)
    sobel_frame.pack(fill="x", pady=(10, 5))

    tk.Label(sobel_frame, text="Sobel Edge Detection:", font=("Arial", 9, "bold")).pack(anchor="w")

    # Sobel parameters frame
    sobel_param_frame = tk.Frame(sobel_frame)
    sobel_param_frame.pack(fill="x", pady=2)

    # Scaling factor input
    scale_frame = tk.Frame(sobel_param_frame)
    scale_frame.pack(fill="x")
    tk.Label(scale_frame, text="Scaling Factor:").pack(side=tk.LEFT)
    sobel_scale_var = tk.StringVar(value="1.0")
    sobel_scale_entry = ttk.Entry(scale_frame, textvariable=sobel_scale_var, width=8)
    sobel_scale_entry.pack(side=tk.LEFT, padx=5)

    # Apply Sobel edge detection button
    def apply_sobel_edge_detection():
        try:
            scaling_factor = float(sobel_scale_var.get())
            if scaling_factor <= 0:
                raise ValueError("Scaling factor must be positive")

            result = apply_edge_detection(inputLabel.pil_image, scaling_factor)
            update_output_image(outputImageLabel, result)
            print(f"Applied Sobel Edge Detection with scaling factor={scaling_factor}")
        except ValueError as e:
            print(f"Error in Sobel Edge Detection: {e}")
        except Exception as e:
            print(f"Unexpected error in Sobel Edge Detection: {e}")

    sobel_btn = tk.Button(sobel_frame, text="Apply Sobel Edge Detection",
                         command=apply_sobel_edge_detection, bg="lightgreen")
    sobel_btn.pack(fill="x", pady=2)


def setup_operations_panel(command_frame, inputLabel, inputLabel2, outputImageLabel):
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

    maxval = getattr(inputLabel, "maxval", 255)

    tk.Button(ops_frame, text="Negative", command=lambda: update_output_image(outputImageLabel, create_negative_image(
        inputLabel.pil_image, maxval))).pack(fill="x")
    tk.Button(ops_frame, text="Addition", command=lambda: update_output_image(outputImageLabel,
                                                                              add_images(inputLabel.pil_image,
                                                                                         inputLabel2.pil_image,
                                                                                         maxval))).pack(fill="x")
    tk.Button(ops_frame, text="Subtraction", command=lambda: update_output_image(outputImageLabel,
                                                                                 subtract_images(inputLabel.pil_image,
                                                                                                 inputLabel2.pil_image,
                                                                                                 maxval))).pack(
        fill="x")
    tk.Button(ops_frame, text="Product", command=lambda: update_output_image(outputImageLabel,
                                                                             multiply_images(inputLabel.pil_image,
                                                                                             inputLabel2.pil_image,
                                                                                             maxval))).pack(fill="x")

    def execute_log_transform():
        try:
            c_value = current_c.get()
            result = log_transform(inputLabel.pil_image, maxval, c_value)
            update_output_image(outputImageLabel, result)
            print(f"Applied Log Transform with c={c_value}")
        except Exception as e:
            print(f"Error in Log Transform: {e}")

    tk.Button(ops_frame, text="Log Transform", command=execute_log_transform).pack(fill="x")

    # power transform with parameters
    def execute_power_transform():
        try:
            c_value = current_c.get()
            gamma_value = current_gamma.get()
            result = power_transform(inputLabel.pil_image, maxval, gamma_value, c_value)
            update_output_image(outputImageLabel, result)
            print(f"Applied Power Transform with γ={gamma_value}, c={c_value}")
        except Exception as e:
            print(f"Error in Power Transform: {e}")

    tk.Button(ops_frame, text="Power Transform", command=execute_power_transform).pack(fill="x")

    tk.Button(ops_frame, text="Update Input Image w/ Output Image",
              command=lambda: update_output_image(inputLabel, outputImageLabel.pil_image)).pack(fill="x")
    tk.Button(ops_frame, text="Histogram Equalization", command=lambda: update_output_image(outputImageLabel,
                                                                                            apply_histogram_equalization(
                                                                                                inputLabel.pil_image,
                                                                                                maxval))).pack(fill="x")

    # row2: connected labeling operations
    connected_labeling_frame = tk.Frame(ops_frame)
    connected_labeling_frame.pack(fill="x", pady=(10, 0))
    tk.Label(connected_labeling_frame, text="Connected-Labeling:").pack(anchor="w")

    connected_labeling_frame = tk.Frame(connected_labeling_frame)
    connected_labeling_frame.pack(fill="x")
    tk.Button(connected_labeling_frame, text="4-Connected",
              command=lambda: update_output_image(outputImageLabel, connected_component_labeling(inputLabel, 4))).pack(
        side=tk.LEFT, fill="x", expand=True, padx=2)
    tk.Button(connected_labeling_frame, text="8-Connected",
              command=lambda: update_output_image(outputImageLabel, connected_component_labeling(inputLabel, 8))).pack(
        side=tk.LEFT, fill="x", expand=True, padx=2)
    tk.Button(connected_labeling_frame, text="M-Connected",
              command=lambda: update_output_image(outputImageLabel, connected_component_labeling_m(inputLabel))).pack(
        side=tk.LEFT, fill="x", expand=True, padx=2)

    # add tooltips or information labels
    info_label = tk.Label(ops_frame, text="Set c and γ values above, then click transform buttons", font=("Arial", 8),
                          fg="gray")
    info_label.pack(anchor="w", pady=(5, 0))

    return ops_frame