from PIL import Image
from connected_component_labeling import connected_component_label, connected_component_label_m
from resize_operations import nearest_neighbor_resize, billinear_interpolation_resize
from arithmetic_operations import apply_negative_image, apply_images_addition, apply_images_subtraction, apply_images_multiplication, apply_log_transform, apply_power_transform

def create_negative_image(inputImage, maxval):
    if not isinstance(inputImage, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    return apply_negative_image(inputImage, maxval)

def add_images(inputImage, inputImage2, maxval):
    if inputImage.size != inputImage2.size:
        inputImage2 = inputImage2.resize(inputImage.size)

    return apply_images_addition(inputImage, inputImage2, maxval)

def subtract_images(inputImage1, inputImage2, maxval):
    if inputImage1.size != inputImage2.size:
        inputImage2 = inputImage2.resize(inputImage1.size)

    return apply_images_subtraction(inputImage1, inputImage2, maxval)

def multiply_images(inputImage1, inputImage2, maxval):
    if inputImage1.size != inputImage2.size:
        inputImage2 = inputImage2.resize(inputImage1.size)

    return apply_images_multiplication(inputImage1, inputImage2, maxval)

def log_transform(inputImage, maxval, c=1.0):
    return apply_log_transform(inputImage, maxval, c=1.0)


def power_transform(inputImage, maxval,gamma=1.0, c=1.0):
    return apply_power_transform(inputImage, maxval,gamma, c)

def connected_component_labeling(inputLabel, connectivity=4):
    return connected_component_label(inputLabel, connectivity)

def connected_component_labeling_m(inputLabel):
    return connected_component_label_m(inputLabel)

def nearest_neighbor(pil_image, new_width, new_height):
    return nearest_neighbor_resize(pil_image, new_width, new_height)

#compute each new pixel as a weighted average of 4 nearest pixels in the original image.
def billinear_interpolation(pil_image, new_width, new_height):
    return billinear_interpolation_resize(pil_image, new_width, new_height)