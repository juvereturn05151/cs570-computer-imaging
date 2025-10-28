"""
File Name:    unsharp_masking.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import os
from PIL import Image, ImageTk

file_name_list = ['cameraman.ppm', 'butterfly-16.ppm', 'apple-20.ppm',
                  'beetle-13.ppm', 'cup-9.ppm', 'mandril_gray.ppm']


class ImageData:
    def __init__(self, pil_image, max_val):
        self.pil = pil_image
        self.tk = ImageTk.PhotoImage(pil_image)
        self.max_val = max_val

    def copy(self):
        """Return a copy with duplicated PIL image"""
        return ImageData(self.pil.copy(), self.max_val)

def get_ppm_maxvalue(filename):
    """Read PPM file and return max value (Usually 255)"""
    with open(filename, "rb") as f:
        header = f.readline().strip()
        if header not in [b"P3", b"P6"]:
            raise ValueError("Not a valid PPM file")

        line = f.readline().strip()
        while line.startswith(b"#"):
            line = f.readline().strip()

        parts = line.split()
        if len(parts) < 2:
            parts += f.readline().split()

        max_val = int(f.readline().strip())
        return max_val

def load_default_images(tree_view, root_id):
    image_data = {}

    for filename in file_name_list:
        pil_image = Image.open(filename)
        name = os.path.basename(filename)
        max_val = get_ppm_maxvalue(filename)

        image_data[name] = ImageData(pil_image, max_val)
        tree_view.insert(root_id, -1, text=name)

    return image_data

def copy_images(image_data, tree_view, root_id):
    new_image_data = {}

    for name, img_data in image_data.items():
        new_image_data[name] = img_data.copy()  # Much cleaner!
        tree_view.insert(root_id, -1, text=name)

    return new_image_data

def load_output_images(image_data):
    """Simply reuse the existing ImageData - no need to recreate"""
    output_image_data = {}

    for name, img_data in image_data.items():
        output_image_data[name] = img_data

    return output_image_data

def update_output_image(output_label, pil_image):
    """Update and configure the output image"""
    output_label.original_pil = pil_image
    output_label.pil_image = pil_image
    output_label.tk_image = ImageTk.PhotoImage(pil_image)
    output_label.configure(image=output_label.tk_image)