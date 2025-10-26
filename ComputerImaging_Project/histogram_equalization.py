from PIL import Image
import numpy as np

def histogram_equalizer(input_image, maxval=255):

    #setup
    if input_image.mode != 'L':
        input_image = input_image.convert('L')
    img_array = np.array(input_image)

    #calculate histogram
    hist, bins = np.histogram(img_array.flatten(), bins=maxval + 1, range=[0, maxval])

    #calculate CDF
    cdf = hist.cumsum()

    #normalize CDF to be in range [0, maxval]
    cdf_normalized = (cdf - cdf.min()) * maxval / (cdf.max() - cdf.min())
    cdf_normalized = cdf_normalized.astype('uint8')

    #apply histogram equalization mapping
    equalized_array = cdf_normalized[img_array]

    #convert back to PIL Image
    equalized_image = Image.fromarray(equalized_array)

    return equalized_image