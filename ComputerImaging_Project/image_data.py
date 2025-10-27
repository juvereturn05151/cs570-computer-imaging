"""
File Name:    unsharp_masking.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import os
from PIL import Image, ImageTk

def get_ppm_maxvalue(filename):
    with open(filename, "rb") as f:
        header = f.readline().strip()
        if header not in [b"P3", b"P6"]:
            raise ValueError("Not a valid PPM file")

        line = f.readline().strip()
        while line.startswith(b"#"):
            line = f.readline().strip()

        parts = line.split()
        if len(parts) < 2:
            parts += f.readline().split()
        width, height = map(int, parts)

        maxval = int(f.readline().strip())
        return maxval

def load_default_images(treeView, rootIID):
    imageData = {}
    filenameList = ['cameraman.ppm', 'butterfly-16.ppm', 'apple-20.ppm', 'beetle-13.ppm', 'cup-9.ppm', 'mandril_gray.ppm']

    for filename in filenameList:
        pil_image = Image.open(filename)
        tk_image = ImageTk.PhotoImage(pil_image)
        name = os.path.basename(filename)
        maxval = get_ppm_maxvalue(filename)

        imageData[name] = {
            "pil": pil_image,
            "tk": tk_image,
            "maxval": maxval,
        }

        treeView.insert(rootIID, -1, text=name)

    return imageData

def copy_images(imageData, treeView, rootIID):
    newImageData = {}

    for name, imgDict in imageData.items():
        # Duplicate the PIL image
        pil_copy = imgDict["pil"].copy()
        # Create a new Tk wrapper for that copy
        tk_copy = ImageTk.PhotoImage(pil_copy)

        newImageData[name] = {
            "pil": pil_copy,
            "tk": tk_copy,
            "maxval": imgDict["maxval"],
        }

        treeView.insert(rootIID, -1, text=name)

    return newImageData

def load_output_images(imageData):
    negImageData = {}

    for name, imgDict in imageData.items():
        orig_pil = imgDict["pil"]
        neg_pil = orig_pil
        neg_tk = ImageTk.PhotoImage(neg_pil)

        negImageData[name] = {
            "pil": neg_pil,
            "tk": neg_tk,
            "maxval": imgDict["maxval"],
        }

    return negImageData

def update_output_image(outputLabel, pil_image):
    outputLabel.original_pil = pil_image
    outputLabel.pil_image = pil_image
    outputLabel.tk_image = ImageTk.PhotoImage(pil_image)
    outputLabel.configure(image=outputLabel.tk_image)