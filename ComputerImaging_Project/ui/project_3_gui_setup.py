"""
File Name:    project_3_gui_setup.py
Author(s):    Ju-ve Chankasemporn
Description:  GUI setup for CS370 Project 3 – Fourier Transform
"""

import tkinter as tk
from tkinter import ttk

from image_data import update_output_image


# ------------------------------------------------------------
# GUI Initialization for Project 3
# ------------------------------------------------------------

def init_project_3_gui(project_3_frame, input_label, spectrum_label, output_label):
    """
    Initialize the UI elements for Project 3 (Fourier Transform).

    Panels:
        - input_label: Original image
        - spectrum_label: Fourier spectrum
        - output_label: Reconstructed image
    """

    # ------------------------------------------------------------
    # Part A(a): Direct 2D DFT
    # ------------------------------------------------------------
    tk.Button(
        project_3_frame,
        text="Direct 2D DFT (Part A(a))",
        command=lambda: run_direct_dft(input_label, spectrum_label, output_label),
        bg="lightblue"
    ).pack(fill="x", pady=3)

    # ------------------------------------------------------------
    # Part A(b): Separable 2D DFT
    # ------------------------------------------------------------
    tk.Button(
        project_3_frame,
        text="Separable 2D DFT (Part A(b))",
        command=lambda: run_separable_dft(input_label, spectrum_label, output_label),
        bg="lightgreen"
    ).pack(fill="x", pady=3)

    # ------------------------------------------------------------
    # Part B: Fast Fourier Transform (FFT)
    # ------------------------------------------------------------
    tk.Button(
        project_3_frame,
        text="Fast Fourier Transform (Part B)",
        command=lambda: run_fft(input_label, spectrum_label, output_label),
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
        command=lambda: run_fft_compression(input_label, spectrum_label, output_label, low_cut_var, high_cut_var),
        bg="lightcoral"
    ).pack(fill="x", pady=5)

    # Return variables if needed later
    return bins_var, low_cut_var, high_cut_var


# ------------------------------------------------------------
# Placeholder Functions (to be implemented later)
# ------------------------------------------------------------

def run_direct_dft(input_label, spectrum_label, output_label):
    print("TODO: Implement Direct 2D DFT")
    # When implemented:
    #   spectrum_image = ...
    #   reconstructed = ...
    # update_output_image(spectrum_label, spectrum_image)
    # update_output_image(output_label, reconstructed)


def run_separable_dft(input_label, spectrum_label, output_label):
    print("TODO: Implement Separable 2D DFT")


def run_fft(input_label, spectrum_label, output_label):
    print("TODO: Implement FFT (DIT)")


def run_pseudocolor_spectrum(spectrum_label, bins_var):
    print(f"TODO: Implement Pseudo-color Spectrum with {bins_var.get()} bins")


def run_fft_compression(input_label, spectrum_label, output_label, low_cut_var, high_cut_var):
    print(f"TODO: Implement Compression: low={low_cut_var.get()}, high={high_cut_var.get()}")
