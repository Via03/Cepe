from django.shortcuts import render, redirect, get_object_or_404
from .models import Skill, Booking, User
from django.contrib.auth.decorators import login_required


# 🔷 Skill List (Homepage)
def skill_list(request):
    skills = Skill.objects.all()
    return render(request, 'skill_list.html', {'skills': skills})


# 🔷 Book Skill
@login_required
def book_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    # ❌ Prevent booking your own skill
    if request.user == skill.user:
        return redirect('skill_list')

    # ❌ Only clients can book
    if request.user.role != 'client':
        return redirect('skill_list')

    if request.method == 'POST':
        date = request.POST.get('date')

        if not date:
            return redirect('skill_list')

        Booking.objects.create(
            client=request.user,
            bayani=skill.user,
            skill=skill,
            date=date
        )

        return redirect('skill_list')

    return render(request, 'book_skill.html', {'skill': skill})


# 🔷 Main Dashboard Redirect
@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    elif request.user.role == 'bayani':
        return redirect('bayani_dashboard')

    else:
        return redirect('client_dashboard')


# 🔷 Client Dashboard
@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    bookings = request.user.client_bookings.all()

    return render(request, 'client_dashboard.html', {
        'bookings': bookings
    })


# 🔷 Bayani Dashboard
@login_required
def bayani_dashboard(request):
    if request.user.role != 'bayani':
        return redirect('dashboard')

    bookings = request.user.bayani_bookings.all()
    skills = request.user.skills.all()

    return render(request, 'bayani_dashboard.html', {
        'bookings': bookings,
        'skills': skills
    })


# 🔷 Admin Dashboard
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    return render(request, 'admin_dashboard.html', {
        'users': User.objects.all(),
        'skills': Skill.objects.all(),
        'bookings': Booking.objects.all(),
    })