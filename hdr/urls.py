from django.urls import path
from .views import process_hdr, gallery_view

urlpatterns = [
    path("", process_hdr, name="process_hdr"),  # <--- changed here
    path("gallery/", gallery_view, name="gallery"),
]
