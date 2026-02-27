from django.shortcuts import render
from .models import TC


def tc_search(request):
    result = None
    not_found = False
    query = request.GET.get('admission_no', '').strip()
    if query:
        try:
            result = TC.objects.get(admission_no=query)
        except TC.DoesNotExist:
            not_found = True
    return render(request, 'tc/tc_search.html', {
        'result': result, 'not_found': not_found, 'query': query
    })
