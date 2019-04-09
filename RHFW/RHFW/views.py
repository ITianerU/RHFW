from django.shortcuts import render
# Create your views here.
from .forms import JobForm

def search(request):
    form = JobForm()
    return render(request, "search.html", {"form": form})
