"""
File Name:    events.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

from PIL import ImageTk

from ui.gui import on_tree_select
from images_ops.image_ops import nearest_neighbor, billinear_interpolation

def bind_events(tree_view, image_label, input_image_data):
    """Bind the event when selecting an image on the first tree"""
    tree_view.bind('<<TreeviewSelect>>',
                  lambda e: on_tree_select(e, tree_view, image_label, input_image_data))

def setup_window_resize_monitor(root, interpolation_var, input_label1, input_label2, output_image_label):
    """Setup event handler to monitor window resize and update images."""

    def resize_label_image(label, width, height, method):
        """Helper to resize and update a single label image."""
        if hasattr(label, "pil_image") and label.pil_image is not None:
            if method == "nearest":
                resized_pil_image = nearest_neighbor(label.original_pil, width, height)
            else:
                resized_pil_image = billinear_interpolation(label.original_pil, width, height)

            label.pil_image = resized_pil_image
            label.tk_image = ImageTk.PhotoImage(resized_pil_image)
            label.configure(image=label.tk_image)

    def on_window_resize(event):
        """Resize each label"""
        method = interpolation_var.get()

        resize_label_image(input_label1, input_label1.winfo_width(), input_label1.winfo_height(), method)
        resize_label_image(input_label2, input_label2.winfo_width(), input_label2.winfo_height(), method)
        resize_label_image(output_image_label, output_image_label.winfo_width(), output_image_label.winfo_height(), method)

    # bind the resize event handler
    root.bind('<Configure>', on_window_resize)
    input_label1.master.bind('<Configure>', on_window_resize)
    output_image_label.master.bind('<Configure>', on_window_resize)
