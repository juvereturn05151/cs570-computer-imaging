import os
from PIL import Image, ImageTk
from image_ops import create_negative_image

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
    filenameList = ['data/cameraman.ppm', 'data/butterfly-16.ppm', 'data/apple-20.ppm']

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

def load_negative_images(imageData):
    negImageData = {}

    for name, imgDict in imageData.items():
        orig_pil = imgDict["pil"]
        maxval = imgDict.get("maxval", 255)
        neg_pil = create_negative_image(orig_pil, maxval)
        neg_tk = ImageTk.PhotoImage(neg_pil)

        negImageData[name] = {
            "pil": neg_pil,
            "tk": neg_tk,
            "maxval": imgDict["maxval"],
        }

    return negImageData