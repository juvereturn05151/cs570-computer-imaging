"""
File Name:    direct_fourier_transform_operations.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import numpy as np
from PIL import Image
from image_data import update_output_image

def direct_dft(input_label, spectrum_label, output_label):
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

def separable_dft(input_label, spectrum_label, output_label):
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