from PIL import Image, ImageTk, ImageOps
import math
import numpy as np

# receive Pil image, and return a PIL image
def create_negative_image(pil_image, maxval=255 ):
    # check if it is a pil_image
    if not isinstance(pil_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    image_data = pil_image.load()
    width, height = pil_image.size
    negative_image = Image.new(pil_image.mode, (width, height))
    neg_data = negative_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = image_data[x, y]
            neg_data[x, y] = (maxval - r, maxval - g, maxval - b)
    return negative_image


def add_images(pil_image1, pil_image2):
    """Add two images with saturation"""
    # Ensure same size
    if pil_image1.size != pil_image2.size:
        pil_image2 = pil_image2.resize(pil_image1.size)

    # Convert to numpy for efficient computation
    arr1 = np.array(pil_image1, dtype=np.int16)
    arr2 = np.array(pil_image2, dtype=np.int16)

    # Add with saturation
    result = np.clip(arr1 + arr2, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def subtract_images(pil_image1, pil_image2):
    """Subtract image2 from image1 with saturation"""
    if pil_image1.size != pil_image2.size:
        pil_image2 = pil_image2.resize(pil_image1.size)

    arr1 = np.array(pil_image1, dtype=np.int16)
    arr2 = np.array(pil_image2, dtype=np.int16)

    result = np.clip(arr1 - arr2, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def multiply_images(pil_image1, pil_image2):
    """Multiply two images (element-wise)"""
    if pil_image1.size != pil_image2.size:
        pil_image2 = pil_image2.resize(pil_image1.size)

    arr1 = np.array(pil_image1, dtype=np.float32) / 255.0
    arr2 = np.array(pil_image2, dtype=np.float32) / 255.0

    result = np.clip((arr1 * arr2) * 255, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def log_transform(pil_image, c=1.0):
    """Apply logarithmic transformation"""
    arr = np.array(pil_image, dtype=np.float32) / 255.0

    # Avoid log(0) by adding small epsilon
    log_arr = c * np.log(1.0 + arr)

    result = np.clip(log_arr * 255, 0, 255).astype(np.uint8)

    return Image.fromarray(result)


def connected_topology_4(pil_image):
    """4-connected topology edge detection"""
    if pil_image.mode != 'L':
        gray_image = pil_image.convert('L')
    else:
        gray_image = pil_image

    arr = np.array(gray_image, dtype=np.float32)

    # 4-connected Laplacian kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 4, -1],
                       [0, -1, 0]])

    # Manual convolution for 4-connected
    height, width = arr.shape
    result = np.zeros_like(arr)

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            neighborhood = arr[y - 1:y + 2, x - 1:x + 2]
            result[y, x] = np.sum(neighborhood * kernel)

    result = np.clip(np.abs(result), 0, 255).astype(np.uint8)
    return Image.fromarray(result)


def connected_topology_8(pil_image):
    """8-connected topology edge detection"""
    if pil_image.mode != 'L':
        gray_image = pil_image.convert('L')
    else:
        gray_image = pil_image

    arr = np.array(gray_image, dtype=np.float32)

    # 8-connected Laplacian kernel
    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])

    height, width = arr.shape
    result = np.zeros_like(arr)

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            neighborhood = arr[y - 1:y + 2, x - 1:x + 2]
            result[y, x] = np.sum(neighborhood * kernel)

    result = np.clip(np.abs(result), 0, 255).astype(np.uint8)
    return Image.fromarray(result)


def connected_topology_m(pil_image):
    """M-connected topology (mixed connectivity)"""
    if pil_image.mode != 'L':
        gray_image = pil_image.convert('L')
    else:
        gray_image = pil_image

    arr = np.array(gray_image, dtype=np.float32)

    # M-connected combines diagonal and direct neighbors with different weights
    kernel = np.array([[-0.7, -1, -0.7],
                       [-1, 6, -1],
                       [-0.7, -1, -0.7]])

    height, width = arr.shape
    result = np.zeros_like(arr)

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            neighborhood = arr[y - 1:y + 2, x - 1:x + 2]
            result[y, x] = np.sum(neighborhood * kernel)

    result = np.clip(np.abs(result), 0, 255).astype(np.uint8)
    return Image.fromarray(result)

def nearest_neighbor(pil_image, new_width, new_height):
    original_width, original_height = pil_image.size
    new_image = Image.new(pil_image.mode, (new_width, new_height))

    original_pixels = pil_image.load()
    new_pixels = new_image.load()

    x_ratio = original_width / new_width
    y_ratio = original_height / new_height

    for y in range(new_height):
        for x in range(new_width):
            orig_x = min(math.floor(x * x_ratio), original_width - 1)
            orig_y = min(math.floor(y * y_ratio), original_height - 1)

            new_pixels[x, y] = original_pixels[orig_x, orig_y]

    return new_image

def billinear_interpolation(pil_image, new_width, new_height):
    original_width, original_height = pil_image.size
    new_image = Image.new(pil_image.mode, (new_width, new_height))

    original_pixels = pil_image.load()
    new_pixels = new_image.load()

    x_ratio = (original_width - 1) / (new_width - 1) if new_width > 1 else 0
    y_ratio = (original_height - 1) / (new_height - 1) if new_height > 1 else 0

    for y in range(new_height):
        for x in range(new_width):
            # Original floating point coordinates
            orig_x = x * x_ratio
            orig_y = y * y_ratio

            x1 = math.floor(orig_x)
            y1 = math.floor(orig_y)
            x2 = min(x1 + 1, original_width - 1)
            y2 = min(y1 + 1, original_height - 1)

            # Fractional parts
            dx = orig_x - x1
            dy = orig_y - y1

            # Get pixel values
            Q11 = original_pixels[x1, y1]
            Q21 = original_pixels[x2, y1]
            Q12 = original_pixels[x1, y2]
            Q22 = original_pixels[x2, y2]

            # If image has multiple channels (like RGB), interpolate each channel
            if isinstance(Q11, tuple):
                interpolated_pixel = tuple(
                    round(
                        Q11[c]*(1-dx)*(1-dy) +
                        Q21[c]*dx*(1-dy) +
                        Q12[c]*(1-dx)*dy +
                        Q22[c]*dx*dy
                    )
                    for c in range(len(Q11))
                )
            else:  # Grayscale
                interpolated_pixel = round(
                    Q11*(1-dx)*(1-dy) +
                    Q21*dx*(1-dy) +
                    Q12*(1-dx)*dy +
                    Q22*dx*dy
                )

            new_pixels[x, y] = interpolated_pixel

    return new_image