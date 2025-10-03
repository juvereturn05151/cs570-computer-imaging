from PIL import Image
import numpy as np

def apply_negative_image(inputImage, maxval):
    image_data = inputImage.load()
    width, height = inputImage.size
    negative_image = Image.new(inputImage.mode, (width, height))
    neg_data = negative_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = image_data[x, y]
            neg_data[x, y] = (maxval - r, maxval - g, maxval - b)
    return negative_image


def apply_images_addition(inputImage, inputImage2, maxval):
    arr1 = np.array(inputImage, dtype=np.int16)
    arr2 = np.array(inputImage2, dtype=np.int16)

    result = np.clip(arr1 + arr2, 0, maxval).astype(np.uint8)

    return Image.fromarray(result)


def apply_images_subtraction(inputImage1, inputImage2, maxval):
    arr1 = np.array(inputImage1, dtype=np.int16)
    arr2 = np.array(inputImage2, dtype=np.int16)

    result = np.clip(arr1 - arr2, 0, maxval).astype(np.uint8)

    return Image.fromarray(result)


def apply_images_multiplication(inputImage1, inputImage2, maxval):
    arr1 = np.array(inputImage1, dtype=np.float32) / maxval
    arr2 = np.array(inputImage2, dtype=np.float32) / maxval

    result = np.clip((arr1 * arr2) * maxval, 0, maxval).astype(np.uint8)

    return Image.fromarray(result)


def apply_log_transform(inputImage, maxval, c=1.0):
    arr = np.array(inputImage, dtype=np.float32) / maxval

    log_arr = c * np.log(1.0 + arr)

    result = np.clip(log_arr * maxval, 0, maxval).astype(np.uint8)

    return Image.fromarray(result)


def apply_power_transform(inputImage, maxval,gamma=1.0, c=1.0):
    arr = np.array(inputImage, dtype=np.float32) / maxval

    power_arr = c * np.power(arr, gamma)

    max_output = np.max(power_arr)
    if max_output > 0:
        power_arr = (power_arr / max_output) * maxval
    else:
        power_arr = power_arr * maxval

    result = np.clip(power_arr, 0, maxval).astype(np.uint8)
    return Image.fromarray(result)