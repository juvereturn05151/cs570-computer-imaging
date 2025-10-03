from PIL import Image
from connected_component_labeling import connected_component_label, connected_component_label_m
from resize_operations import nearest_neighbor_resize, billinear_interpolation_resize
from arithmetic_operations import apply_negative_image, apply_images_addition, apply_images_subtraction, apply_images_multiplication, apply_log_transform, apply_power_transform

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

    return apply_log_transform(input_image, maxval, c=1.0)


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