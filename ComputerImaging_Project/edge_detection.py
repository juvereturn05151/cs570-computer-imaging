"""
File Name:    edge_detection.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import numpy as np
from PIL import Image


def sobel_edge_detection(input_image, scaling_factor=1.0):
    if not isinstance(input_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    # Convert to grayscale if needed
    if input_image.mode != 'L':
        input_image = input_image.convert('L')

    # Convert to numpy array
    img_array = np.array(input_image, dtype=np.float32)
    height, width = img_array.shape

    # Initialize output array
    output_array = np.zeros((height, width), dtype=np.float32)

    # Define Sobel kernels with scaling factor
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]]) * scaling_factor

    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]]) * scaling_factor

    # Apply Sobel filters with zero padding
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            # Extract 3x3 region
            region = img_array[i - 1:i + 2, j - 1:j + 2]

            # Apply horizontal Sobel (Gx)
            gx = np.sum(region * sobel_x)

            # Apply vertical Sobel (Gy)
            gy = np.sum(region * sobel_y)

            # Combine the results (approximate magnitude)
            magnitude = np.sqrt(gx ** 2 + gy ** 2)
            output_array[i, j] = magnitude

    # Normalize to 0-255 range
    output_array = np.clip(output_array, 0, 255)

    # Convert back to PIL Image
    return Image.fromarray(output_array.astype(np.uint8))