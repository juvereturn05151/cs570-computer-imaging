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
from images_ops.image_ops import (apply_direct_dft, apply_separable_dft, apply_fft, apply_fft_compression)

def init_project_3_gui(project_3_frame, input_label, spectrum_label, output_label):
    # direct force DFT
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

    # ------------------------------------------------------------
    # Part B: Fast Fourier Transform (FFT)
    # ------------------------------------------------------------
    tk.Button(
        project_3_frame,
        text="Fast Fourier Transform (Part B)",
        command=lambda: apply_fft(input_label, spectrum_label, output_label),
        bg="khaki"
    ).pack(fill="x", pady=3)

    # ------------------------------------------------------------
    # Part C: Pseudo-color Spectrum (Intensity Slicing)
    # ------------------------------------------------------------
    tk.Label(project_3_frame, text="Pseudo-color Bins:", font=("Arial", 9)).pack(anchor="w")

    bins_var = tk.StringVar(value="8")
    ttk.Entry(project_3_frame, textvariable=bins_var, width=8).pack(anchor="w", pady=2)

    tk.Button(
        project_3_frame,
        text="Display Pseudo-color Spectrum (Part C)",
        command=lambda: run_pseudocolor_spectrum(spectrum_label, bins_var),
        bg="orange"
    ).pack(fill="x", pady=3)

    # ------------------------------------------------------------
    # Part E: Simple Compression (Optional Extra Credit)
    # ------------------------------------------------------------
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

def run_pseudocolor_spectrum(spectrum_label, bins_var):
    print(f"TODO: Implement Pseudo-color Spectrum with {bins_var.get()} bins")

    try:
        bins = int(bins_var.get())
        if bins < 2:
            bins = 2
    except ValueError:
        bins = 8  # default

        # ------------------------------------------
        # 2. Get CURRENT spectrum image (must be grayscale)
        # ------------------------------------------
    gray_pil = spectrum_label.pil_image.convert("L")
    gray = np.array(gray_pil, dtype=np.uint8)

    H, W = gray.shape

    # ------------------------------------------
    # 3. Create bin edges (0..255)
    # ------------------------------------------
    bin_edges = np.linspace(0, 255, bins + 1)

    # ------------------------------------------
    # 4. Choose a color map (per bin)
    # ------------------------------------------
    colormap = [
        (255, 0, 0),  # red
        (255, 165, 0),  # orange
        (255, 255, 0),  # yellow
        (0, 255, 0),  # green
        (0, 255, 255),  # cyan
        (0, 0, 255),  # blue
        (128, 0, 255),  # violet
        (255, 0, 255),  # magenta
    ]

    # If more bins than colors → extend by repeating last color
    while len(colormap) < bins:
        colormap.append(colormap[-1])

    # ------------------------------------------
    # 5. Create output color image
    # ------------------------------------------
    color_image = np.zeros((H, W, 3), dtype=np.uint8)

    for i in range(bins):
        low = bin_edges[i]
        high = bin_edges[i + 1]

        mask = (gray >= low) & (gray < high)
        color_image[mask] = colormap[i]

    # ------------------------------------------
    # 6. Update GUI
    # ------------------------------------------
    color_pil = Image.fromarray(color_image)
    update_output_image(spectrum_label, color_pil)

    print(f"Pseudo-color spectrum displayed using {bins} bins.")


