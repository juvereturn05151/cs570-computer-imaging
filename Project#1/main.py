import tkinter as tk  # Import tkinter for GUI creation
from tkinter import ttk  # Import themed tkinter widgets
import gc  # Import garbage collector for memory management
from image_ops import create_negative_image  # Import function to create negative images
from commands import execute_command  # Import command execution function
from PIL import Image, ImageTk  # Import PIL for image processing and tkinter integration
import os  # Import os for file path operations
from events import bind_events, setup_window_resize_monitor

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