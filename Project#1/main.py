import tkinter as tk  # Import tkinter for GUI creation
from tkinter import ttk  # Import themed tkinter widgets
import gc  # Import garbage collector for memory management
from gui import on_tree_select, load_image, resize_image_to_fit  # Import functions from gui module
from image_ops import create_negative_image  # Import function to create negative images
from commands import execute_command  # Import command execution function
from PIL import Image, ImageTk  # Import PIL for image processing and tkinter integration
import os  # Import os for file path operations


def setup_frames(root):
    """Create and organize all frames in the main window"""
    topFrame = tk.Frame(root)  # Create top frame to hold main content
    operationFrame = tk.Frame(topFrame)  # Create frame for operations (treeview)
    imageFrame = tk.Frame(topFrame)  # Create frame for input image display
    outputImageFrame = tk.Frame(topFrame)  # Create frame for output image display

    # Pack top frame to fill top portion of window and expand with window size
    topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # Pack operation frame to left side, fill vertically
    operationFrame.pack(side=tk.LEFT, fill=tk.Y)
    # Pack image frame to left, fill available space and expand
    imageFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    imageFrame.pack_propagate(False)
    # Pack output frame to right, fill available space and expand
    outputImageFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    outputImageFrame.pack_propagate(False)
    # Return all frames including a new command frame
    return topFrame, operationFrame, imageFrame, outputImageFrame, tk.Frame(root)


def setup_treeview(operationFrame):
    """Create and configure the treeview widget for image selection"""
    # Create treeview widget with browse selection mode
    treeView = ttk.Treeview(operationFrame, selectmode='browse')
    # Insert root item for image list with empty parent and auto index
    rootIID = treeView.insert('', -1, text="Image List")
    # Pack treeview with padding
    treeView.pack(padx=10, pady=10)
    # Return treeview and root item ID
    return treeView, rootIID


def load_default_images(treeView, rootIID):
    """Load default images and populate the treeview"""
    imageData = {}  # Dictionary to store image info

    filenameList = ['data/cameraman.ppm', 'data/butterfly-16.ppm', 'data/apple-20.ppm']

    for filename in filenameList:
        pil_img = Image.open(filename)  # PIL Image
        tk_img = ImageTk.PhotoImage(pil_img)  # Tkinter PhotoImage

        # Create default negative output
        neg_pil = create_negative_image(pil_img)
        neg_tk = ImageTk.PhotoImage(neg_pil)

        name = os.path.basename(filename)

        # Store both input and output images in dictionary
        imageData[name] = {
            "input": {
                "pil": pil_img,
                "tk": tk_img
            },
            "output": {
                "pil": neg_pil,
                "tk": neg_tk
            }
        }

        # Add to treeview
        treeView.insert(rootIID, -1, text=name)

    return imageData


def setup_image_labels(imageFrame, outputImageFrame, imageData, default_name='apple-20.ppm'):
    if default_name not in imageData:
        raise ValueError(f"Default image '{default_name}' not found in imageData")

    # Input image
    pil_input = imageData[default_name]["input"]["pil"]
    tk_input = imageData[default_name]["input"]["tk"]

    imageLabel = tk.Label(imageFrame, image=tk_input)
    imageLabel.pack(padx=10, pady=10)

    imageLabel.original_pil = pil_input
    imageLabel.pil_image = pil_input
    imageLabel.tk_image = tk_input

    # Output image
    pil_output = imageData[default_name]["output"]["pil"]
    tk_output = imageData[default_name]["output"]["tk"]

    outputImageLabel = tk.Label(outputImageFrame, image=tk_output)
    outputImageLabel.pack(padx=10, pady=10)

    outputImageLabel.original_pil = pil_output
    outputImageLabel.pil_image = pil_output
    outputImageLabel.tk_image = tk_output

    return imageLabel, outputImageLabel


def setup_command_interface(commandFrame, imageData, treeView, rootIID, outputImageLabel):
    """Create command entry interface and bind event handlers"""
    # Create label for command prompt
    commandLabel = tk.Label(commandFrame, text="Execute command:")
    # Pack label to left side with padding
    commandLabel.pack(side=tk.LEFT, padx=5, pady=5)

    # Create entry widget for command input
    command_entry = ttk.Entry(commandFrame)
    # Pack entry to left, fill horizontal space, expand with padding
    command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
    # Bind Enter key press to execute_command function with parameters
    command_entry.bind("<Return>",
                       lambda e: execute_command(e, command_entry, imageData, treeView, rootIID, outputImageLabel))
    # Return command entry widget
    return command_entry


