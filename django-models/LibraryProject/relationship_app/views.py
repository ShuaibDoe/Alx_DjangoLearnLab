from django.shortcuts import render
from django.views.generic import DetailView
from .models import Library

# Class-based view for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

