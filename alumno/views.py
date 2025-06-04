from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.decorators import rol_requerido
<<<<<<< Updated upstream
from .models import Perfil_alumno, Proyecto, ProyectoRequest
from .forms import PerfilForm, ProyectoForm
from administrador.models import Track, TrackRequest
from django.shortcuts import get_object_or_404
from django.contrib import messages
from docente.models import DocentePost
from administrador.models import ReunionTrack
=======
from .models import Perfil_alumno, Proyecto
from .forms import PerfilForm, ProyectoForm
>>>>>>> Stashed changes

#Home

@login_required
@rol_requerido('alumno')
def home_view(request):
    return render(request, 'home_alumno.html')

#Perfil

@login_required
@rol_requerido('alumno')
def editar_perfil(request):
    try:
        perfil = Perfil_alumno.objects.get(alumno=request.user)
    except Perfil_alumno.DoesNotExist:
        return redirect('perfil-alumno')

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('home-alumno') 
    else:
        form = PerfilForm(instance=perfil)

    context = {
        'form': form,
    }
    return render(request, 'perfil/editar_perfil.html', context)

#Proyectos

@login_required
@rol_requerido('alumno')
def listar_proyectos(request):
<<<<<<< Updated upstream
    track_id = request.user.id_track
    proyectos = Proyecto.objects.filter(jefe_proyecto=request.user.perfil_alumno, id_track=track_id)
    context = {'proyectos':proyectos, 'track_id': track_id}
    return render(request,'mis-proyectos/crud/listar_proyectos.html',context)
=======
    proyectos = Proyecto.objects.all()
    context = {'proyectos':proyectos}
    return render(request,'proyectos/listar_proyectos.html',context)
>>>>>>> Stashed changes

@login_required
@rol_requerido('alumno')
def añadir_proyecto(request):
<<<<<<< Updated upstream
    track_id = request.user.id_track
=======
>>>>>>> Stashed changes
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.jefe_proyecto = request.user.perfil_alumno
<<<<<<< Updated upstream
            proyecto.track_id = track_id
            proyecto.save()
            return redirect('listar-proyectos') 
    else:
        form = ProyectoForm()
=======
            proyecto.save()
            return redirect('listar-proyectos') 
    else:
        form = ProyectoForm(instance=request.user) 
>>>>>>> Stashed changes

    context = {
        'form': form,
    }
<<<<<<< Updated upstream
    return render(request, 'mis-proyectos/crud/crear_proyecto.html', context)

=======
    return render(request, 'proyectos/crear_proyecto.html', context)
>>>>>>> Stashed changes

@login_required
@rol_requerido('alumno')
def modificar_proyecto(request,pk):
    try:
        proyecto = Proyecto.objects.get(id_proyecto = pk)
        if proyecto:
            if request.method == 'POST':
                form = ProyectoForm(request.POST,instance=proyecto)
                form.save()
                return redirect('listar-proyectos')
            else:
                form = ProyectoForm(instance=proyecto)
                context={'form':form}
<<<<<<< Updated upstream
                return render(request,'mis-proyectos/crud/modificar_proyecto.html',context)
=======
                return render(request,'proyectos/modificar_proyecto.html',context)
>>>>>>> Stashed changes
    except:
        return redirect('listar-proyectos')
    
@login_required
@rol_requerido('alumno')
def eliminar_proyecto(request,pk):
    try:
        mensajes=[]
        proyecto = Proyecto.objects.get(id_proyecto = pk)
        if proyecto:
            proyecto.delete()
            mensajes.append('Proyecto eliminado satisfactoriamente')
            return redirect('listar-proyectos')
    except:
        return redirect('listar-proyectos')

# Vistas para los tracks

def robotica_view(request):
<<<<<<< Updated upstream
    track_id = 1  # esta hardcodeado mientras se testea XD
    solicitud_pendiente = False
    boton_solicitud = True

    if request.user.id_track:
        boton_solicitud = False

    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()

    track = Track.objects.filter(id_track=track_id).first()
    posts = DocentePost.objects.filter(track=track).order_by('-fecha_creacion') if track else []
    proyectos = Proyecto.objects.filter(id_track=track) if track else []
    alumnos = Perfil_alumno.objects.filter(alumno__id_track=track) if track else []
    reuniones = ReunionTrack.objects.filter(track=track) if track else []

    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
        'track': track,
        'posts': posts,
        'proyectos': proyectos,
        'alumnos': alumnos,
        'reuniones': reuniones,
    }
    return render(request, 'tracks/home_track/robotica-home.html', context)

def unirse_a_track(request, track_id):
    if request.method == 'POST' and request.user.rol == 'alumno':
        track = get_object_or_404(Track, id_track=track_id)

        solicitud_existente = TrackRequest.objects.filter(
            track=track,
            alumno=request.user,
            estado='pendiente'
        ).exists()

        if not solicitud_existente:
            TrackRequest.objects.create(track=track, alumno=request.user)

    return redirect(request.META.get('HTTP_REFERER', 'home-alumno'))

def ciberseguridad_view(request):
    track_id = 2  # esta hardcodeado mientras se testea XD
    solicitud_pendiente = False
    boton_solicitud = True

    if request.user.id_track:
        boton_solicitud = False

    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()

    track = Track.objects.filter(id_track=track_id).first()
    posts = DocentePost.objects.filter(track=track).order_by('-fecha_creacion') if track else []
    proyectos = Proyecto.objects.filter(id_track=track) if track else []
    alumnos = Perfil_alumno.objects.filter(alumno__id_track=track) if track else []
    reuniones = ReunionTrack.objects.filter(track=track) if track else []

    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
        'track': track,
        'posts': posts,
        'proyectos': proyectos,
        'alumnos': alumnos,
        'reuniones': reuniones,
    }
    return render(request, 'tracks/home_track/ciberseguridad-home.html', context)

