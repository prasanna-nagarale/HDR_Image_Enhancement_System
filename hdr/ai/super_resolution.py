from realesrgan import RealESRGAN
from PIL import Image

def enhance_image(image_path):
    model = RealESRGAN.from_pretrained('nateraw/real-esrgan').to("cuda")
    image = Image.open(image_path)
    enhanced = model.predict(image)
    enhanced_path = "media/enhanced_hdr.jpg"
    enhanced.save(enhanced_path)
    return enhanced_path
