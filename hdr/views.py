import cv2
import numpy as np
import rawpy
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import shutil
from datetime import datetime

def read_image(file_path):
    if file_path.lower().endswith(('.arw', '.dng', '.nef', '.cr2')):
        with rawpy.imread(file_path) as raw:
            rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, output_bps=8)
            img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            return None
        if img.dtype == np.uint16:
            img = (img / 256).astype(np.uint8)
        elif img.dtype in [np.float32, np.float64]:
            img = np.clip(img * 255, 0, 255).astype(np.uint8)

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img

def apply_hdr_merge_mertens(img_list):
    merge_mertens = cv2.createMergeMertens()
    fusion = merge_mertens.process(img_list)
    ldr = np.clip(fusion * 255, 0, 255).astype(np.uint8)
    return ldr

def final_enhancement_pipeline(image):
    image = image.astype(np.float32) / 255.0

    # Apply soft gamma to balance brightness
    image = np.power(image, 1 / 1.08)

    # Improve wall and floor tone with LAB CLAHE
    lab = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR).astype(np.float32) / 255.0

    # Reduce haloing/artifacts while keeping clarity
    image = cv2.bilateralFilter((image * 255).astype(np.uint8), d=9, sigmaColor=60, sigmaSpace=60)

    # Gentle vibrance and exposure compensation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] *= 1.04
    hsv[..., 2] *= 1.025
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0

    return np.clip(image * 255, 0, 255).astype(np.uint8)

def process_hdr(request):
    if request.method == "POST" and request.FILES.getlist("images"):
        images = request.FILES.getlist("images")

        if len(images) != 4:
            return render(request, "hdr_app/process.html", {
                "error_message": "Please upload exactly 4 images with different exposures (e.g., dark, medium-dark, medium, bright)."
            })

        img_list = []
        file_names = []

        for img_file in images:
            file_path = default_storage.save(f"tmp/{img_file.name}", ContentFile(img_file.read()))
            img = read_image(default_storage.path(file_path))
            if img is None:
                return JsonResponse({"error": f"Failed to load image: {img_file.name}"}, status=400)
            img_list.append(img)
            file_names.append(file_path)

        # Match shape to first image
        base_shape = img_list[0].shape[:2]
        img_list = [cv2.resize(img, (base_shape[1], base_shape[0]), interpolation=cv2.INTER_AREA) for img in img_list]

        merged_image = apply_hdr_merge_mertens(img_list)
        enhanced_image = final_enhancement_pipeline(merged_image)

        output_rel_path = "tmp/output_hdr.jpg"
        output_abs_path = os.path.join(settings.MEDIA_ROOT, output_rel_path)
        os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)
        cv2.imwrite(output_abs_path, enhanced_image)

        # Save to gallery
        gallery_dir = os.path.join(settings.MEDIA_ROOT, "gallery")
        os.makedirs(gallery_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        gallery_filename = f"hdr_{timestamp}.jpg"
        gallery_output_path = os.path.join(gallery_dir, gallery_filename)
        shutil.copy(output_abs_path, gallery_output_path)

        # Save resized preview
        resized_output_path = output_abs_path.replace("output_hdr.jpg", "resized_output_hdr.jpg")
        resized_img = cv2.resize(enhanced_image, (400, 300))
        cv2.imwrite(resized_output_path, resized_img)

        return render(request, "hdr_app/result.html", {
            "output_url": settings.MEDIA_URL + output_rel_path,
            "uploaded_images": file_names
        })

    return render(request, "hdr_app/process.html")

def gallery_view(request):
    gallery_dir = os.path.join(settings.MEDIA_ROOT, 'gallery')
    image_urls = []

    if os.path.exists(gallery_dir):
        for filename in os.listdir(gallery_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_urls.append(os.path.join(settings.MEDIA_URL, 'gallery', filename))

    return render(request, 'hdr_app/gallery.html', {'images': image_urls})
