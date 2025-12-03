"""
File Name:    pseudo_color_spectrum.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

import numpy as np
from PIL import Image
from image_data import update_output_image

def pseudocolor_spectrum(spectrum_label, bins_var):
    print(f"TODO: Implement Pseudo-color Spectrum with {bins_var.get()} bins")

    try:
        bins = int(bins_var.get())
        if bins < 2:
            bins = 2
    except ValueError:
        bins = 8  # default

        # ------------------------------------------
        # 2. Get CURRENT spectrum image (must be grayscale)
        # ------------------------------------------
    gray_pil = spectrum_label.pil_image.convert("L")
    gray = np.array(gray_pil, dtype=np.uint8)

    H, W = gray.shape

    # ------------------------------------------
    # 3. Create bin edges (0..255)
    # ------------------------------------------
    bin_edges = np.linspace(0, 255, bins + 1)

    # ------------------------------------------
    # 4. Choose a color map (per bin)
    # ------------------------------------------
    colormap = [
        (255, 0, 0),  # red
        (255, 165, 0),  # orange
        (255, 255, 0),  # yellow
        (0, 255, 0),  # green
        (0, 255, 255),  # cyan
        (0, 0, 255),  # blue
        (128, 0, 255),  # violet
        (255, 0, 255),  # magenta
    ]

    # If more bins than colors → extend by repeating last color
    while len(colormap) < bins:
        colormap.append(colormap[-1])

    # ------------------------------------------
    # 5. Create output color image
    # ------------------------------------------
    color_image = np.zeros((H, W, 3), dtype=np.uint8)

    for i in range(bins):
        low = bin_edges[i]
        high = bin_edges[i + 1]

        mask = (gray >= low) & (gray < high)
        color_image[mask] = colormap[i]

    # ------------------------------------------
    # 6. Update GUI
    # ------------------------------------------
    color_pil = Image.fromarray(color_image)
    update_output_image(spectrum_label, color_pil)

    print(f"Pseudo-color spectrum displayed using {bins} bins.")