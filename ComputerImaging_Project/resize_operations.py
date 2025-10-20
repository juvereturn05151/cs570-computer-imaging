from PIL import Image
import math
def nearest_neighbor_resize(pil_image, new_width, new_height):
    original_width, original_height = pil_image.size
    new_image = Image.new(pil_image.mode, (new_width, new_height))

    original_pixels = pil_image.load()
    new_pixels = new_image.load()

    x_ratio = (original_width - 1) / (new_width - 1)if new_width > 1 else 0
    y_ratio = (original_height - 1) / (new_height - 1)if new_height > 1 else 0

    for y in range(new_height):
        for x in range(new_width):
            orig_x = min(int(round(x * x_ratio)), original_width - 1)
            orig_y = min(int(round(y * y_ratio)), original_height - 1)

            new_pixels[x, y] = original_pixels[orig_x, orig_y]

    return new_image

#compute each new pixel as a weighted average of 4 nearest pixels in the original image.
def billinear_interpolation_resize(pil_image, new_width, new_height):
    original_width, original_height = pil_image.size
    new_image = Image.new(pil_image.mode, (new_width, new_height))

    original_pixels = pil_image.load()
    new_pixels = new_image.load()

    #how pixels in the new image map to the original image.
    x_ratio = (original_width - 1) / (new_width - 1) if new_width > 1 else 0
    y_ratio = (original_height - 1) / (new_height - 1) if new_height > 1 else 0

    for y in range(new_height):
        for x in range(new_width):
            #get original floating points coordinates
            orig_x = x * x_ratio
            orig_y = y * y_ratio

            #identify surrounding pixels
            x1 = math.floor(orig_x)
            y1 = math.floor(orig_y)
            x2 = min(x1 + 1, original_width - 1)
            y2 = min(y1 + 1, original_height - 1)

            #how far from x1(left)
            dx = orig_x - x1
            # how far from y1(top)
            dy = orig_y - y1

            #get 4 neighbors
            Q11 = original_pixels[x1, y1]
            Q21 = original_pixels[x2, y1]
            Q12 = original_pixels[x1, y2]
            Q22 = original_pixels[x2, y2]

            #for color image
            if isinstance(Q11, tuple):
                interpolated_pixel = (tuple
                    (
                    round(
                        Q11[c]*(1-dx)*(1-dy) +
                        Q21[c]*dx*(1-dy) +
                        Q12[c]*(1-dx)*dy +
                        Q22[c]*dx*dy
                    )
                    for c in range(len(Q11))
                ))
            #for grayscale image
            else:
                interpolated_pixel = round(
                    Q11*(1-dx)*(1-dy) +
                    Q21*dx*(1-dy) +
                    Q12*(1-dx)*dy +
                    Q22*dx*dy
                )

            new_pixels[x, y] = interpolated_pixel

    return new_image