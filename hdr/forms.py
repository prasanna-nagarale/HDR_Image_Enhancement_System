from django import forms
from .models import HDRJob
from .models import UploadedImage

class HDRProcessingForm(forms.Form):
    """Form for HDR processing options."""
    auto_color_correction = forms.BooleanField(initial=True, required=False)
    denoising = forms.BooleanField(initial=True, required=False)
    sharpening = forms.BooleanField(initial=True, required=False)
    sky_replacement = forms.BooleanField(initial=False, required=False)
    
    OUTPUT_CHOICES = (
        ('jpg', 'JPG (Smallest file size)'),
        ('png', 'PNG (Better quality)'),
        ('tiff', 'TIFF (Highest quality)'),
    )
    output_format = forms.ChoiceField(choices=OUTPUT_CHOICES, initial='tiff')

# Move HDRImageForm outside of HDRProcessingForm
class HDRImageForm(forms.ModelForm):
    class Meta:
        model = HDRJob  # Assuming HDRJob stores the uploaded image
        fields = ['image']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']