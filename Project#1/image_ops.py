from PIL import Image, ImageTk, ImageOps
import math

# receive Pil image, and return a PIL image
def create_negative_image(pil_image, maxval=255 ):
    # check if it is a pil_image
    if not isinstance(pil_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    image_data = pil_image.load()
    width, height = pil_image.size
    negative_image = Image.new(pil_image.mode, (width, height))
    neg_data = negative_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = image_data[x, y]
            neg_data[x, y] = (maxval - r, maxval - g, maxval - b)
    return negative_image

def nearest_neighbor(pil_image, new_width, new_height):
    original_width, original_height = pil_image.size
    new_image = Image.new(pil_image.mode, (new_width, new_height))

    original_pixels = pil_image.load()
    new_pixels = new_image.load()

    x_ratio = original_width / new_width
    y_ratio = original_height / new_height

    for y in range(new_height):
        for x in range(new_width):
            orig_x = min(math.floor(x * x_ratio), original_width - 1)
            orig_y = min(math.floor(y * y_ratio), original_height - 1)

            new_pixels[x, y] = original_pixels[orig_x, orig_y]

    return new_image