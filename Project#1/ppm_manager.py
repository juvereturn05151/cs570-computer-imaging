import numpy as np


def load_ppm(filename):
    with open(filename, 'r') as f:
        assert f.readline().strip() == "P3"  # format check
        width, height = map(int, f.readline().split())
        maxval = int(f.readline())

        # read pixel values
        data = []
        for line in f:
            data.extend(line.split())

        data = np.array(data, dtype=np.uint8)
        image = data.reshape((height, width, 3))
        return image


def save_ppm(filename, image):
    height, width, _ = image.shape
    with open(filename, 'w') as f:
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")
        for row in image:
            for pixel in row:
                f.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
            f.write("\n")
