import cv2
from skyar import SkyAR

def replace_sky(input_image, new_sky):
    skyar = SkyAR()
    img = cv2.imread(input_image)
    sky = cv2.imread(new_sky)
    output = skyar.replace_sky(img, sky)
    output_path = "media/hdr_with_sky.jpg"
    cv2.imwrite(output_path, output)
    return output_path
