from django.urls import path

from . import views

urlpatterns = [
    path('extractor/<int:ex_id>/', views.index),
]
