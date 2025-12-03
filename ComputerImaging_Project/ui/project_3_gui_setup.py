"""
File Name:    project_3_gui_setup.py
Author(s):    Ju-ve Chankasemporn
Description:  GUI setup for CS370 Project 3 – Fourier Transform
"""

import tkinter as tk
from tkinter import ttk

from PIL import Image
import numpy as np
from image_data import update_output_image
from images_ops.image_ops import (apply_direct_dft, apply_separable_dft, apply_fft, apply_fft_compression, apply_pseudocolor_spectrum)

def init_project_3_gui(project_3_frame, input_label, spectrum_label, output_label):
    # direct fourier transform
    tk.Button(
        project_3_frame,
        text="Direct 2D DFT (Part A(a))",
        command=lambda: apply_direct_dft(input_label, spectrum_label, output_label),
        bg="lightblue"
    ).pack(fill="x", pady=3)

    # separable DFT
    tk.Button(
        project_3_frame,
        text="Separable 2D DFT (Part A(b))",
        command=lambda: apply_separable_dft(input_label, spectrum_label, output_label),
        bg="lightgreen"
    ).pack(fill="x", pady=3)

    # fast fourier transform
    tk.Button(
        project_3_frame,
        text="Fast Fourier Transform (Part B)",
        command=lambda: apply_fft(input_label, spectrum_label, output_label),
        bg="khaki"
    ).pack(fill="x", pady=3)

    # pseudo color spectrum
    tk.Label(project_3_frame, text="Pseudo-color Bins:", font=("Arial", 9)).pack(anchor="w")

    bins_var = tk.StringVar(value="8")
    ttk.Entry(project_3_frame, textvariable=bins_var, width=8).pack(anchor="w", pady=2)

    tk.Button(
        project_3_frame,
        text="Display Pseudo-color Spectrum (Part C)",
        command=lambda: apply_pseudocolor_spectrum(spectrum_label, bins_var),
        bg="orange"
    ).pack(fill="x", pady=3)

    # compressing using fft
    tk.Label(project_3_frame, text="Compression Frequency Range:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 3))

    # lower freq
    tk.Label(project_3_frame, text="Low Cutoff:").pack(anchor="w")
    low_cut_var = tk.StringVar(value="0")
    ttk.Entry(project_3_frame, textvariable=low_cut_var, width=10).pack(anchor="w")

    # upper freq
    tk.Label(project_3_frame, text="High Cutoff:").pack(anchor="w", pady=(5, 0))
    high_cut_var = tk.StringVar(value="100000")
    ttk.Entry(project_3_frame, textvariable=high_cut_var, width=10).pack(anchor="w")

    tk.Button(
        project_3_frame,
        text="Apply Compression (Part E)",
        command=lambda: apply_fft_compression(input_label, spectrum_label, output_label, low_cut_var, high_cut_var),
        bg="lightcoral"
    ).pack(fill="x", pady=5)




