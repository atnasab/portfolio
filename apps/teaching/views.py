from django.shortcuts import render, get_object_or_404
from .models import Subject


def subject_list(request):
    active = Subject.objects.filter(is_active=True).order_by("order")
    past = Subject.objects.filter(is_active=False).order_by("-academic_year")
    return render(request, "teaching/list.html", {
        "active_subjects": active,
        "past_subjects": past,
    })


def subject_detail(request, slug):
    subject = get_object_or_404(Subject, slug=slug)
    return render(request, "teaching/detail.html", {"subject": subject})
