from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    index = "Hello, World !"
    return HttpResponse(index)
