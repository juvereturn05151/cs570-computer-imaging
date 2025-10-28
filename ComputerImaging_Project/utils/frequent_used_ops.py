"""
File Name:    frequent_used_ops.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

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
        print("Error: Kernel size must be odd")
        return
    if kernel_size < 3:
        print("Error: Kernel size must be at least 3")
        return
    if sigma <= 0:
        print("Error: Sigma must be positive")
        return
    if k <= 0:
        print("Error: Scaling factor k must be positive")
        return

    if errors:
        print("Validation errors:\n- " + "\n- ".join(errors))
        return False
    return True