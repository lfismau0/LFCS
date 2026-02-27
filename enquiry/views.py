from django.shortcuts import render, redirect
from .forms import EnquiryForm, CareerForm


def enquiry_view(request):
    form = EnquiryForm()
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'enquiry/enquiry.html', {'form': EnquiryForm(), 'success': True})
    return render(request, 'enquiry/enquiry.html', {'form': form})


def career_view(request):
    form = CareerForm()
    if request.method == 'POST':
        form = CareerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'enquiry/career.html', {'form': CareerForm(), 'success': True})
    return render(request, 'enquiry/career.html', {'form': form})
