from django import forms
from .models import Enquiry, CareerApplication


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone', 'email', 'message', 'class_interested']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'}),
            'class_interested': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class Interested For'}),
        }


class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerApplication
        fields = ['name', 'qualification', 'experience', 'resume_upload', 'phone', 'email', 'applied_for']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Highest Qualification'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'applied_for': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position Applied For'}),
            'resume_upload': forms.FileInput(attrs={'class': 'form-control'}),
        }
