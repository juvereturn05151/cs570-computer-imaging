import os
from PIL import Image, ImageTk
from image_ops import create_negative_image

def load_default_images(treeView, rootIID):
    imageData = {}
    filenameList = ['data/cameraman.ppm', 'data/butterfly-16.ppm', 'data/apple-20.ppm']

    for filename in filenameList:
        pil_image = Image.open(filename)
        tk_image = ImageTk.PhotoImage(pil_image)
        neg_pil_image = create_negative_image(pil_image)
        neg_tk_image = ImageTk.PhotoImage(neg_pil_image)
        name = os.path.basename(filename)

        imageData[name] = {
            "input": {"pil": pil_image, "tk": tk_image},
            "output": {"pil": neg_pil_image, "tk": neg_tk_image},
        }

        treeView.insert(rootIID, -1, text=name)

    return imageData