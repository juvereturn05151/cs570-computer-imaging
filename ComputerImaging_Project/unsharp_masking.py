"""
File Name:    unsharp_masking.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import numpy as np
from PIL import Image

from smoothing_filter import gaussian_smoothing

def unsharp_masking(input_image, kernel_size, sigma, k, padding_mode='reflect'):
    if not isinstance(input_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    # Apply Gaussian blur to create the blurred version
    blurred_image = gaussian_smoothing(input_image, kernel_size, sigma, padding_mode)

    # Convert images to numpy arrays for processing
    original_array = np.array(input_image, dtype=np.float32)
    blurred_array = np.array(blurred_image, dtype=np.float32)

    # Calculate the mask: original - blurred
    mask = original_array - blurred_array

    # Apply unsharp masking: original + k * mask
    sharpened_array = original_array + k * mask

    # Clip values to valid range [0, 255]
    sharpened_array = np.clip(sharpened_array, 0, 255)

    # Convert back to PIL Image
    return Image.fromarray(sharpened_array.astype(np.uint8))