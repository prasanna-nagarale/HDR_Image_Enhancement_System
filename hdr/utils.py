import cv2
import numpy as np
import rawpy
from PIL import Image

def get_exposure_time(image_path):
    """ Extracts exposure time from image metadata. """
    try:
        with rawpy.imread(image_path) as raw:
            metadata = raw.metadata
            return metadata.shutter  # Extract exposure time
    except:
        return None  # Return None if metadata is missing

def load_images(image_paths):
    """ Load images as 32-bit float for HDR processing. """
    img_list = []
    exposure_times = []
    
    for path in image_paths:
        exposure = get_exposure_time(path) or 1/60  # Default exposure
        exposure_times.append(exposure)
        
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED).astype(np.float32) / 255.0
        img_list.append(img)
    
    return img_list, np.array(exposure_times, dtype=np.float32)

def process_hdr(image_paths):
    img_list = []
    
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"Error loading image: {path}")
        else:
            img_list.append(img)

    print(f"Loaded {len(img_list)} images for HDR processing.")

    if len(img_list) < 3:
        raise ValueError("Not enough valid images loaded for HDR.")

    exposure_times = np.array([1/1000, 1/250, 1/60], dtype=np.float32)

    assert len(img_list) == len(exposure_times), "Number of images must match number of exposure times."

    merge_debevec = cv2.createMergeDebevec()
    hdr_image = merge_debevec.process(img_list, times=exposure_times)

    if hdr_image is None:
        raise ValueError("HDR image creation failed.")

    return hdr_image, None


