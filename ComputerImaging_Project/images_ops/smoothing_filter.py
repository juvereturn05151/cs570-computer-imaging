"""
File Name:    smooothing_filter.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import numpy as np
from PIL import Image

def create_gaussian_kernel(kernel_size, sigma):
    """Create the Gaussian kernel"""
    kernel = np.zeros((kernel_size, kernel_size))
    center = kernel_size // 2
    constant = 1 / (2 * np.pi * sigma ** 2)

    for i in range(kernel_size):
        for j in range(kernel_size):
            x = i - center
            y = j - center
            kernel[i, j] = constant * np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))

    # normalize
    kernel /= np.sum(kernel)

    return kernel


def apply_filter_2d(image, kernel, padding_mode='reflect'):
    """Apply padding based on the chosen mode"""

    # image:2D numpy array
    # kernel: 2D filter kernel
    kernel_size = kernel.shape[0]
    pad_size = kernel_size // 2
    output = np.zeros_like(image)

    if padding_mode == 'reflect':
        padded_image = np.pad(image, pad_size, mode='reflect')
    elif padding_mode == 'constant':
        padded_image = np.pad(image, pad_size, mode='constant', constant_values=0)
    elif padding_mode == 'nearest':
        padded_image = np.pad(image, pad_size, mode='edge')
    else:
        raise ValueError("Unsupported padding mode")

    # perform convolution
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded_image[i:i + kernel_size, j:j + kernel_size]
            rotated_kernel = np.rot90(kernel, 2)
            output[i, j] = np.sum(region * rotated_kernel)

    return output


def gaussian_smoothing(input_image, kernel_size, sigma, padding_mode='reflect', max_val=255):
    """Perform gaussian smoothing on the input image,
    This should make an image blurrier"""

    if kernel_size % 2 == 0:
        raise ValueError("Kernel size must be odd")

    if input_image.mode == 'L':
        img_array = np.array(input_image, dtype=np.float32)
        is_grayscale = True
    else:
        img_array = np.array(input_image.convert('RGB'), dtype=np.float32)
        is_grayscale = False

    kernel = create_gaussian_kernel(kernel_size, sigma)

    # apply filter to each channel
    if is_grayscale:
        smoothed_array = apply_filter_2d(img_array, kernel, padding_mode)
    else:
        smoothed_channels = []
        for channel in range(3):
            smoothed_channel = apply_filter_2d(img_array[:, :, channel], kernel, padding_mode)
            smoothed_channels.append(smoothed_channel)
        smoothed_array = np.stack(smoothed_channels, axis=2)

    # convert back to uint8 and PIL Image
    smoothed_array = np.clip(smoothed_array, 0, max_val).astype(np.uint8)

    if is_grayscale:
        return Image.fromarray(smoothed_array, mode='L')
    else:
        return Image.fromarray(smoothed_array, mode='RGB')