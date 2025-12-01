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


def run_direct_dft(input_label, spectrum_label, output_label):
    print("Running Direct 2D DFT (Part A(a))... this may take long.")

    f = np.array(input_label.pil_image.convert("L"), dtype=float)
    M, N = f.shape

    # 2D DFT
    F = np.zeros((M, N), dtype=complex)
    for u in range(M):
        for v in range(N):
            s = 0
            for x in range(M):
                for y in range(N):
                    angle = -2j * np.pi * ((u*x)/M + (v*y)/N)
                    s += f[x, y] * np.exp(angle)
            F[u, v] = s

    # Spectrum
    spectrum = np.log(np.abs(F) + 1)
    spectrum = (spectrum / spectrum.max() * 255).astype(np.uint8)
    spectrum_image = Image.fromarray(spectrum)

    # Inverse 2D DFT
    reconstructed = np.zeros((M, N), dtype=complex)
    for x in range(M):
        for y in range(N):
            s = 0
            for u in range(M):
                for v in range(N):
                    angle = 2j * np.pi * ((u*x)/M + (v*y)/N)
                    s += F[u, v] * np.exp(angle)
            reconstructed[x, y] = s / (M * N)

    reconstructed = np.clip(np.abs(reconstructed), 0, 255).astype(np.uint8)
    reconstructed_image = Image.fromarray(reconstructed)

    update_output_image(spectrum_label, spectrum_image)
    update_output_image(output_label, reconstructed_image)


# ============================================================
# PART A(b) — Separable 2D DFT (1D row → 1D column)
# ============================================================

def dft_1d(x):
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        s = 0
        for n in range(N):
            s += x[n] * np.exp(-2j * np.pi * k * n / N)
        X[k] = s
    return X


def idft_1d(X):
    N = len(X)
    x = np.zeros(N, dtype=complex)
    for n in range(N):
        s = 0
        for k in range(N):
            s += X[k] * np.exp(2j * np.pi * k * n / N)
        x[n] = s / N
    return x


def run_separable_dft(input_label, spectrum_label, output_label):
    print("Running Separable 2D DFT (Part A(b))...")

    f = np.array(input_label.pil_image.convert("L"), dtype=float)
    M, N = f.shape

    # Pass 1 — rows
    row_dft = np.zeros((M, N), dtype=complex)
    for i in range(M):
        row_dft[i, :] = dft_1d(f[i, :])

    # Pass 2 — columns
    F = np.zeros((M, N), dtype=complex)
    for j in range(N):
        F[:, j] = dft_1d(row_dft[:, j])

    spectrum = np.log(np.abs(F) + 1)
    spectrum = (spectrum / spectrum.max() * 255).astype(np.uint8)
    spectrum_image = Image.fromarray(spectrum)

    # Inverse 2D Separable DFT
    col_idft = np.zeros((M, N), dtype=complex)
    for j in range(N):
        col_idft[:, j] = idft_1d(F[:, j])

    reconstructed = np.zeros((M, N), dtype=complex)
    for i in range(M):
        reconstructed[i, :] = idft_1d(col_idft[i, :])

    reconstructed = np.clip(np.abs(reconstructed), 0, 255).astype(np.uint8)
    reconstructed_image = Image.fromarray(reconstructed)

    update_output_image(spectrum_label, spectrum_image)
    update_output_image(output_label, reconstructed_image)



# ============================================================
# PART B — Fast Fourier Transform (DIT + Bit Reversal)
# ============================================================

def bit_reverse_indices(N):
    bits = N.bit_length() - 1
    rev = np.zeros(N, dtype=int)
    for i in range(N):
        b = f'{i:0{bits}b}'
        rev[i] = int(b[::-1], 2)
    return rev


def fft_1d_inplace(x):
    """Iterative Decimation-in-Time FFT (In-place)."""
    N = len(x)
    rev = bit_reverse_indices(N)
    x[:] = x[rev]  # bit-reversal reorder

    half = 1
    while half < N:
        step = half * 2
        wm = np.exp(-2j * np.pi / step)
        for k in range(0, N, step):
            w = 1
            for n in range(half):
                i = k + n
                j = i + half
                t = w * x[j]
                x[j] = x[i] - t
                x[i] = x[i] + t
                w *= wm
        half = step


def ifft_1d_inplace(x):
    """Inverse FFT using forward FFT code (conjugate trick)."""
    x[:] = np.conjugate(x)
    fft_1d_inplace(x)
    x[:] = np.conjugate(x)
    x[:] = x / len(x)


