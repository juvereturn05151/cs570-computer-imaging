"""
File Name:    commands.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import tkinter as tk
import os

from ui.gui import load_image, save_output_image
from images_ops.image_ops import (
    create_negative_image, add_images, subtract_images, multiply_images,
    log_transform, power_transform, apply_histogram_equalization,
    apply_gaussian_smoothing, apply_edge_detection, apply_unsharp_masking
)
from image_data import update_output_image  # Import this function
from utils.frequent_used_ops import validate_gaussian_smoothing_input_variables, validate_unsharp_masking_input_variables

def parse_command_args(tokens, flag):
    """Use to extract command line arguments"""
    if flag not in tokens:
        return None
    idx = tokens.index(flag)

    # return all args until next "-" or end
    args = []
    for t in tokens[idx + 1:]:
        if t.startswith("-"):
            break
        args.append(t)
    return args if len(args) > 1 else (args[0] if args else None)


def execute_command(event=None, command_entry=None, image_data=None, tree_view=None, root_id=None, output_image_label=None, path_label=None):
    """Event-based command-line interface that works when the user presses the command"""
    cmd = command_entry.get().strip()
    command_entry.delete(0, tk.END)

    if not cmd:
        return

    tokens = cmd.split()
    op = tokens[0].lower()

    # directory navigation
    if op == "cd":
        if len(tokens) < 2:
            print("Usage: cd <directory>")
            return
        new_dir = " ".join(tokens[1:])
        if os.path.isdir(new_dir):
            os.chdir(new_dir)
            print(f"Changed directory to: {os.getcwd()}")
            if path_label:
                path_label.config(text=f"Current Path: {os.getcwd()}")
        else:
            print(f"Directory not found: {new_dir}")
        return

    # load
    if op == "load":
        inputs = parse_command_args(tokens, "-i")
        if not inputs:
            inputs = tokens[1:]  # fallback
        for f in (inputs if isinstance(inputs, list) else [inputs]):
            file_path = os.path.join(os.getcwd(), f)
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
            load_image(f, image_data, tree_view, root_id)
            print(f"Loaded {f}")
        return

    # save
    if op == "save":
        out_file = parse_command_args(tokens, "-o") or (tokens[1] if len(tokens) > 1 else None)
        if not out_file:
            print("Usage: save -o <output file>")
            return
        save_output_image(out_file, output_image_label)
        print(f"Saved {out_file}")
        return

    # image operations
    input_files = parse_command_args(tokens, "-i")
    output_file = parse_command_args(tokens, "-o")

    if not input_files:
        print("Missing input file(s). Use -i <file(s)>")
        return
    if not output_file:
        print("Missing output file. Use -o <file>")
        return

    # ensure that the list exists
    if isinstance(input_files, str):
        input_files = [input_files]

    # load input images as PIL
    from PIL import Image
    input_pils = [Image.open(os.path.join(os.getcwd(), f)) for f in input_files]

    max_val = getattr(input_pils[0], "max_val", 255)

    # Handle multiple operations and filters
    if op == "add":
        result = add_images(input_pils[0], input_pils[1], max_val)
    elif op == "sub":
        result = subtract_images(input_pils[0], input_pils[1], max_val)
    elif op == "mul":
        result = multiply_images(input_pils[0], input_pils[1], max_val)
    elif op == "inv":
        result = create_negative_image(input_pils[0], max_val)
    elif op == "log":
        c_val = float(parse_command_args(tokens, "-c") or 1.0)
        result = log_transform(input_pils[0], max_val, c=c_val)
    elif op == "pow":
        c_val = float(parse_command_args(tokens, "-c") or 1.0)
        gamma_val = float(parse_command_args(tokens, "-gamma") or 1.0)
        result = power_transform(input_pils[0], max_val, gamma=gamma_val, c=c_val)
    elif op == "histeq":  # Histogram equalization command
        if len(input_files) != 1:
            print("Histogram equalization requires exactly one input file")
            return
        result = apply_histogram_equalization(input_pils[0], max_val)
    elif op == "gblur":  # Gaussian blur command
        if len(input_files) != 1:
            print("Gaussian blur requires exactly one input file")
            return

        # Parse Gaussian blur parameters
        n_val = parse_command_args(tokens, "-N")
        sigma_val = parse_command_args(tokens, "-sigma")

        if not n_val:
            print("Missing kernel size. Use -N <size>")
            return
        if not sigma_val:
            print("Missing sigma value. Use -sigma <value>")
            return

        try:
            kernel_size = int(n_val)
            sigma = float(sigma_val)

            if not validate_gaussian_smoothing_input_variables(kernel_size, sigma):
                return

            # Apply Gaussian blur with default padding mode
            result = apply_gaussian_smoothing(input_pils[0], kernel_size, sigma, 'reflect')
            print(f"Applied Gaussian blur: N={kernel_size}, σ={sigma}")

        except ValueError as e:
            print(f"Error in Gaussian blur parameters: {e}")
            return
    elif op == "sobel":  # Sobel edge detection command
        if len(input_files) != 1:
            print("Sobel edge detection requires exactly one input file")
            return

        # Parse optional scaling factor
        scale_val = parse_command_args(tokens, "-scale")
        scaling_factor = float(scale_val) if scale_val else 1.0

        try:
            # Validate scaling factor
            if scaling_factor <= 0:
                print("Error: Scaling factor must be positive")
                return

            # Apply Sobel edge detection
            result = apply_edge_detection(input_pils[0], scaling_factor)
            print(f"Applied Sobel edge detection with scaling factor={scaling_factor}")

        except ValueError as e:
            print(f"Error in Sobel parameters: {e}")
            return
    elif op == "unsharp":  # Unsharp masking command
        if len(input_files) != 1:
            print("Unsharp masking requires exactly one input file")
            return

        # Parse unsharp masking parameters
        n_val = parse_command_args(tokens, "-N")
        sigma_val = parse_command_args(tokens, "-sigma")
        k_val = parse_command_args(tokens, "-k")

        # Set defaults if not provided
        kernel_size = int(n_val) if n_val else 5
        sigma = float(sigma_val) if sigma_val else 1.0
        k = float(k_val) if k_val else 1.0

        try:
            # Validate parameters
            if not validate_unsharp_masking_input_variables(kernel_size, sigma, k):
                return

            if kernel_size % 2 == 0:
                print("Error: Kernel size must be odd")
                return
            if kernel_size < 3:
                print("Error: Kernel size must be at least 3")
                return
            if sigma <= 0:
                print("Error: Sigma must be positive")
                return
            if k <= 0:
                print("Error: Scaling factor k must be positive")
                return

            #apply unsharp masking
            result = apply_unsharp_masking(input_pils[0], kernel_size, sigma, k, 'reflect')
            print(f"Applied unsharp masking: N={kernel_size}, σ={sigma}, k={k}")

        except ValueError as e:
            print(f"Error in unsharp masking parameters: {e}")
            return
    else:
        print(f"Unknown operation: {op}")
        return

    #save result to file
    output_path = os.path.join(os.getcwd(), output_file)
    result.save(output_path)
    print(f"{op.upper()} operation complete. Saved as {output_file}")

    #update the output panel with the result
    if output_image_label:
        update_output_image(output_image_label, result)
        print(f"Output panel updated with {output_file}")