"""
File Name:    arithmetic_operations.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

from PIL import Image
import numpy as np

def apply_negative_image(input_image, max_val):
    """Black to white image or the other way around operation"""
    image_data = input_image.load()
    width, height = input_image.size
    negative_image = Image.new(input_image.mode, (width, height))
    neg_data = negative_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = image_data[x, y]
            neg_data[x, y] = (max_val - r, max_val - g, max_val - b)
    return negative_image


def apply_images_addition(input_image1, input_image2, max_val):
    """Add two images to an image."""
    # we need to convert to 16 bits to avoid overflow (e.g., 200 + 100 = 44)
    arr1 = np.array(input_image1, dtype=np.int16)
    arr2 = np.array(input_image2, dtype=np.int16)

    result = np.clip(arr1 + arr2, 0, max_val).astype(np.uint8)
    return Image.fromarray(result)


def apply_images_subtraction(input_image1, input_image2, max_val):
    """Subtract two images to an image."""
    arr1 = np.array(input_image1, dtype=np.int16)
    arr2 = np.array(input_image2, dtype=np.int16)

    result = np.clip(arr1 - arr2, 0, max_val).astype(np.uint8)
    return Image.fromarray(result)

def apply_images_multiplication(input_image1, input_image2, max_val):
    """Multiply two images to an image.
    This operation is mainly use to find the overlap between two images."""
    # normalize image to range [0,1] to avoid overflow
    arr1 = np.array(input_image1, dtype=np.float32) / max_val
    arr2 = np.array(input_image2, dtype=np.float32) / max_val

    result = np.clip((arr1 * arr2) * max_val, 0, max_val).astype(np.uint8)
    return Image.fromarray(result)

def apply_log_transform(input_image, max_val, c=1.0):
    """Use log transform to either darken or whiten the image.
       if 0 < c < 1, darken image
       if c > 1, whiten image"""
    arr = np.array(input_image, dtype=np.float32) / max_val
    log_arr = c * np.log(1.0 + arr)

    result = np.clip(log_arr * max_val, 0, max_val).astype(np.uint8)
    return Image.fromarray(result)

def apply_power_transform(input_image, max_val, gamma=1.0, c=1.0):
    """Use power transform to either darken or whiten the image.
           if signa > 1, darken image
           if sigma < 1, whiten image"""
    arr = np.array(input_image, dtype=np.float32) / max_val
    power_arr = c * np.power(arr, gamma)

    #normalize the value to make sure that it's in the range from 0-1
    max_output = np.max(power_arr)
    if max_output > 0:
        power_arr = (power_arr / max_output) * max_val
    else:
        power_arr = power_arr * max_val

    result = np.clip(power_arr, 0, max_val).astype(np.uint8)
    return Image.fromarray(result)