from django.shortcuts import render, redirect
from .forms import LoginForm, RegistroAlumnoForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        print(form.errors)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            print(f"Usuario autenticado: {user.username}, Rol: {user.rol}")
            login(request, user)
            if user.rol == 'alumno':
                return redirect('home-alumno')
            elif user.rol == 'docente':
                return redirect('home-docente')
            else:
                return redirect('home-alumno')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registrar_alumno(request):
    if request.method == 'POST':
        form = RegistroAlumnoForm(request.POST)
        print(form.errors)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            user.rol = 'alumno'
            user.save()
            return redirect('login-alumno') 
    else:
        form = RegistroAlumnoForm()
    return render(request, 'registro.html', {'form': form})

def login_docente(request):
    if request.method == 'POST':
        form = DocenteLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                rol = user.rol
                print(rol)
                if user.rol == 'docente':
                    login(request, user)
                    return redirect('home-docente')
                else:
                    return redirect('home-docente')
    else:
        form = DocenteLoginForm()
    context = {
        'form': form
    }
    return render(request, 'usuarios/login/login_docente.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login-alumno')
