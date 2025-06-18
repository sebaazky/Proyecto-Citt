from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from login.decorators import rol_requerido
from .models import Perfil_alumno, Proyecto, ProyectoRequest, Solicitud, ProyectoPost, ReunionProyecto, IntegranteProyecto
from .forms import PerfilForm, ProyectoForm, SolicitudForm, ProyectoPostForm, ReunionProyectoForm
from administrador.models import Track, ReunionTrack,  TrackRequest
from docente.models import TrackPost, Evento
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator


# Home


@login_required
@rol_requerido('alumno')
def home_view(request):
    perfil = Perfil_alumno.objects.filter(alumno=request.user).first()
    # Onboarding: Si el alumno no ha completado el flujo, redirigir
    paso = None
    if perfil is None or not (perfil.nombres and perfil.apellido_paterno):
        paso = 1
    else:
        solicitud = TrackRequest.objects.filter(alumno=request.user).order_by('-fecha_solicitud').first()
        if not solicitud:
            paso = 2
        elif solicitud.estado == 'pendiente':
            paso = 3
        elif solicitud.estado == 'aprobada':
            paso = 4
        else:
            paso = 2
    if paso and paso < 4:
        return redirect('flujo-onboarding')
    context = {
        'perfil_alumno': perfil,
    }
    return render(request, 'home_alumno.html', context)

# Perfil


@login_required
@rol_requerido('alumno')
def ver_perfil(request):
    perfil = get_object_or_404(Perfil_alumno, alumno=request.user)
    return render(request, 'perfil/ver_perfil.html', {'perfil': perfil})


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

    context = {'form': form}
    return render(request, 'perfil/editar_perfil.html', context)

# Proyectos


@login_required
@rol_requerido('alumno')
def listar_proyectos(request):
    track_id = request.user.id_track
    proyectos = Proyecto.objects.filter(
        jefe_proyecto=request.user, id_track=track_id)
    context = {'proyectos': proyectos, 'track_id': track_id}
    return render(request, 'proyectos/listar_proyectos.html', context)


@login_required
@rol_requerido('alumno')
def añadir_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.jefe_proyecto = request.user
            proyecto.id_track = request.user.id_track
            proyecto.fecha_inicio = timezone.now().date()
            proyecto.save()
            return redirect('listar-proyectos')
    else:
        form = ProyectoForm()

    return render(request, 'proyectos/crear_proyecto.html', {'form': form})


@login_required
@rol_requerido('alumno')
def modificar_proyecto(request, pk):
    try:
        proyecto = Proyecto.objects.get(id_proyecto=pk)
        if request.method == 'POST':
            form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
            if form.is_valid():
                form.save()
                return redirect('listar-proyectos')
        else:
            form = ProyectoForm(instance=proyecto)
        context = {'form': form}
        return render(request, 'proyectos/modificar_proyecto.html', context)
    except Proyecto.DoesNotExist:
        return redirect('listar-proyectos')


# Unirse a track


