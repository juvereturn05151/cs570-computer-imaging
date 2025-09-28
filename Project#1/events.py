from PIL import ImageTk
from gui import on_tree_select, on_tree_select2
from image_ops import nearest_neighbor, billinear_interpolation


def bind_events(treeView, imageLabel, outputImageLabel, input_image_data, output_image_frame):
    treeView.bind('<<TreeviewSelect>>',
                  lambda e: on_tree_select(e, treeView, imageLabel, outputImageLabel, input_image_data, output_image_frame))


def bind_events2(treeView, imageLabel, input_image_data):
    treeView.bind('<<TreeviewSelect>>',
                  lambda e: on_tree_select2(e, treeView, imageLabel, input_image_data))


def setup_window_resize_monitor(root, interpolation_var, inputLabel, inputLabel2, outputImageLabel):
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
        method = interpolation_var.get()

        # Resize each label
        resize_label_image(inputLabel, inputLabel.winfo_width(), inputLabel.winfo_height(), method)
        resize_label_image(inputLabel2, inputLabel2.winfo_width(), inputLabel2.winfo_height(), method)
        resize_label_image(outputImageLabel, outputImageLabel.winfo_width(), outputImageLabel.winfo_height(), method)

    # Bind the resize event handler
    root.bind('<Configure>', on_window_resize)
    inputLabel.master.bind('<Configure>', on_window_resize)
    outputImageLabel.master.bind('<Configure>', on_window_resize)
