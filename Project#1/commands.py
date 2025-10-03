import tkinter as tk
import os
from gui import load_image, save_output_image
from image_ops import (
    create_negative_image, add_images, subtract_images, multiply_images,
    log_transform, power_transform
)

def parse_command_args(tokens, flag):
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


def execute_command(event=None, command_entry=None,
                    imageData=None, treeView=None, rootIID=None,
                    outputImageLabel=None, path_label=None):
    cmd = command_entry.get().strip()
    command_entry.delete(0, tk.END)

    if not cmd:
        return

    tokens = cmd.split()
    op = tokens[0].lower()

    # ---------- Directory navigation ----------
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

    #load/save
    if op == "load":
        inputs = parse_command_args(tokens, "-i")
        if not inputs:
            inputs = tokens[1:]  # fallback
        for f in (inputs if isinstance(inputs, list) else [inputs]):
            file_path = os.path.join(os.getcwd(), f)
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
            load_image(f, imageData, treeView, rootIID)
            print(f"Loaded {f}")
        return

    if op == "save":
        out_file = parse_command_args(tokens, "-o") or (tokens[1] if len(tokens) > 1 else None)
        if not out_file:
            print("Usage: save -o <output file>")
            return
        save_output_image(out_file, outputImageLabel)
        print(f"Saved {out_file}")
        return

    #image operations
    input_files = parse_command_args(tokens, "-i")
    output_file = parse_command_args(tokens, "-o")

    if not input_files:
        print("Missing input file(s). Use -i <file(s)>")
        return
    if not output_file:
        print("Missing output file. Use -o <file>")
        return

    # Ensure list
    if isinstance(input_files, str):
        input_files = [input_files]

    # Load input images as PIL
    from PIL import Image
    input_pils = [Image.open(os.path.join(os.getcwd(), f)) for f in input_files]

    maxval = getattr(input_pils[0], "maxval", 255)

    # Handle each operation
    if op == "add":
        result = add_images(input_pils[0], input_pils[1], maxval)
    elif op == "sub":
        result = subtract_images(input_pils[0], input_pils[1], maxval)
    elif op == "mul":
        result = multiply_images(input_pils[0], input_pils[1], maxval)
    elif op == "inv":
        result = create_negative_image(input_pils[0], maxval)
    elif op == "log":
        c_val = float(parse_command_args(tokens, "-c") or 1.0)
        base_val = float(parse_command_args(tokens, "-b") or 10.0)
        result = log_transform(input_pils[0], maxval, c=c_val, base=base_val)
    elif op == "pow":
        c_val = float(parse_command_args(tokens, "-c") or 1.0)
        gamma_val = float(parse_command_args(tokens, "-gamma") or 1.0)
        result = power_transform(input_pils[0], maxval, gamma=gamma_val, c=c_val)
    else:
        print(f"Unknown operation: {op}")
        return

    #save result
    result.save(os.path.join(os.getcwd(), output_file))
    print(f"{op.upper()} operation complete. Saved as {output_file}")
