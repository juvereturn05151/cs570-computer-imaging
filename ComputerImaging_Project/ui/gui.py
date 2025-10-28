"""
File Name:    unsharp_masking.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import os
from PIL import Image

from image_data import get_ppm_maxvalue, ImageData

def select_image(image_name, image_label, output_image_label, input_image_data, output_image_frame):
    """Update input image"""
    img_data = input_image_data[image_name]
    image_label.config(image=img_data.tk)
    image_label.tk_image = img_data.tk
    image_label.original_pil = img_data.pil
    image_label.pil_image = img_data.pil

def select_image2(image_name, input_image_label, input_image_data):
    """Update input 2nd image"""
    img_data = input_image_data[image_name]
    input_image_label.config(image=img_data.tk)
    input_image_label.tk_image = img_data.tk
    input_image_label.original_pil = img_data.pil
    input_image_label.pil_image = img_data.pil

def on_tree_select(event, tree_view, input_image_label, output_image_label, input_image_data, output_image_data):
    """Update an input image when select from the 1st tree"""
    selected_item = tree_view.focus()
    item_details = tree_view.item(selected_item)
    item_text = item_details['text']
    if item_text in input_image_data:
        select_image(item_text, input_image_label, output_image_label, input_image_data, output_image_data)

def on_tree_select2(event, tree_view, input_image_label, input_image_data):
    """Update an input image when select from the 2nd tree"""
    selected_item = tree_view.focus()
    item_details = tree_view.item(selected_item)
    item_text = item_details['text']
    if item_text in input_image_data:
        select_image2(item_text, input_image_label, input_image_data)


def load_image(load_file_name, input_image_data, tree_view=None, root_id=None):
    pil_image = Image.open(load_file_name)
    name = os.path.basename(load_file_name)

    # get max_val for PPM
    try:
        max_val = get_ppm_maxvalue('data/' + load_file_name)
    except Exception:
        # default fallback for non-PPM images
        max_val = 255
        
    # store using ImageData class
    input_image_data[name] = ImageData(pil_image, max_val)

    # insert into TreeView if provided
    if tree_view is not None and root_id is not None:
        tree_view.insert(root_id, -1, text=name)

def save_output_image(file_name, output_image_label):
    """Check if we have a PIL image stored"""
    if not hasattr(output_image_label, 'pil_image'):
        print("No OutputImage")
        return

    if output_image_label.pil_image:
        if not file_name.endswith('.ppm'):
            file_name += '.ppm'
            print(f"Added .ppm extension. Saving as: {file_name}")

        output_image_label.pil_image.save(file_name)
        print(f"Image saved to save_images/{file_name}")
    else:
        print("No output image to save")