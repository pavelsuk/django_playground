from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index. And it's located in pools2 directory!")

def hopla(request):
    return HttpResponse("Hopla lopla")
