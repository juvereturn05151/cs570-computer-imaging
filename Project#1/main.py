import tkinter as tk
import gc
from gui_setup import setup_frames, setup_treeview, setup_image_labels, setup_command_interface
from image_data import load_default_images, load_negative_images, copy_images
from events import bind_events, setup_window_resize_monitor

def main():
    root = tk.Tk()
    root.title("CS 570 Project#1")
    root.geometry("1080x520")
    #setup GUI frames and get frame references
    top_frame, operation_frame, input_image_frame, input_image_frame, output_image_frame, command_frame = setup_frames(root)

    #setup treeview and get treeview reference and root item ID
    treeView, rootIID = setup_treeview(operation_frame)

    #load default images and store in imageData dictionary
    input_image_data = load_default_images(treeView, rootIID)
    input_image_data2 = copy_images(input_image_data)
    output_image_data = load_negative_images(input_image_data)

    #setup image display labels and get label references
    input_image_label, output_image_label = setup_image_labels(input_image_frame, output_image_frame, input_image_data, output_image_data)

    #setup command interface
    command_entry = setup_command_interface(command_frame, input_image_data, treeView, rootIID, output_image_label)

    #bind event handlers to widgets
    bind_events(treeView, input_image_label, output_image_label, input_image_data, output_image_data)

    #setup window resize monitoring
    setup_window_resize_monitor(root, input_image_label, output_image_label)

    root.mainloop()
    gc.collect()


if __name__ == "__main__":
    main()