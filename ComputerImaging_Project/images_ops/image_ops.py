import cv2
from PIL import Image

from images_ops.connected_component_labeling import connected_component_label, connected_component_label_m
from images_ops.resize_operations import nearest_neighbor_resize, billinear_interpolation_resize
from images_ops.arithmetic_operations import apply_negative_image, apply_images_addition, apply_images_subtraction, apply_images_multiplication, apply_log_transform, apply_power_transform
from images_ops.histogram_equalization import histogram_equalization, histogram_equalization_opencv
from images_ops.smoothing_filter import gaussian_smoothing
from images_ops.edge_detection import sobel_edge_detection
from images_ops.unsharp_masking import unsharp_masking

def create_negative_image(input_image, maxval):
    if not isinstance(input_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    return apply_negative_image(input_image, maxval)

def add_images(input_image1, input_image2, maxval):
    if not isinstance(input_image1, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    if not isinstance(input_image2, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    if input_image1.size != input_image2.size:
        input_image2 = input_image2.resize(input_image1.size)

    return apply_images_addition(input_image1, input_image2, maxval)

def subtract_images(input_image1, input_image2, maxval):
    if not isinstance(input_image1, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    if not isinstance(input_image2, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    if input_image1.size != input_image2.size:
        input_image2 = input_image2.resize(input_image1.size)

    return apply_images_subtraction(input_image1, input_image2, maxval)

def multiply_images(input_image1, input_image2, maxval):
    if not isinstance(input_image1, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    if not isinstance(input_image2, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    if input_image1.size != input_image2.size:
        input_image2 = input_image2.resize(input_image1.size)

    return apply_images_multiplication(input_image1, input_image2, maxval)

def log_transform(input_image, maxval, c=1.0):
    if not isinstance(input_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    return apply_log_transform(input_image, maxval, c)


def power_transform(input_image, maxval,gamma=1.0, c=1.0):
    if not isinstance(input_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    return apply_power_transform(input_image, maxval,gamma, c)

def connected_component_labeling(input_label, connectivity=4):
    return connected_component_label(input_label, connectivity)

def connected_component_labeling_m(input_label):
    return connected_component_label_m(input_label)

def nearest_neighbor(pil_image, new_width, new_height):
    return nearest_neighbor_resize(pil_image, new_width, new_height)

#compute each new pixel as a weighted average of 4 nearest pixels in the original image.
def billinear_interpolation(pil_image, new_width, new_height):
    return billinear_interpolation_resize(pil_image, new_width, new_height)

def apply_histogram_equalization(input_image, maxval=255):
    result, fig = histogram_equalization(input_image, maxval, plot_histogram=True)
    return result

def apply_histogram_equalization_opencv(input_image, maxval=255):
    result, fig = histogram_equalization_opencv(input_image, maxval, plot_histogram=True)
    return result

def apply_gaussian_smoothing(input_image, kernel_size, sigma, padding_mode='reflect'):
    return gaussian_smoothing(input_image, kernel_size, sigma, padding_mode)

def apply_edge_detection(input_image, scaling_factor):
    return sobel_edge_detection(input_image, scaling_factor)

def apply_unsharp_masking(input_image, kernel_size, sigma, k, padding_mode='reflect'):
    return unsharp_masking(input_image, kernel_size, sigma, k, padding_mode='reflect')