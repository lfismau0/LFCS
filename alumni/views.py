from django.shortcuts import render
from .models import Alumni


def alumni_list(request):
    batch = request.GET.get('batch', '')
    alumni = Alumni.objects.all()
    if batch:
        alumni = alumni.filter(batch=batch)
    batches = Alumni.objects.values_list('batch', flat=True).distinct().order_by('-batch')
    return render(request, 'alumni/alumni.html', {
        'alumni': alumni, 'batches': batches, 'selected_batch': batch
    })
