import tkinter as tk
import gc
from gui_setup import setup_frames, setup_treeview, setup_image_labels, setup_command_interface
from image_data import load_default_images
from events import bind_events, setup_window_resize_monitor

def main():
    root = tk.Tk()
    root.title("CS 570 Project#1")
    root.geometry("1080x520")
    #setup GUI frames and get frame references
    topFrame, operationFrame, imageFrame, outputImageFrame, commandFrame = setup_frames(root)

    #setup treeview and get treeview reference and root item ID
    treeView, rootIID = setup_treeview(operationFrame)

    #load default images and store in imageData dictionary
    imageData = load_default_images(treeView, rootIID)

    #setup image display labels and get label references
    imageLabel, outputImageLabel = setup_image_labels(imageFrame, outputImageFrame, imageData)

    #setup command interface
    command_entry = setup_command_interface(commandFrame, imageData, treeView, rootIID, outputImageLabel)

    #bind event handlers to widgets
    bind_events(treeView, imageLabel, outputImageLabel, imageData)

    #setup window resize monitoring
    setup_window_resize_monitor(root, imageLabel, outputImageLabel)

    root.mainloop()
    gc.collect()


if __name__ == "__main__":
    main()