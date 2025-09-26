from PIL import ImageTk
from gui import on_tree_select, on_tree_select2
from image_ops import nearest_neighbor

def bind_events(treeView, imageLabel, outputImageLabel, input_image_data, output_image_frame):
    treeView.bind('<<TreeviewSelect>>',
                  lambda e: on_tree_select(e, treeView, imageLabel, outputImageLabel, input_image_data, output_image_frame))

def bind_events2(treeView, imageLabel, input_image_data):
    treeView.bind('<<TreeviewSelect>>',
                  lambda e: on_tree_select2(e, treeView, imageLabel, input_image_data))

def setup_window_resize_monitor(root, inputLabel, inputLabel2, outputImageLabel):
    """Setup event handler to monitor window resize and print image sizes"""
    def on_window_resize(event):
        """Event handler called when window is resized"""
        # Get the current size of the input image label
        input_label_width = inputLabel.winfo_width()
        input_label_height = inputLabel.winfo_height()

        input_label_width2 = inputLabel2.winfo_width()
        input_label_height2 = inputLabel2.winfo_height()

        # Get the current size of the output image label
        output_label_width = outputImageLabel.winfo_width()
        output_label_height = outputImageLabel.winfo_height()

        if hasattr(inputLabel, "pil_image") and inputLabel.pil_image is not None:
            resized_pil_image = nearest_neighbor(inputLabel.original_pil, input_label_width, input_label_height)

            inputLabel.pil_image = resized_pil_image
            inputLabel.tk_image = ImageTk.PhotoImage(resized_pil_image)

            inputLabel.configure(image=inputLabel.tk_image)

        if hasattr(inputLabel2, "pil_image") and inputLabel2.pil_image is not None:
            resized_pil_image = nearest_neighbor(inputLabel2.original_pil, input_label_width2, input_label_height2)

            inputLabel2.pil_image = resized_pil_image
            inputLabel2.tk_image = ImageTk.PhotoImage(resized_pil_image)

            inputLabel2.configure(image=inputLabel2.tk_image)

        if hasattr(outputImageLabel, "pil_image") and outputImageLabel.pil_image is not None:
            resized_pil_image = nearest_neighbor(outputImageLabel.original_pil, output_label_width, output_label_height)

            outputImageLabel.pil_image = resized_pil_image
            outputImageLabel.tk_image = ImageTk.PhotoImage(resized_pil_image)

            outputImageLabel.config(image=outputImageLabel.tk_image)

    # Bind the resize event handler
    root.bind('<Configure>', on_window_resize)
    inputLabel.master.bind('<Configure>', on_window_resize)
    outputImageLabel.master.bind('<Configure>', on_window_resize)