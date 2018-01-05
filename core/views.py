from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def climate(request):
    return render(request, "core/climate.html")
