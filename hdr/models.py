from django.db import models

class HDRImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name


class HDRJob(models.Model):  # Add HDRJob model if it was missing
    job_name = models.CharField(max_length=100)
    image = models.ForeignKey(HDRImage, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_name

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)