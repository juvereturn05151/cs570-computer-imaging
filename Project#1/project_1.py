import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")

        # canvas for image
        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # menu
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.load_image)
        filemenu.add_command(label="Save As", command=self.save_image)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        self.image = None
        self.tk_image = None
    def load_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("PPM files", "*.ppm")])
        if filepath:
            self.image = load_ppm(filepath)
            self.show_image()
    def save_image(self):
        if self.image is None:
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".ppm",
                                                filetypes=[("PPM files", "*.ppm")])
        if filepath:
            save_ppm(filepath, self.image)

    def show_image(self):
        if self.image is None:
            return
        # convert NumPy → PIL → Tkinter
        pil_img = Image.fromarray(self.image)
        self.tk_image = ImageTk.PhotoImage(pil_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

root = tk.Tk()
app = ImageApplication(root)
root.mainloop()