def fftshift_2d(F):
    M, N = F.shape
    F = np.roll(F, M//2, axis=0)
    F = np.roll(F, N//2, axis=1)
    return F


def pad_to_power_of_2(img):
    M, N = img.shape
    M2 = 1 << (M - 1).bit_length()
    N2 = 1 << (N - 1).bit_length()
    result = np.zeros((M2, N2), dtype=float)
    result[:M, :N] = img
    return result, M, N  # keep original size


def run_fft(input_label, spectrum_label, output_label):
    print("Running FFT (Part B) – In-place, bit reversal, iterative.")

    # Convert + Pad
    f = np.array(input_label.pil_image.convert("L"), dtype=float)
    padded, M0, N0 = pad_to_power_of_2(f)
    M, N = padded.shape

    F = padded.astype(complex)

    # 1D FFT on rows
    for i in range(M):
        fft_1d_inplace(F[i, :])

    # 1D FFT on columns
    for j in range(N):
        fft_1d_inplace(F[:, j])

    # FFT shift for spectrum
    F_shift = fftshift_2d(F)

    # Spectrum
    spectrum = np.log(np.abs(F_shift) + 1)
    spectrum = (spectrum / spectrum.max() * 255).astype(np.uint8)
    spectrum_image = Image.fromarray(spectrum)

    # -------- Inverse FFT ----------
    G = F.copy()

    for j in range(N):
        ifft_1d_inplace(G[:, j])
    for i in range(M):
        ifft_1d_inplace(G[i, :])

    reconstructed = np.clip(np.abs(G[:M0, :N0]), 0, 255).astype(np.uint8)
    reconstructed_image = Image.fromarray(reconstructed)

    update_output_image(spectrum_label, spectrum_image)
    update_output_image(output_label, reconstructed_image)


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


def run_fft_compression(input_label, spectrum_label, output_label, low_cut_var, high_cut_var):
    print(f"TODO: Implement Compression: low={low_cut_var.get()}, high={high_cut_var.get()}")
    # ------------------------------------------
    # 1. Parse frequency cutoffs
    # ------------------------------------------
    try:
        low_cut = float(low_cut_var.get())
    except:
        low_cut = 0.0

    try:
        high_cut = float(high_cut_var.get())
    except:
        high_cut = 1e9  # very large max

    print(f"Applying compression: keep {low_cut} <= |F(u,v)| <= {high_cut}")

    # ------------------------------------------
    # 2. Convert image + pad to power-of-2
    # ------------------------------------------
    f = np.array(input_label.pil_image.convert("L"), dtype=float)
    padded, M0, N0 = pad_to_power_of_2(f)
    M, N = padded.shape

    # ------------------------------------------
    # 3. Compute forward FFT (same as run_fft)
    # ------------------------------------------
    F = padded.astype(complex)

    # FFT rows
    for i in range(M):
        fft_1d_inplace(F[i, :])

    # FFT columns
    for j in range(N):
        fft_1d_inplace(F[:, j])

    # (No fftshift here because shift is only for display)
    magnitude = np.abs(F)

    # ------------------------------------------
    # 4. Apply frequency compression
    # ------------------------------------------
    mask = (magnitude >= low_cut) & (magnitude <= high_cut)
    F_compressed = F * mask  # zero out unwanted frequencies

    # ------------------------------------------
    # 5. For display: build shifted spectrum image
    # ------------------------------------------
    F_shift = fftshift_2d(F_compressed)

    spectrum = np.log(np.abs(F_shift) + 1)
    spectrum = (spectrum / spectrum.max() * 255).astype(np.uint8)
    spectrum_image = Image.fromarray(spectrum)

    # ------------------------------------------
    # 6. Inverse FFT to reconstruct image
    # ------------------------------------------
    G = F_compressed.copy()

    # IFFT columns
    for j in range(N):
        ifft_1d_inplace(G[:, j])

    # IFFT rows
    for i in range(M):
        ifft_1d_inplace(G[i, :])

    reconstructed = np.clip(np.abs(G[:M0, :N0]), 0, 255).astype(np.uint8)
    reconstructed_image = Image.fromarray(reconstructed)

    # ------------------------------------------
    # 7. Update GUI with spectrum + compressed reconstruction
    # ------------------------------------------
    update_output_image(spectrum_label, spectrum_image)
    update_output_image(output_label, reconstructed_image)

    print("Compression applied and image reconstructed.")