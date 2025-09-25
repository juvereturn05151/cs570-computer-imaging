from PIL import Image, ImageTk, ImageOps

# receive Pil image, and return a PIL image
def create_negative_image(pil_image):
    # Check if it is a pil_image
    if not isinstance(pil_image, Image.Image):
        raise ValueError("Input must be a PIL Image object")

    # Convert to a format that allows pixel manipulation
    image_data = pil_image.load()
    width, height = pil_image.size
    negative_image = Image.new(pil_image.mode, (width, height))
    neg_data = negative_image.load()

    for y in range(height):
        for x in range(width):
            r, g, b = image_data[x, y]
            neg_data[x, y] = (255 - r, 255 - g, 255 - b)
    return negative_image
