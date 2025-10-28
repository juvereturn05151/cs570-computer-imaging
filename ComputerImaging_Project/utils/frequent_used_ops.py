"""
File Name:    frequent_used_ops.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

from PIL import Image

def validate_gaussian_smoothing_input_variables(kernel_size, sigma):
    """Validate parameters and collect all errors before returning."""
    errors = []

    if kernel_size % 2 == 0:
        errors.append("Kernel size must be odd")
    if kernel_size < 3:
        errors.append("Kernel size must be at least 3")
    if sigma <= 0:
        errors.append("Sigma must be positive")

    if errors:
        print("Validation errors:\n- " + "\n- ".join(errors))
        return False
    return True

def validate_unsharp_masking_input_variables(kernel_size, sigma, k):
    """Validate parameters and collect all errors before returning."""
    errors = []

    if kernel_size % 2 == 0:
        errors.append("Error: Kernel size must be odd")
    if kernel_size < 3:
        errors.append("Error: Kernel size must be at least 3")
    if sigma <= 0:
        errors.append("Error: Sigma must be positive")
    if k <= 0:
        errors.append("Error: Scaling factor k must be positive")

    if errors:
        print("Validation errors:\n- " + "\n- ".join(errors))
        return False
    return True

def get_max_value(input_label):
    """Return the maximum value from the label."""
    return getattr(input_label, "max_val", 255)

def validate_image(input_image, param_name="input_image"):
    """Check if image is valid."""
    if not isinstance(input_image, Image.Image):
        raise ValueError(f"{param_name} must be a PIL Image object")

def resize_image(input_image1, input_image2):
    """Resize image 2 to the size of image 1"""
    if input_image1.size != input_image2.size:
        input_image2 = input_image2.resize(input_image1.size)

    return  input_image2