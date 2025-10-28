"""
File Name:    project_1_gui_setup.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import tkinter as tk
from tkinter import ttk

from images_ops.image_ops import (
    create_negative_image, add_images, subtract_images, multiply_images,
    log_transform, power_transform, connected_component_labeling,
    connected_component_labeling_m,
)
from image_data import update_output_image

def init_project_1_gui(ops_frame):
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

    return  c_var, gamma_var

def update_parameters(c_var, gamma_var):
    current_c = tk.DoubleVar(value=1.0)
    current_gamma = tk.DoubleVar(value=1.0)

    try:
        c_value = float(c_var.get())
        gamma_value = float(gamma_var.get())
        current_c.set(c_value)
        current_gamma.set(gamma_value)
        print(f"Parameters updated: c={c_value}, γ={gamma_value}")
    except ValueError:
        print("Invalid parameter values. Please enter numbers.")

    return  current_c, current_gamma

def setup_log_transform_panel(ops_frame, input_label, output_image_label, max_val, current_c):
    def execute_log_transform():
        try:
            c_value = current_c.get()
            result = log_transform(input_label.pil_image, max_val, c_value)
            update_output_image(output_image_label, result)
            print(f"Applied Log Transform with c={c_value}")
        except Exception as e:
            print(f"Error in Log Transform: {e}")

    tk.Button(ops_frame, text="Log Transform", command=execute_log_transform).pack(fill="x")

def setup_power_transform_panel(ops_frame, input_label, output_image_label, max_val, current_c, current_gamma):
    # power transform with parameters
    def execute_power_transform():
        try:
            c_value = current_c.get()
            gamma_value = current_gamma.get()
            result = power_transform(input_label.pil_image, max_val, gamma_value, c_value)
            update_output_image(output_image_label, result)
            print(f"Applied Power Transform with γ={gamma_value}, c={c_value}")
        except Exception as e:
            print(f"Error in Power Transform: {e}")

    tk.Button(ops_frame, text="Power Transform", command=execute_power_transform).pack(fill="x")

def setup_connected_component_labeling(ops_frame, input_label, output_image_label):
    connected_labeling_frame = tk.Frame(ops_frame)
    connected_labeling_frame.pack(fill="x", pady=(10, 0))
    tk.Label(connected_labeling_frame, text="Connected-Labeling:").pack(anchor="w")

    connected_labeling_frame = tk.Frame(connected_labeling_frame)
    connected_labeling_frame.pack(fill="x")
    tk.Button(connected_labeling_frame, text="4-Connected", command=lambda: update_output_image(output_image_label,connected_component_labeling(input_label,4))).pack(side=tk.LEFT, fill="x", expand=True, padx=2)
    tk.Button(connected_labeling_frame, text="8-Connected", command=lambda: update_output_image(output_image_label,connected_component_labeling(input_label,8))).pack(side=tk.LEFT, fill="x", expand=True, padx=2)
    tk.Button(connected_labeling_frame, text="M-Connected", command=lambda: update_output_image(output_image_label,connected_component_labeling_m(input_label))).pack(side=tk.LEFT, fill="x", expand=True, padx=2)
