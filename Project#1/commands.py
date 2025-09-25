import tkinter as tk
import os
from gui import load_image, save_output_image  # import from gui.py

def execute_command(event=None, command_entry=None, imageData=None, treeView=None, rootIID=None, outputImageLabel=None):
    cmd = command_entry.get().strip()
    command_entry.delete(0, tk.END)

    if(is_command_valid(cmd)):
        filename = cmd.split(" ", 1)[1]
        if cmd.startswith("load "):
            if not os.path.exists("data/" + filename):
                print(f"File not found: {filename}")
                return

            load_image(filename, imageData, treeView, rootIID)
        elif cmd.startswith("save "):
            save_output_image(filename, outputImageLabel)
    else:
        print(f"Unknown command: {cmd}")

def is_command_valid(command):
    return command.startswith("load ") or command.startswith("save ")
