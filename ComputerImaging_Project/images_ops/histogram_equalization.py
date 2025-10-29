"""
File Name:    histogram_equalization.py
Author(s):    Ju-ve Chankasemporn
Copyright:    (c) 2025 DigiPen Institute of Technology. All rights reserved.
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

def _histogram_equalizer(input_image, maxval=255):
    """Traditional method for histogram equalization.
        The result should be more equalized intensities
        on pixels of image"""

    if input_image.mode != 'L':
        input_image = input_image.convert('L')
    img_array = np.array(input_image)

    # calculate histogram
    hist, bins = np.histogram(img_array.flatten(), bins=maxval + 1, range=[0, maxval])

    # calculate CDF
    cdf = hist.cumsum()

    # normalize CDF to be in range [0, maxval]
    cdf_normalized = (cdf - cdf.min()) * maxval / (cdf.max() - cdf.min())
    cdf_normalized = cdf_normalized.astype('uint8')

    # apply histogram equalization mapping
    equalized_array = cdf_normalized[img_array]

    # convert back to PIL Image
    equalized_image = Image.fromarray(equalized_array)

    return equalized_image, hist, bins


def _plot_histograms(original_hist, equalized_hist, bins, maxval=255):
    """Plot original and equalized histograms side by side"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # plot original histogram
    ax1.bar(bins[:-1], original_hist, width=1, alpha=0.7, color='blue')
    ax1.set_title('Original Image Histogram')
    ax1.set_xlabel('Pixel Intensity')
    ax1.set_ylabel('Frequency')
    ax1.set_xlim(0, maxval)
    ax1.grid(True, alpha=0.3)

    # plot equalized histogram
    ax2.bar(bins[:-1], equalized_hist, width=1, alpha=0.7, color='red')
    ax2.set_title('Equalized Image Histogram')
    ax2.set_xlabel('Pixel Intensity')
    ax2.set_ylabel('Frequency')
    ax2.set_xlim(0, maxval)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def histogram_equalization(input_image, maxval=255, plot_histogram=True):
    """Apply traditional method for histogram equalization and plot the table"""
    equalized_image, original_hist, bins = _histogram_equalizer(input_image, maxval)

    # calculate histogram
    equalized_array = np.array(equalized_image)
    equalized_hist, _ = np.histogram(equalized_array.flatten(), bins=maxval + 1, range=[0, maxval])

    # plot the table
    fig = None
    if plot_histogram:
        fig = _plot_histograms(original_hist, equalized_hist, bins, maxval)
        plt.show()

    return equalized_image, fig

def histogram_equalization_opencv(input_image, maxval=255, plot_histogram=True):
    """Histogram equalization using OpenCV for comparison"""
    if input_image.mode != 'L':
        input_image = input_image.convert('L')
    img_array = np.array(input_image)

    # apply OpenCV histogram equalization
    equalized_array = cv2.equalizeHist(img_array)

    equalized_image = Image.fromarray(equalized_array)

    # calculate histograms
    original_hist, bins = np.histogram(img_array.flatten(), bins=maxval + 1, range=[0, maxval])
    equalized_hist, _ = np.histogram(equalized_array.flatten(), bins=maxval + 1, range=[0, maxval])

    #  plot the table
    fig = None
    if plot_histogram:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

        # plot original histogram
        ax1.bar(bins[:-1], original_hist, width=1, alpha=0.7, color='blue')
        ax1.set_title('Original Image Histogram')
        ax1.set_xlabel('Pixel Intensity')
        ax1.set_ylabel('Frequency')
        ax1.set_xlim(0, maxval)
        ax1.grid(True, alpha=0.3)

        # plot traditional equalized histogram for comparison
        custom_equalized, _, _ = _histogram_equalizer(input_image, maxval)
        custom_array = np.array(custom_equalized)
        custom_hist, _ = np.histogram(custom_array.flatten(), bins=maxval + 1, range=[0, maxval])
        ax2.bar(bins[:-1], custom_hist, width=1, alpha=0.7, color='green')
        ax2.set_title('Standard Equalized Histogram')
        ax2.set_xlabel('Pixel Intensity')
        ax2.set_ylabel('Frequency')
        ax2.set_xlim(0, maxval)
        ax2.grid(True, alpha=0.3)

        # plot OpenCV equalized histogram
        ax3.bar(bins[:-1], equalized_hist, width=1, alpha=0.7, color='red')
        ax3.set_title('OpenCV Equalized Histogram')
        ax3.set_xlabel('Pixel Intensity')
        ax3.set_ylabel('Frequency')
        ax3.set_xlim(0, maxval)
        ax3.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    return equalized_image, fig


