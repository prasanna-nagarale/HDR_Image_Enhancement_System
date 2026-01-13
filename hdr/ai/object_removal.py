from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image

pipe = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting").to("cuda")

def remove_objects(image_path, mask_path):
    img = Image.open(image_path)
    mask = Image.open(mask_path)
    output = pipe(image=img, mask_image=mask).images[0]
    output_path = "media/cleaned_hdr.jpg"
    output.save(output_path)
    return output_path
