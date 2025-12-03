"""
File Name:    fast_fourier_transform_operations.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import numpy as np
from PIL import Image
from image_data import update_output_image

def fft(input_label, spectrum_label, output_label):
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

def fft_compression(input_label, spectrum_label, output_label, low_cut_var, high_cut_var):
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




