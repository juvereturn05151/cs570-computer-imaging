"""
File Name:    unsharp_masking.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import numpy as np
from PIL import Image

from images_ops.smoothing_filter import gaussian_smoothing

def unsharp_masking(input_image, kernel_size, sigma, k, padding_mode='reflect'):
    """Apply unsharp masking: to make the image sharper
    by creating a mask from blurred image,
    then add it back to the original image"""
    if not isinstance(input_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    # apply Gaussian blur to create the blurred version
    blurred_image = gaussian_smoothing(input_image, kernel_size, sigma, padding_mode)

    # convert images to numpy arrays for processing
    original_array = np.array(input_image, dtype=np.float32)
    blurred_array = np.array(blurred_image, dtype=np.float32)

    # calculate the mask: original - blurred
    mask = original_array - blurred_array

    # apply unsharp masking: original + k * mask
    sharpened_array = original_array + k * mask

    # clip values to valid range [0, 255]
    sharpened_array = np.clip(sharpened_array, 0, 255)

    # convert back to PIL Image
    return Image.fromarray(sharpened_array.astype(np.uint8))