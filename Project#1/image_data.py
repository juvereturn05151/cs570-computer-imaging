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
            "pil": pil_image,
            "tk": tk_image
        }

        treeView.insert(rootIID, -1, text=name)

    return imageData

def load_negative_images(imageData):
    negImageData = {}

    for name, imgDict in imageData.items():
        orig_pil = imgDict["pil"]
        neg_pil = create_negative_image(orig_pil)
        neg_tk = ImageTk.PhotoImage(neg_pil)

        negImageData[name] = {
            "pil": neg_pil,
            "tk": neg_tk,
        }

    return negImageData