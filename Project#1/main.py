import tkinter as tk
import gc
import os
from gui_setup import setup_frames, setup_treeview, setup_image_labels, setup_command_interface, setup_interpolation_options, setup_operations_panel
from image_data import load_default_images, load_negative_images, copy_images
from events import bind_events, setup_window_resize_monitor, bind_events2

ORIGIN_PATH = os.path.join(os.getcwd(), "data")

if not os.path.exists(ORIGIN_PATH):
    os.makedirs(ORIGIN_PATH)
os.chdir(ORIGIN_PATH)

def main():
    root = tk.Tk()
    root.title("CS 570 Project#1")
    root.geometry("1080x560")
    #setup GUI frames and get frame references
    top_frame, operation_frame, operation_frame2, input_image_frame, input_image_frame2, output_image_frame, command_frame = setup_frames(root)

    #setup treeview and get treeview reference and root item ID
    tree_view, rootIID = setup_treeview(operation_frame)
    tree_view2, rootIID2 = setup_treeview(operation_frame2)

    #load default images and store in imageData dictionary
    input_image_data = load_default_images(tree_view, rootIID)
    input_image_data2 = copy_images(input_image_data, tree_view2, rootIID2 )
    output_image_data = load_negative_images(input_image_data)

    #setup image display labels and get label references
    input_image_label, input_image_label2, output_image_label = setup_image_labels(input_image_frame, input_image_frame2, output_image_frame, input_image_data, input_image_data2, output_image_data)

    #setup command interface
    setup_command_interface(command_frame, input_image_data, tree_view, rootIID, output_image_label)

    setup_operations_panel(command_frame, input_image_label, input_image_label2, output_image_label)

    # setup interpolation options
    interpolation_var = setup_interpolation_options(command_frame)
    #bind event handlers to widgets
    bind_events(tree_view, input_image_label, output_image_label, input_image_data, output_image_data)

    bind_events2(tree_view2, input_image_label2, input_image_data2)

    #setup window resize monitoring
    setup_window_resize_monitor(root, interpolation_var, input_image_label, input_image_label2, output_image_label)

    root.mainloop()
    gc.collect()


if __name__ == "__main__":
    main()