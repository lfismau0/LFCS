from django.shortcuts import render
from .models import Staff


def staff_list(request):
    department = request.GET.get('department', '')
    staff = Staff.objects.all()
    if department:
        staff = staff.filter(department=department)
    departments = Staff.DEPARTMENT_CHOICES
    return render(request, 'staff/staff.html', {
        'staff': staff, 'departments': departments, 'selected_dept': department
    })