def lista_proyectos_citt(request, track_id):
    solicitud_pendiente = False
    boton_solicitud = True

    if request.user.id_track:
        boton_solicitud = False

    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()

    track = Track.objects.filter(id_track=track_id).first()
    posts = DocentePost.objects.filter(track=track).order_by('-fecha_creacion') if track else []
    proyectos = Proyecto.objects.filter(id_track=track) if track else []
    alumnos = Perfil_alumno.objects.filter(alumno__id_track=track) if track else []
    reuniones = ReunionTrack.objects.filter(track=track) if track else []

    # Obtener IDs de proyectos con solicitud pendiente del usuario
    solicitudes_proyectos = ProyectoRequest.objects.filter(
        alumno=request.user, estado='pendiente', proyecto__in=proyectos
    ).values_list('proyecto_id', flat=True)

    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
        'track': track,
        'posts': posts,
        'proyectos': proyectos,
        'alumnos': alumnos,
        'reuniones': reuniones,
        'proyectos_solicitados': set(solicitudes_proyectos),  # Usamos un set para eficiencia
    }

    return render(request, 'tracks/proyectos/lista_proyectos.html', context)

@login_required
@rol_requerido('alumno')
def solicitar_ingreso_proyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    
    if ProyectoRequest.objects.filter(proyecto=proyecto, alumno=request.user, estado='pendiente').exists():
        messages.warning(request, "Ya enviaste una solicitud a este proyecto.")
    else:
        ProyectoRequest.objects.create(proyecto=proyecto, alumno=request.user)
        messages.success(request, "Solicitud enviada correctamente.")
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@rol_requerido('alumno')
def gestionar_solicitudes_proyecto(request):
    perfil = request.user.perfil_alumno
    proyectos = Proyecto.objects.filter(jefe_proyecto=perfil)
    solicitudes = ProyectoRequest.objects.filter(proyecto__in=proyectos, estado='pendiente')

    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        accion = request.POST.get('accion')
        solicitud = get_object_or_404(ProyectoRequest, id_solicitud=solicitud_id, proyecto__in=proyectos)

        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'

        solicitud.save()
        messages.success(request, f'Solicitud {accion}ada correctamente.')

        return redirect('gestionar-solicitudes-proyecto')

    return render(request, 'mis-proyectos/solicitudes/solicitudes_proyecto.html', {
        'solicitudes': solicitudes
    })

def bigdata_view(request):
    track_id = 2  # Asume el ID de Big Data es 2
    solicitud_pendiente = False
    boton_solicitud = True
    if request.user.id_track:
        boton_solicitud = False
    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()
    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
    }
    return render(request, 'tracks/home_track/bigdata-home.html', context)

def videojuegos_view(request):
    track_id = 3  # Asume el ID de Videojuegos es 3
    solicitud_pendiente = False
    boton_solicitud = True
    if request.user.id_track:
        boton_solicitud = False
    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()
    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
    }
    return render(request, 'tracks/home_track/videojuegos-home.html', context)

def machinelearning_view(request):
    track_id = 4  # Asume el ID de Machine Learning es 4
    solicitud_pendiente = False
    boton_solicitud = True
    if request.user.id_track:
        boton_solicitud = False
    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()
    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
    }
    return render(request, 'tracks/home_track/machinelearning-home.html', context)

def realidadvirtual_view(request):
    track_id = 5  # Asume el ID de Realidad Virtual es 5
    solicitud_pendiente = False
    boton_solicitud = True
    if request.user.id_track:
        boton_solicitud = False
    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()
    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
    }
    return render(request, 'tracks/home_track/realidadvirtual-home.html', context)

def appmovilweb_view(request):
    track_id = 7  # Asume el ID de App Móvil & Web es 7
    solicitud_pendiente = False
    boton_solicitud = True
    if request.user.id_track:
        boton_solicitud = False
    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()
    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
    }
    return render(request, 'tracks/home_track/appmovilweb-home.html', context)

def iot_view(request):
    track_id = 8  # Asume el ID de IoT es 8
    solicitud_pendiente = False
    boton_solicitud = True
    if request.user.id_track:
        boton_solicitud = False
    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()
    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
    }
    return render(request, 'tracks/home_track/iot-home.html', context)

def drones_view(request):
    track_id = 9  # Asume el ID de Drones es 9
    solicitud_pendiente = False
    boton_solicitud = True
    if request.user.id_track:
        boton_solicitud = False
    if request.user.is_authenticated and request.user.rol == 'alumno':
        solicitud_pendiente = TrackRequest.objects.filter(
            track=track_id,
            alumno=request.user,
            estado='pendiente'
        ).exists()
    context = {
        'track_id': track_id,
        'solicitud_pendiente': solicitud_pendiente,
        'boton_solicitud': boton_solicitud,
    }
    return render(request, 'tracks/home_track/drones-home.html', context)

def error_view(request):
    context = {
        'error_message': 'No tienes permisos para acceder a esta página.',
    }
    return render(request, 'error.html', context)
=======
    return render(request, 'tracks/home_track/robotica-home.html')

def ciberseguridad_view(request):
    return render(request, 'tracks/home_track/ciberseguridad-home.html')
>>>>>>> Stashed changes
