from PIL import Image
import numpy as np

def apply_negative_image(input_image, maxval):
    image_data = input_image.load()
    width, height = input_image.size
    negative_image = Image.new(input_image.mode, (width, height))
    neg_data = negative_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = image_data[x, y]
            neg_data[x, y] = (maxval - r, maxval - g, maxval - b)
    return negative_image


def apply_images_addition(input_image1, input_image2, maxval):
    #we need to convert to 16 bits to avoid overflow (e.g., 200 + 100 = 44)
    arr1 = np.array(input_image1, dtype=np.int16)
    arr2 = np.array(input_image2, dtype=np.int16)

    result = np.clip(arr1 + arr2, 0, maxval).astype(np.uint8)
    return Image.fromarray(result)


def apply_images_subtraction(input_image1, input_image2, maxval):
    arr1 = np.array(input_image1, dtype=np.int16)
    arr2 = np.array(input_image2, dtype=np.int16)

    result = np.clip(arr1 - arr2, 0, maxval).astype(np.uint8)
    return Image.fromarray(result)

def apply_images_multiplication(input_image1, input_image2, maxval):
    #normalize image to range [0,1] to avoid overflow
    arr1 = np.array(input_image1, dtype=np.float32) / maxval
    arr2 = np.array(input_image2, dtype=np.float32) / maxval

    result = np.clip((arr1 * arr2) * maxval, 0, maxval).astype(np.uint8)
    return Image.fromarray(result)

def apply_log_transform(input_image, maxval, c=1.0):
    arr = np.array(input_image, dtype=np.float32) / maxval
    log_arr = c * np.log(1.0 + arr)

    result = np.clip(log_arr * maxval, 0, maxval).astype(np.uint8)
    return Image.fromarray(result)


def apply_power_transform(input_image, maxval, gamma=1.0, c=1.0):
    arr = np.array(input_image, dtype=np.float32) / maxval

    power_arr = c * np.power(arr, gamma)

    #normalize the value to make sure that it's in the range from 0-1
    max_output = np.max(power_arr)
    if max_output > 0:
        power_arr = (power_arr / max_output) * maxval
    else:
        power_arr = power_arr * maxval

    result = np.clip(power_arr, 0, maxval).astype(np.uint8)
    return Image.fromarray(result)