"""
File Name:    direct_fourier_transform_operations.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import numpy as np
from PIL import Image
from image_data import update_output_image, create_spectrum_image

def direct_discrete_fourier_transform(input_label, spectrum_label, output_label):
    """Brute Force Version"""
    if input_label.pil_image.mode != 'L':
        input_label.pil_image = input_label.pil_image.convert('L')

    f = np.array(input_label.pil_image, dtype=float)
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

    # spectrum
    spectrum_image = create_spectrum_image(F)

    # inverse 2D DFT
    reconstructed = np.zeros((M, N), dtype=complex)
    for x in range(M):
        for y in range(N):
            s = 0
            for u in range(M):
                for v in range(N):
                    angle = 2j * np.pi * ((u*x)/M + (v*y)/N)
                    s += F[u, v] * np.exp(angle)
            reconstructed[x, y] = s / (M * N)

    reconstructed_image = create_spectrum_image(reconstructed)

    update_output_image(spectrum_label, spectrum_image)
    update_output_image(output_label, reconstructed_image)

def separable_discrete_fourier_transform(input_label, spectrum_label, output_label):
    """A Faster version of direct_discrete_fourier_transform"""
    if input_label.pil_image.mode != 'L':
        input_label.pil_image = input_label.pil_image.convert('L')

    f = np.array(input_label.pil_image, dtype=float)
    M, N = f.shape

    #pass 1 — row
    row_dft = np.zeros((M, N), dtype=complex)
    for i in range(M):
        row_dft[i, :] = discrete_fourier_transform_1d(f[i, :])

    #pass 2 — column
    F = np.zeros((M, N), dtype=complex)
    for j in range(N):
        F[:, j] = discrete_fourier_transform_1d(row_dft[:, j])

    spectrum = np.log(np.abs(F) + 1)
    spectrum = (spectrum / spectrum.max() * 255).astype(np.uint8)
    spectrum_image = Image.fromarray(spectrum)

    #inverse 2D Separable DFT
    col_idft = np.zeros((M, N), dtype=complex)
    for j in range(N):
        col_idft[:, j] = inverse_discrete_fourier_transform_1d(F[:, j])

    reconstructed = np.zeros((M, N), dtype=complex)
    for i in range(M):
        reconstructed[i, :] = inverse_discrete_fourier_transform_1d(col_idft[i, :])

    reconstructed_image = create_spectrum_image(reconstructed)

    update_output_image(spectrum_label, spectrum_image)
    update_output_image(output_label, reconstructed_image)

def discrete_fourier_transform_1d(x):
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        s = 0
        for n in range(N):
            s += x[n] * np.exp(-2j * np.pi * k * n / N)
        X[k] = s
    return X


def inverse_discrete_fourier_transform_1d(X):
    N = len(X)
    x = np.zeros(N, dtype=complex)
    for n in range(N):
        s = 0
        for k in range(N):
            s += X[k] * np.exp(2j * np.pi * k * n / N)
        x[n] = s / N
    return x