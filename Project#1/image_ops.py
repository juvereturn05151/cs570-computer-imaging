from PIL import Image, ImageTk, ImageOps
import math
import numpy as np
from collections import deque

def create_negative_image(inputImage, maxval):
    # check if it is a pil_image
    if not isinstance(inputImage, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    image_data = inputImage.load()
    width, height = inputImage.size
    negative_image = Image.new(inputImage.mode, (width, height))
    neg_data = negative_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = image_data[x, y]
            neg_data[x, y] = (maxval - r, maxval - g, maxval - b)
    return negative_image


def add_images(inputImage, inputImage2, maxval):
    #ensure same size
    if inputImage.size != inputImage2.size:
        inputImage2 = inputImage2.resize(inputImage.size)

    # Convert image to numpy array
    arr1 = np.array(inputImage, dtype=np.int16)
    arr2 = np.array(inputImage2, dtype=np.int16)

    # Add them up, then convert back to 8-bit
    result = np.clip(arr1 + arr2, 0, maxval).astype(np.uint8)

    return Image.fromarray(result)


def subtract_images(inputImage1, inputImage2, maxval):
    if inputImage1.size != inputImage2.size:
        inputImage2 = inputImage2.resize(inputImage1.size)

    arr1 = np.array(inputImage1, dtype=np.int16)
    arr2 = np.array(inputImage2, dtype=np.int16)

    result = np.clip(arr1 - arr2, 0, maxval).astype(np.uint8)

    return Image.fromarray(result)


def multiply_images(inputImage1, inputImage2, maxval):
    if inputImage1.size != inputImage2.size:
        inputImage2 = inputImage2.resize(inputImage1.size)

    arr1 = np.array(inputImage1, dtype=np.float32) / maxval
    arr2 = np.array(inputImage2, dtype=np.float32) / maxval

    result = np.clip((arr1 * arr2) * maxval, 0, maxval).astype(np.uint8)

    return Image.fromarray(result)


def log_transform(inputImage, maxval, c=1.0):
    arr = np.array(inputImage, dtype=np.float32) / maxval

    log_arr = c * np.log(1.0 + arr)

    result = np.clip(log_arr * maxval, 0, maxval).astype(np.uint8)

    return Image.fromarray(result)


def power_transform(inputImage, maxval,gamma=1.0, c=1.0):

    arr = np.array(inputImage, dtype=np.float32) / maxval

    power_arr = c * np.power(arr, gamma)

    max_output = np.max(power_arr)
    if max_output > 0:
        power_arr = (power_arr / max_output) * maxval
    else:
        power_arr = power_arr * maxval

    result = np.clip(power_arr, 0, maxval).astype(np.uint8)
    return Image.fromarray(result)

def connected_component_labeling(inputLabel, connectivity=4):
    # Convert to grayscale if needed
    if inputLabel.pil_image.mode != 'L':
        gray = inputLabel.pil_image.convert('L')
    else:
        gray = inputLabel.pil_image

    arr = np.array(gray, dtype=np.uint8)
    height, width = arr.shape

    # Binary threshold (treat >0 as foreground)
    binary = (arr > 0).astype(np.uint8)

    # Output label image
    labels = np.zeros_like(binary, dtype=np.int32)

    # Neighbor definitions
    if connectivity == 4:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    elif connectivity == 8:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    current_label = 1

    # Iterate through pixels
    for y in range(height):
        for x in range(width):
            if binary[y, x] == 1 and labels[y, x] == 0:
                # Start BFS flood fill
                queue = deque()
                queue.append((y, x))
                labels[y, x] = current_label

                while queue:
                    cy, cx = queue.popleft()
                    for dy, dx in neighbors:
                        ny, nx = cy + dy, cx + dx
                        if (0 <= ny < height) and (0 <= nx < width):
                            if binary[ny, nx] == 1 and labels[ny, nx] == 0:
                                labels[ny, nx] = current_label
                                queue.append((ny, nx))

                current_label += 1

    # Normalize labels for visualization (map to 0–255 range)
    colors = [
        (255, 0, 0),  # 1
        (0, 255, 0),  # 2
        (0, 0, 255),  # 3
        (255, 255, 0),  # 4
        (255, 0, 255),  # 5
        (0, 255, 255),  # 6
        (128, 0, 0),  # 7
        (0, 128, 0),  # 8
        (0, 0, 128),  # 9
        (128, 128, 0),  # 10
        (128, 0, 128),  # 11
        (0, 128, 128),  # 12
        (255, 128, 0),  # 13
        (128, 255, 0),  # 14
        (0, 255, 128),  # 15
        (0, 128, 255),  # 16
        (128, 0, 255),  # 17
        (255, 0, 128),  # 18
        (192, 192, 192),  # 19
        (64, 64, 64),  # 20
    ]

    height, width = labels.shape
    rgb_image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            label = labels[y, x]
            if label > 0:
                # wrap around if there are more labels than colors
                color_index = (label - 1) % len(colors)
                rgb_image[y, x] = colors[color_index]
            else:
                rgb_image[y, x] = [0, 0, 0]  # background

    return Image.fromarray(rgb_image)

def connected_component_labeling_m(inputLabel):
    if inputLabel.pil_image.mode != 'L':
        gray = inputLabel.pil_image.convert('L')
    else:
        gray = inputLabel.pil_image

    arr = np.array(gray, dtype=np.uint8)
    binary = (arr > 0).astype(np.uint8)
    height, width = binary.shape

    labels = np.zeros_like(binary, dtype=np.int32)
    current_label = 1

    # Offsets for neighbors
    neighbors_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors_diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for y in range(height):
        for x in range(width):
            if binary[y, x] == 1 and labels[y, x] == 0:
                # Start BFS
                queue = deque()
                queue.append((y, x))
                labels[y, x] = current_label

                while queue:
                    cy, cx = queue.popleft()

                    # 4-connected neighbors (always allowed)
                    for dy, dx in neighbors_4:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if binary[ny, nx] == 1 and labels[ny, nx] == 0:
                                labels[ny, nx] = current_label
                                queue.append((ny, nx))

                    # m-connected diagonals (conditionally allowed)
                    for dy, dx in neighbors_diag:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if binary[ny, nx] == 1 and labels[ny, nx] == 0:
                                # Check shared 4-neighbors
                                if dy == -1 and dx == -1:  # top-left
                                    if not (binary[cy - 1, cx] and binary[cy, cx - 1]):
                                        labels[ny, nx] = current_label
                                        queue.append((ny, nx))
                                elif dy == -1 and dx == 1:  # top-right
                                    if not (binary[cy - 1, cx] and binary[cy, cx + 1]):
                                        labels[ny, nx] = current_label
                                        queue.append((ny, nx))
                                elif dy == 1 and dx == -1:  # bottom-left
                                    if not (binary[cy + 1, cx] and binary[cy, cx - 1]):
                                        labels[ny, nx] = current_label
                                        queue.append((ny, nx))
                                elif dy == 1 and dx == 1:  # bottom-right
                                    if not (binary[cy + 1, cx] and binary[cy, cx + 1]):
                                        labels[ny, nx] = current_label
                                        queue.append((ny, nx))

                current_label += 1

    # Normalize labels for visualization
    if current_label > 1:
        max_label = current_label - 1
        norm_labels = (labels * (255 // max_label)).astype(np.uint8)
    else:
        norm_labels = labels.astype(np.uint8)

    # Normalize labels for visualization (map to 0–255 range)
    colors = [
        (255, 0, 0),  # 1
        (0, 255, 0),  # 2
        (0, 0, 255),  # 3
        (255, 255, 0),  # 4
        (255, 0, 255),  # 5
        (0, 255, 255),  # 6
        (128, 0, 0),  # 7
        (0, 128, 0),  # 8
        (0, 0, 128),  # 9
        (128, 128, 0),  # 10
        (128, 0, 128),  # 11
        (0, 128, 128),  # 12
        (255, 128, 0),  # 13
        (128, 255, 0),  # 14
        (0, 255, 128),  # 15
        (0, 128, 255),  # 16
        (128, 0, 255),  # 17
        (255, 0, 128),  # 18
        (192, 192, 192),  # 19
        (64, 64, 64),  # 20
    ]

    height, width = labels.shape
    rgb_image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            label = labels[y, x]
            if label > 0:
                # wrap around if there are more labels than colors
                color_index = (label - 1) % len(colors)
                rgb_image[y, x] = colors[color_index]
            else:
                rgb_image[y, x] = [0, 0, 0]

    return Image.fromarray(rgb_image)

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