@login_required
@rol_requerido('alumno')
def unirse_a_track(request, track_id):
    if request.method == 'POST':
        track = get_object_or_404(Track, id_track=track_id)
        if not TrackRequest.objects.filter(track=track, alumno=request.user, estado='pendiente').exists():
            TrackRequest.objects.create(track=track, alumno=request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home-alumno'))

# Listar proyectos del track


@login_required
@rol_requerido('alumno')
def lista_proyectos_citt(request, track_id):
    track = get_object_or_404(Track, id_track=track_id)
    proyectos = Proyecto.objects.filter(id_track=track)
    solicitudes_proyectos = ProyectoRequest.objects.filter(
        alumno=request.user, estado='pendiente', proyecto__in=proyectos
    ).values_list('proyecto_id', flat=True)

    context = {
        'track_id': track_id,
        'track': track,
        'proyectos': proyectos,
        'proyectos_solicitados': set(solicitudes_proyectos),
    }
    return render(request, 'tracks/proyectos/lista_proyectos.html', context)

# Solicitar ingreso a proyecto



# Gestionar solicitudes de proyectos


@login_required
@rol_requerido('alumno')
def gestionar_solicitudes_proyecto(request):
    perfil = request.user.perfil_alumno
    proyectos = Proyecto.objects.filter(jefe_proyecto=perfil)
    solicitudes = ProyectoRequest.objects.filter(
        proyecto__in=proyectos, estado='pendiente')

    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        accion = request.POST.get('accion')
        solicitud = get_object_or_404(
            ProyectoRequest, id_solicitud=solicitud_id, proyecto__in=proyectos)

        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'

        solicitud.save()
        messages.success(request, f'Solicitud {solicitud.estado} correctamente.')
        return redirect('gestionar-solicitudes-proyecto-alumno')

    return render(request, 'mis-proyectos/solicitudes/solicitudes_proyecto.html', {'solicitudes': solicitudes})

# Vista dinámica del detalle del track


@login_required
@rol_requerido('alumno')
def detalle_track_view(request, slug):
    track = get_object_or_404(Track, nom_track__iexact=slug.replace('-', ' '))

    # Solicitud pendiente para este track
    solicitud_en_este_track = TrackRequest.objects.filter(
        track=track, alumno=request.user, estado='pendiente'
    ).exists()

    # Solicitud pendiente en otro track
    solicitud_en_otro_track = TrackRequest.objects.filter(
        alumno=request.user, estado='pendiente'
    ).exclude(track=track).exists()

    # Mostrar botón solo si no tiene track asignado y no tiene solicitudes pendientes
    mostrar_boton_solicitud = not request.user.id_track and not solicitud_en_este_track and not solicitud_en_otro_track

    posts = TrackPost.objects.filter(track=track).order_by('-fecha_creacion')
    proyectos = Proyecto.objects.filter(id_track=track)
    alumnos = Perfil_alumno.objects.filter(alumno__id_track=track).select_related('alumno')
    reuniones = ReunionTrack.objects.filter(track=track)

    proyectos_info = []
    for proyecto in proyectos:
        es_jefe = request.user == proyecto.jefe_proyecto
        es_integrante = es_jefe or proyecto.integrantes.filter(alumno=request.user).exists()
        solicitud_proyecto_pendiente = ProyectoRequest.objects.filter(proyecto=proyecto, alumno=request.user, estado='pendiente').exists()
        puede_solicitar = not es_integrante and not solicitud_proyecto_pendiente
        proyectos_info.append({
            'proyecto': proyecto,
            'es_jefe': es_jefe,
            'es_integrante': es_integrante,
            'solicitud_pendiente': solicitud_proyecto_pendiente,
            'puede_solicitar': puede_solicitar,
        })

    proyectos_carrusel = [info for info in proyectos_info if info['puede_solicitar']]

    context = {
        'track': track,
        'mostrar_boton_solicitud': mostrar_boton_solicitud,
        'solicitud_en_este_track': solicitud_en_este_track,
        'solicitud_en_otro_track': solicitud_en_otro_track,
        'posts': posts,
        'proyectos_info': proyectos_info,
        'proyectos_carrusel': proyectos_carrusel,
        'alumnos': alumnos,
        'reuniones': reuniones,
    }
    return render(request, 'tracks/home_track/detalle_track.html', context)
    

@login_required
@rol_requerido('alumno')
def reuniones_alumno_view(request):
    if _alumno_onboarding_incompleto(request):
        return HttpResponseForbidden('Debes completar el onboarding para acceder a esta sección.')
    track = request.user.id_track  # Asumimos que el alumno tiene asignado un track
    reuniones = ReunionTrack.objects.filter(track=track).order_by('-fecha')

    context = {
        'reuniones': reuniones,
    }
    return render(request, 'reuniones/reuniones_alumno.html', context)


@login_required
@rol_requerido('alumno')
def eventos_track_view(request):
    if _alumno_onboarding_incompleto(request):
        return HttpResponseForbidden('Debes completar el onboarding para acceder a esta sección.')
    eventos = Evento.objects.all().order_by(
        '-fecha_evento')  # ✅ Sin filtro por track

    context = {
        'eventos': eventos,
    }
    return render(request, 'eventos/lista_eventos.html', context)


@login_required
@rol_requerido('alumno')
def listar_solicitudes_citt(request):
    if _alumno_onboarding_incompleto(request):
        return HttpResponseForbidden('Debes completar el onboarding para acceder a esta sección.')
    solicitudes = Solicitud.objects.filter(
        alumno=request.user).order_by('-fecha_creacion')
    return render(request, 'solicitudes/listar.html', {'solicitudes': solicitudes})


@login_required
@rol_requerido('alumno')
def crear_solicitud_citt(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.alumno = request.user
            solicitud.save()
            return redirect('listar-solicitudes')
    else:
        form = SolicitudForm()
    return render(request, 'solicitudes/crear.html', {'form': form})


@login_required
@rol_requerido('alumno')
def modificar_solicitud_citt(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk, alumno=request.user)
    if solicitud.estado != 'pendiente':
        return redirect('listar-solicitudes')

    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('listar-solicitudes')
    else:
        form = SolicitudForm(instance=solicitud)
    return render(request, 'solicitudes/modificar.html', {'form': form})

# Flujo Onboarding


@login_required
def flujo_onboarding(request):
    user = request.user
    try:
        perfil = user.perfil_alumno
        tiene_perfil = perfil.nombres and perfil.apellido_paterno
    except Perfil_alumno.DoesNotExist:
        tiene_perfil = False
    if not tiene_perfil:
        paso = 1
    else:
        solicitud = TrackRequest.objects.filter(alumno=user).order_by('-fecha_solicitud').first()
        if not solicitud:
            paso = 2
        elif solicitud.estado == 'pendiente':
            paso = 3
        elif solicitud.estado == 'aprobada':
            paso = 4
        else:
            paso = 2
    # Si ya completó el onboarding, redirigir a home normal
    if paso == 4:
        return redirect('home-alumno')
    return render(request, 'flujo_onboarding.html', {'paso': paso})

@login_required
@rol_requerido('alumno')
def listar_tracks(request):
    tracks = Track.objects.all()
    return render(request, 'listar_tracks.html', {'tracks': tracks})

@login_required
@rol_requerido('alumno')
def _alumno_onboarding_incompleto(request):
    try:
        perfil = request.user.perfil_alumno
        tiene_perfil = perfil.nombres and perfil.apellido_paterno
    except Exception:
        return True
    from administrador.models import TrackRequest  # Corregido: importar desde administrador
    solicitud = TrackRequest.objects.filter(alumno=request.user).order_by('-fecha_solicitud').first()
    if not tiene_perfil or not solicitud or solicitud.estado != 'aprobada':
        return True
    return False

@login_required
@rol_requerido('alumno')
def home_proyecto_view(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    posts = ProyectoPost.objects.filter(proyecto=proyecto).order_by('-fecha_creacion')
    integrantes = IntegranteProyecto.objects.filter(proyecto=proyecto).select_related('alumno')
    es_jefe = request.user == proyecto.jefe_proyecto
    es_integrante = es_jefe or integrantes.filter(alumno=request.user).exists()
    puede_solicitar = not es_integrante and not ProyectoRequest.objects.filter(proyecto=proyecto, alumno=request.user, estado='pendiente').exists()
    solicitud_pendiente = ProyectoRequest.objects.filter(proyecto=proyecto, alumno=request.user, estado='pendiente').exists()

    # Paginación de reuniones
    reuniones = ReunionProyecto.objects.filter(proyecto=proyecto).order_by('-fecha')
    page_number = request.GET.get('page', 1)
    if request.GET.get('seccion') == 'reuniones':
        paginator = Paginator(reuniones, 5)
        reuniones_paginadas = paginator.get_page(page_number)
    else:
        reuniones_paginadas = None

    # Solicitudes solo si es jefe y está en la sección
    solicitudes = []
    if es_jefe and request.GET.get('seccion') == 'solicitudes':
        solicitudes = ProyectoRequest.objects.filter(proyecto=proyecto, estado='pendiente').order_by('-fecha_solicitud')

    context = {
        'proyecto': proyecto,
        'posts': posts,
        'reuniones': reuniones,
        'reuniones_paginadas': reuniones_paginadas,
        'integrantes': integrantes,
        'es_jefe': es_jefe,
        'es_integrante': es_integrante,
        'puede_solicitar': puede_solicitar,
        'solicitud_pendiente': solicitud_pendiente,
        'post_form': ProyectoPostForm(),
        'reunion_form': ReunionProyectoForm(),
        'solicitudes': solicitudes,
    }
    return render(request, 'proyectos/home_proyecto.html', context)

@login_required
@rol_requerido('alumno')
def crear_post_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    if not (request.user == proyecto.jefe_proyecto or IntegranteProyecto.objects.filter(proyecto=proyecto, alumno=request.user).exists()):
        return HttpResponseForbidden('No tienes permiso para publicar en este proyecto.')
    if request.method == 'POST':
        form = ProyectoPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.proyecto = proyecto
            post.autor = request.user
            post.save()
            messages.success(request, 'Post creado correctamente.')
    return redirect('home-proyecto-alumno', proyecto_id=proyecto_id)

@login_required
@rol_requerido('alumno')
def crear_reunion_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    if request.user != proyecto.jefe_proyecto:
        return HttpResponseForbidden('Solo el jefe de proyecto puede crear reuniones.')
    if request.method == 'POST':
        form = ReunionProyectoForm(request.POST)
        if form.is_valid():
            reunion = form.save(commit=False)
            reunion.proyecto = proyecto
            reunion.save()
            messages.success(request, 'Reunión creada correctamente.')
    return redirect('home-proyecto-alumno', proyecto_id=proyecto_id)

@login_required
@rol_requerido('alumno')
def solicitar_ingreso_proyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    if ProyectoRequest.objects.filter(proyecto=proyecto, alumno=request.user, estado='pendiente').exists():
        messages.warning(request, "Ya enviaste una solicitud a este proyecto.")
    else:
        ProyectoRequest.objects.create(proyecto=proyecto, alumno=request.user)
        messages.success(request, "Solicitud enviada correctamente.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@rol_requerido('alumno')
def gestionar_solicitudes_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    if request.user != proyecto.jefe_proyecto:
        return HttpResponseForbidden('Solo el jefe de proyecto puede gestionar solicitudes.')
    solicitudes = ProyectoRequest.objects.filter(proyecto=proyecto, estado='pendiente')
    return render(request, 'proyectos/solicitudes_proyecto.html', {'proyecto': proyecto, 'solicitudes': solicitudes})

@login_required
@rol_requerido('alumno')
def aceptar_solicitud_proyecto(request, proyecto_id, solicitud_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    solicitud = get_object_or_404(ProyectoRequest, id_solicitud=solicitud_id, proyecto=proyecto)

    if request.user != proyecto.jefe_proyecto:
        return HttpResponseForbidden('Solo el jefe de proyecto puede aceptar solicitudes.')

    solicitud.estado = 'aprobada'
    solicitud.save()

    IntegranteProyecto.objects.get_or_create(proyecto=proyecto, alumno=solicitud.alumno)

    ProyectoRequest.objects.filter(
        proyecto=proyecto, alumno=solicitud.alumno
    ).exclude(id_solicitud=solicitud_id).update(estado='rechazada')

    messages.success(request, 'Solicitud aceptada y alumno agregado al proyecto.')

    # Redirige a la misma página desde donde vino el request
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@rol_requerido('alumno')
def rechazar_solicitud_proyecto(request, proyecto_id, solicitud_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    solicitud = get_object_or_404(ProyectoRequest, id_solicitud=solicitud_id, proyecto=proyecto)
    if request.user != proyecto.jefe_proyecto:
        return HttpResponseForbidden('Solo el jefe de proyecto puede rechazar solicitudes.')
    solicitud.estado = 'rechazada'
    solicitud.save()
    messages.info(request, 'Solicitud rechazada.')
    return redirect('gestionar-solicitudes-proyecto-alumno', proyecto_id=proyecto_id)

@login_required
@rol_requerido('alumno')
def cancelar_solicitud_proyecto(request, id_proyecto):
    """
    Permite a un alumno cancelar su solicitud pendiente a un proyecto.
    """
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    solicitud = ProyectoRequest.objects.filter(proyecto=proyecto, alumno=request.user, estado='pendiente').first()
    if solicitud:
        solicitud.delete()
        messages.success(request, 'Solicitud cancelada correctamente.')
    else:
        messages.warning(request, 'No tienes una solicitud pendiente para este proyecto.')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@rol_requerido('alumno')
def modificar_post_proyecto(request, proyecto_id, post_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    post = get_object_or_404(ProyectoPost, id_post=post_id, proyecto=proyecto)
    if request.user != proyecto.jefe_proyecto:
        return HttpResponseForbidden('Solo el jefe de proyecto puede modificar posts.')
    if request.method == 'POST':
        form = ProyectoPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post modificado correctamente.')
            return redirect('home-proyecto-alumno', proyecto_id=proyecto_id)
    else:
        form = ProyectoPostForm(instance=post)
    return render(request, 'proyectos/modificar_post_proyecto.html', {'form': form, 'post': post, 'proyecto': proyecto})

@login_required
@rol_requerido('alumno')
def eliminar_post_proyecto(request, proyecto_id, post_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    post = get_object_or_404(ProyectoPost, id_post=post_id, proyecto=proyecto)
    if request.user != proyecto.jefe_proyecto:
        return HttpResponseForbidden('Solo el jefe de proyecto puede eliminar posts.')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post eliminado correctamente.')
        return redirect('home-proyecto-alumno', proyecto_id=proyecto_id)
    return render(request, 'proyectos/eliminar_post_proyecto.html', {'post': post, 'proyecto': proyecto})

@login_required
@rol_requerido('alumno')
def modificar_reunion_proyecto_alumno(request, proyecto_id, reunion_id):
    reunion = get_object_or_404(ReunionProyecto, id_reunion=reunion_id, proyecto_id=proyecto_id)
    if request.user != reunion.proyecto.jefe_proyecto:
        return HttpResponseForbidden('No tienes permiso para modificar esta reunión.')
    if request.method == 'POST':
        form = ReunionProyectoForm(request.POST, instance=reunion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reunión modificada correctamente.')
            return redirect('home-proyecto-alumno', proyecto_id=proyecto_id)
    else:
        form = ReunionProyectoForm(instance=reunion)
    return render(request, 'proyectos/modificar_reunion_proyecto_alumno.html', {'form': form, 'reunion': reunion, 'proyecto': reunion.proyecto})


@login_required
@rol_requerido('alumno')
def eliminar_reunion_proyecto_alumno(request, proyecto_id, reunion_id):
    reunion = get_object_or_404(ReunionProyecto, id_reunion=reunion_id, proyecto_id=proyecto_id)
    if request.user != reunion.proyecto.jefe_proyecto:
        return HttpResponseForbidden('No tienes permiso para eliminar esta reunión.')
    if request.method == 'POST':
        reunion.delete()
        messages.success(request, 'Reunión eliminada correctamente.')
        return redirect('home-proyecto-alumno', proyecto_id=proyecto_id)
    return render(request, 'proyectos/eliminar_reunion_proyecto_alumno.html', {'reunion': reunion, 'proyecto': reunion.proyecto})
