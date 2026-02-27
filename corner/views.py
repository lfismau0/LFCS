from django.shortcuts import render
from .models import Corner


def corner_view(request, category):
    valid = {'student': 'Student Corner', 'teacher': 'Teacher Corner', 'parent': 'Parent Corner'}
    items = Corner.objects.filter(category=category)
    title = valid.get(category, 'Corner')
    return render(request, 'corner/corner.html', {'items': items, 'title': title, 'category': category})
