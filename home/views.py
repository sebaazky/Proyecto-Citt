from django.shortcuts import render

# Create your views here.

def inicio(request):
    context={}
    return render(request,'usuarios/home-citt/index.html',context)

def proyectos(request):
    context={}
    return render(request,'usuarios/home-citt/proyecto.html',context)

def track(request):
    context={}
    return render(request,'usuarios/home-citt/track.html',context)