def bind_events(treeView, imageLabel, outputImageLabel, imageData):
    """Bind event handlers to widgets"""
    # Bind treeview selection event to on_tree_select function
    treeView.bind('<<TreeviewSelect>>',
                  lambda e: on_tree_select(e, treeView, imageLabel, outputImageLabel, imageData))


def setup_window_resize_monitor(root, imageLabel, outputImageLabel):
    """Setup event handler to monitor window resize and print image sizes"""

    def on_window_resize(event):
        """Event handler called when window is resized"""
        # Get the current size of the input image label
        image_label_width = imageLabel.winfo_width()  # Get width of input image label in pixels
        image_label_height = imageLabel.winfo_height()  # Get height of input image label in pixels

        # Get the current size of the output image label
        output_label_width = outputImageLabel.winfo_width()  # Get width of output image label in pixels
        output_label_height = outputImageLabel.winfo_height()  # Get height of output image label in pixels

        print("\n=== IMAGE INFORMATION ===")

        rw, rh = root.winfo_width(), root.winfo_height()
        print(f"Root Window Size: {rw}x{rh}")

        # Print the sizes to console with descriptive labels
        print(f"Window Resized - Input Label Image: {image_label_width}x{image_label_height}, Output Image: {output_label_width}x{output_label_height}")

        if hasattr(imageLabel, "pil_image") and imageLabel.pil_image is not None:
            w, h = imageLabel.pil_image.size
            print(f"Before: Input Image Size: {w}x{h}, Mode: {imageLabel.pil_image.mode}")
            resized_pil = resize_image_to_fit(imageLabel.original_pil, image_label_width, image_label_height)

            # Update references
            imageLabel.pil_image = resized_pil
            imageLabel.tk_image = ImageTk.PhotoImage(resized_pil)

            # Reconfigure label to show new image
            imageLabel.config(image=imageLabel.tk_image)
            print(f"After: Input Image Size_image.: {w}x{h}, Mode: {imageLabel.pil_image.mode}")

        if hasattr(outputImageLabel, "pil_image") and outputImageLabel.pil_image is not None:

            w, h = outputImageLabel.pil_image.size
            print(f"Output Image Size: {w}x{h}, Mode: {outputImageLabel.pil_image.mode}")

            resized_pil = resize_image_to_fit(outputImageLabel.original_pil, output_label_width, output_label_height)

            # Update references
            outputImageLabel.pil_image = resized_pil
            outputImageLabel.tk_image = ImageTk.PhotoImage(resized_pil)

            outputImageLabel.config(image=outputImageLabel.tk_image)
            print(f"After: Output Image Size_image.: {w}x{h}, Mode: {outputImageLabel.pil_image.mode}")



    # Bind the resize event handler to the main window
    # The '<Configure>' event fires when window size or position changes
    root.bind('<Configure>', on_window_resize)

    # Also bind to the image frames for more specific monitoring
    imageLabel.master.bind('<Configure>', on_window_resize)  # Bind to input image frame
    outputImageLabel.master.bind('<Configure>', on_window_resize)  # Bind to output image frame


def main():
    """Main function to initialize and run the application"""
    root = tk.Tk()  # Create main tkinter window
    root.title("CS 570 Project#1")  # Set window title

    # Setup GUI frames and get frame references
    topFrame, operationFrame, imageFrame, outputImageFrame, commandFrame = setup_frames(root)

    # Setup treeview and get treeview reference and root item ID
    treeView, rootIID = setup_treeview(operationFrame)

    # Load default images and store in imageData dictionary
    imageData = load_default_images(treeView, rootIID)

    # Setup image display labels and get label references
    imageLabel, outputImageLabel = setup_image_labels(imageFrame, outputImageFrame, imageData)

    # Setup command interface
    command_entry = setup_command_interface(commandFrame, imageData, treeView, rootIID, outputImageLabel)

    # Bind event handlers to widgets
    bind_events(treeView, imageLabel, outputImageLabel, imageData)

    # Setup window resize monitoring
    setup_window_resize_monitor(root, imageLabel, outputImageLabel)

    # Start tkinter main event loop
    root.mainloop()

    # Force garbage collection after application closes
    gc.collect()


# Standard Python idiom to check if this file is being run directly
if __name__ == "__main__":
    main()  # Execute main function if file is run directly