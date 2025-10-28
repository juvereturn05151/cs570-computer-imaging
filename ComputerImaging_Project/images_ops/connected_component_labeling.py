"""
File Name:    unsharp_masking.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

from collections import deque
import numpy as np
from PIL import Image

# predefined 20 colors
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0),
    (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
    (255, 128, 0), (128, 255, 0), (0, 255, 128), (0, 128, 255),
    (128, 0, 255), (255, 0, 128), (192, 192, 192), (64, 64, 64),
]

def prepare_binary(input_label, threshold=128):
    gray = input_label.pil_image.convert('L') if input_label.pil_image.mode != 'L' else input_label.pil_image
    arr = np.array(gray, dtype=np.uint8)
    return (arr > threshold).astype(np.uint8)

def visualize_labels(labels):
    h, w = labels.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            label = labels[y, x]
            if label > 0:
                rgb[y, x] = COLORS[(label - 1) % len(COLORS)]
    return Image.fromarray(rgb)

def connected_component_label(input_label, connectivity=4):
    binary = prepare_binary(input_label)
    h, w = binary.shape
    labels = np.zeros_like(binary, dtype=np.int32)
    current_label = 1

    if connectivity == 4:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    elif connectivity == 8:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for y in range(h):
        for x in range(w):
            if binary[y, x] and labels[y, x] == 0:
                queue = deque([(y, x)])
                labels[y, x] = current_label
                while queue:
                    cy, cx = queue.popleft()
                    for dy, dx in neighbors:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w:
                            if binary[ny, nx] and labels[ny, nx] == 0:
                                labels[ny, nx] = current_label
                                queue.append((ny, nx))
                current_label += 1

    return visualize_labels(labels)

def connected_component_label_m(inputLabel):
    binary = prepare_binary(inputLabel)
    h, w = binary.shape
    labels = np.zeros_like(binary, dtype=np.int32)
    current_label = 1

    neighbors_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors_diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for y in range(h):
        for x in range(w):
            if binary[y, x] and labels[y, x] == 0:
                queue = deque([(y, x)])
                labels[y, x] = current_label
                while queue:
                    cy, cx = queue.popleft()
                    # check 4-connected
                    for dy, dx in neighbors_4:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w:
                            if binary[ny, nx] and labels[ny, nx] == 0:
                                labels[ny, nx] = current_label
                                queue.append((ny, nx))
                    # then check diagonals
                    for dy, dx in neighbors_diag:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w:
                            if binary[ny, nx] and labels[ny, nx] == 0:
                                if dy == -1 and dx == -1 and not (binary[cy-1, cx] and binary[cy, cx-1]):
                                    labels[ny, nx] = current_label; queue.append((ny, nx))
                                elif dy == -1 and dx == 1 and not (binary[cy-1, cx] and binary[cy, cx+1]):
                                    labels[ny, nx] = current_label; queue.append((ny, nx))
                                elif dy == 1 and dx == -1 and not (binary[cy+1, cx] and binary[cy, cx-1]):
                                    labels[ny, nx] = current_label; queue.append((ny, nx))
                                elif dy == 1 and dx == 1 and not (binary[cy+1, cx] and binary[cy, cx+1]):
                                    labels[ny, nx] = current_label; queue.append((ny, nx))
                current_label += 1

    return visualize_labels(labels)
