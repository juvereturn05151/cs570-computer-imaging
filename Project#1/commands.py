import tkinter as tk
import os
from gui import load_image, save_output_image  # import from gui.py



def execute_command(event=None, command_entry=None, imageData=None, treeView=None, rootIID=None, outputImageLabel=None, path_label=None):
    cmd = command_entry.get().strip()
    command_entry.delete(0, tk.END)

    if(is_command_valid(cmd)):
        filename = cmd.split(" ", 1)[1]
        if cmd.startswith("cd "):
            new_dir = cmd[3:].strip()
            if os.path.isdir(new_dir):
                os.chdir(new_dir)
                print(f"Changed directory to: {os.getcwd()}")
                if path_label:
                    path_label.config(text=f"Current Path: {os.getcwd()}")
            else:
                print(f"Directory not found: {new_dir}")

        if cmd.startswith("load "):
            if not os.path.exists(filename):
                print(f"File not found: {filename}")
                return

            load_image(filename, imageData, treeView, rootIID)
        elif cmd.startswith("save "):
            save_output_image(filename, outputImageLabel)

    else:
        print(f"Unknown command: {cmd}")

def is_command_valid(command):
    return command.startswith("load ") or command.startswith("save ") or command.startswith("cd ")
