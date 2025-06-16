from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.decorators import rol_requerido
from administrador.models import Track, TrackRequest, ReunionTrack
from django.shortcuts import get_object_or_404
from .models import PerfilDocente, Evento, TrackPost, PostProyectoDocente, ReunionProyectoDocente
from .forms import EventoForm, PerfilDocenteForm, ReunionProyectoDocenteForm, DocentePostForm
from django.http import HttpResponseForbidden
from .forms import ProyectoDocenteForm, ReunionTrackForm
from django.contrib import messages
from alumno.models import Proyecto, ProyectoPost, ReunionProyecto, ProyectoRequest, Perfil_alumno
from alumno.forms import ProyectoPostForm, ReunionProyectoForm


# Create your views here.


@login_required
@rol_requerido('docente')
def home_docente(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    return render(request, 'home-docente.html', {'track': track})


@login_required
@rol_requerido('docente')
def ver_perfil_docente(request):
    perfil, created = PerfilDocente.objects.get_or_create(docente=request.user)
    return render(request, 'perfil/ver_perfil_docente.html', {'perfil': perfil})


@login_required
@rol_requerido('docente')
def editar_perfil_docente(request):
    perfil = get_object_or_404(PerfilDocente, docente=request.user)
    if request.method == 'POST':
        form = PerfilDocenteForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('ver-perfil-doc')
    else:
        form = PerfilDocenteForm(instance=perfil)
    return render(request, 'perfil/editar_perfil_docente.html', {'form': form})


# @login_required
# @rol_requerido('docente')
# def solicitudes_pendientes_view(request):
#     if request.user.rol != 'docente':
#         return render(request, 'error.html', {'mensaje': 'No autorizado'})

#     track = Track.objects.filter(id_usuario=request.user).first()

#     if not track:
#         return render(request, 'error.html', {'mensaje': 'No tienes un track asignado'})

#     solicitudes = TrackRequest.objects.filter(track=track, estado='pendiente')

#     return render(request, 'solicitudes/solicitudes-alumnos.html', {
#         'track': track,
#         'solicitudes': solicitudes
#     })

@login_required
@rol_requerido('docente')
def solicitudes_pendientes_view(request):
    if request.user.rol != 'docente':
        messages.error(
            request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home-docente')

    track = Track.objects.filter(id_usuario=request.user).first()

    if not track:
        messages.warning(
            request, 'No tienes un track asignado. Contacta con el administrador.')
        return redirect('home-docente')  # o a otra vista que tenga sentido

    solicitudes = TrackRequest.objects.filter(track=track, estado='pendiente')
    return render(request, 'solicitudes/solicitudes-alumnos.html', {
        'track': track,
        'solicitudes': solicitudes
    })


@login_required
@rol_requerido('docente')
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(TrackRequest, id_solicitud=solicitud_id)

    solicitud.estado = 'aprobada'
    solicitud.save()

    usuario_alumno = solicitud.alumno
    usuario_alumno.id_track = solicitud.track
    usuario_alumno.save(update_fields=["id_track"])

    # Rechazar otras solicitudes pendientes del alumno
    TrackRequest.objects.filter(alumno=usuario_alumno).exclude(id_solicitud=solicitud_id).update(estado='rechazada')

    return redirect('solicitudes_pendientes')


@login_required
@rol_requerido('docente')
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(TrackRequest, id_solicitud=solicitud_id)

    solicitud.estado = 'rechazado'
    solicitud.save()
    return redirect('solicitudes_pendientes')


@login_required
@rol_requerido('docente')
def listar_eventos(request):
    eventos = Evento.objects.filter(docente=request.user)
    return render(request, 'evento/listar_eventos.html', {'eventos': eventos})


@login_required
@rol_requerido('docente')
def añadir_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.docente = request.user
            evento.save()
            return redirect('listar-eventos')
    else:
        form = EventoForm()
    return render(request, 'evento/añadir_evento.html', {'form': form})


@login_required
@rol_requerido('docente')
def modificar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, docente=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('listar-eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'evento/modificar_evento.html', {'form': form})


@login_required
@rol_requerido('docente')
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, docente=request.user)
    if request.method == 'POST':
        evento.delete()
        return redirect('listar-eventos')
    return render(request, 'evento/eliminar_evento.html', {'evento': evento})


@login_required
@rol_requerido('docente')
def mi_track_view(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    if request.method == 'POST' and track:
        form = DocentePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.docente = request.user
            post.track = track
            post.save()
            return redirect('mi-track')
    else:
        form = DocentePostForm()
    posts = TrackPost.objects.filter(track=track).order_by('-fecha_creacion') if track else []
    proyectos = Proyecto.objects.filter(id_track=track) if track else []
    proyectos_info = [{'proyecto': p} for p in proyectos]
    reuniones = ReunionTrack.objects.filter(track=track).order_by('-fecha') if track else []
    eventos = Evento.objects.filter(docente=request.user) if track else []
    from login.models import User
    integrantes = User.objects.filter(id_track=track, rol='alumno') if track else []
    context = {
        'track': track,
        'posts': posts,
        'post_form': form,
        'proyectos_info': proyectos_info,
        'reuniones': reuniones,
        'eventos': eventos,
        'alumnos': integrantes,
    }
    return render(request, 'track/mi_track.html', context)


@login_required
@rol_requerido('docente')
def crear_post_docente(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    if request.method == 'POST' and track:
        form = DocentePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.docente = request.user
            post.track = track
            post.save()
    return redirect('mi-track')


@login_required
@rol_requerido('docente')
def eliminar_post_docente(request, post_id):
    post = TrackPost.objects.get(id=post_id)
    if post.docente != request.user:
        return HttpResponseForbidden()
    post.delete()
    return redirect('mi-track')


@login_required
@rol_requerido('docente')
def modificar_post_docente(request, post_id):
    post = TrackPost.objects.get(id=post_id)
    if post.docente != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = DocentePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('mi-track')
    else:
        form = DocentePostForm(instance=post)
    track = post.track
    posts = TrackPost.objects.filter(track=track).order_by('-fecha_creacion')
    return render(request, 'track/mi_track.html', {'track': track, 'posts': posts, 'post_form': form, 'edit_post_id': post.id})


@login_required
@rol_requerido('docente')
def listado_alumnos_track(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    alumnos = Perfil_alumno.objects.filter(
        alumno__id_track=track) if track else []
    return render(request, 'track/mi_track.html', {
        'track': track,
        'alumnos_list': alumnos,
        'central_content': 'alumnos',
    })


@login_required
@rol_requerido('docente')
def eliminar_alumno_track(request, alumno_id):
    track = Track.objects.filter(id_usuario=request.user).first()
    alumno = Perfil_alumno.objects.get(pk=alumno_id)
    if request.method == 'POST':
        user = alumno.alumno
        user.id_track = None
        user.save()
        return redirect('listado-alumnos-track')
    return render(request, 'track/confirmar_eliminar_alumno.html', {'alumno': alumno})


@login_required
@rol_requerido('docente')
def listado_solicitudes_track(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    solicitudes = TrackRequest.objects.filter(
        track=track, estado='pendiente') if track else []
    return render(request, 'track/mi_track.html', {
        'track': track,
        'solicitudes_list': solicitudes,
        'central_content': 'solicitudes',
    })


@login_required
@rol_requerido('docente')
def listado_eventos_track(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    eventos = Evento.objects.filter(docente=request.user) if track else []
    return render(request, 'track/mi_track.html', {
        'track': track,
        'eventos_list': eventos,
        'central_content': 'eventos',
    })


@login_required
@rol_requerido('docente')
def listar_reuniones_track(request):
    reuniones = ReunionTrack.objects.filter(id_docente=request.user)
    return render(request, 'reuniones/listar_reuniones.html', {'reuniones': reuniones})


@login_required
@rol_requerido('docente')
def crear_reunion_track(request):
    if request.method == 'POST':
        form = ReunionTrackForm(request.POST)
        if form.is_valid():
            reunion = form.save(commit=False)
            reunion.id_docente = request.user

            # Obtener el track asociado al docente
            track = Track.objects.filter(id_usuario=request.user).first()
            if not track:
                messages.error(request, "No tienes un track asignado.")
                return redirect('mi-track')

            reunion.track = track
            reunion.save()
            messages.success(request, "Reunión creada correctamente.")
            return redirect('listar-reuniones-track')
    else:
        form = ReunionTrackForm()

    return render(request, 'reuniones/crear_reunion.html', {'form': form})


@login_required
@rol_requerido('docente')
def editar_reunion_track(request, pk):
    reunion = get_object_or_404(ReunionTrack, pk=pk, id_docente=request.user)
    if request.method == 'POST':
        form = ReunionTrackForm(request.POST, instance=reunion)
        if form.is_valid():
            form.save()
            return redirect('listar-reuniones-track')
    else:
        form = ReunionTrackForm(instance=reunion)
    return render(request, 'reuniones/editar_reunion.html', {'form': form})


@login_required
@rol_requerido('docente')
def eliminar_reunion_track(request, pk):
    reunion = get_object_or_404(ReunionTrack, pk=pk, id_docente=request.user)
    if request.method == 'POST':
        reunion.delete()
        return redirect('listar-reuniones-track')
    return render(request, 'reuniones/eliminar_reunion.html', {'reunion': reunion})


@login_required
@rol_requerido('docente')
def detalle_reunion_modal(request, pk):
    reunion = get_object_or_404(ReunionTrack, pk=pk)
    return render(request, 'reuniones/detalle_reunion.html', {'reunion': reunion})


# proyecto


@login_required
@rol_requerido('docente')
def listar_proyectos_docente(request):
    track = Track.objects.filter(id_usuario=request.user).first()
    proyectos = Proyecto.objects.filter(id_track=track) if track else Proyecto.objects.none()
    return render(request, 'proyectos/listar_proyectos_docente.html', {'proyectos': proyectos})


@login_required
@rol_requerido('docente')
def crear_proyecto_docente(request):
    # Obtener el track del docente
    track = Track.objects.filter(id_usuario=request.user).first()
    if not track:
        messages.error(request, "No tienes un track asignado. Contacta al administrador.")
        return redirect('listar-proyectos-docente')

    if request.method == 'POST':
        form = ProyectoDocenteForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.id_track = track
            proyecto.jefe_proyecto = request.user
            proyecto.save()
            return redirect('listar-proyectos-docente')
    else:
        form = ProyectoDocenteForm()
    return render(request, 'proyectos/crear_proyecto_docente.html', {'form': form})


@login_required
@rol_requerido('docente')
def modificar_proyecto_docente(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoDocenteForm(
            request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('listar-proyectos-docente')
    else:
        form = ProyectoDocenteForm(instance=proyecto)
    return render(request, 'proyectos/modificar_proyecto_docente.html', {'form': form})


@login_required
@rol_requerido('docente')
def eliminar_proyecto_docente(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('listar-proyectos-docente')
    return render(request, 'proyectos/eliminar_proyecto_docente.html', {'proyecto': proyecto})


@login_required
@rol_requerido('docente')
def home_proyecto_docente(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    es_jefe = request.user == proyecto.jefe_proyecto
    integrantes = proyecto.integrantes.all() if hasattr(proyecto, 'integrantes') else []

    # Crear post
    post_form = ProyectoPostForm()
    if request.method == 'POST' and 'crear_post' in request.POST:
        post_form = ProyectoPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.proyecto = proyecto
            post.autor = request.user
            post.save()
            return redirect('home-proyecto-docente', proyecto_id=proyecto.id_proyecto)

    # Crear reunión
    reunion_form = ReunionProyectoForm()
    if request.method == 'POST' and 'crear_reunion' in request.POST:
        reunion_form = ReunionProyectoForm(request.POST)
        if reunion_form.is_valid():
            reunion = reunion_form.save(commit=False)
            reunion.proyecto = proyecto
            reunion.save()
            return redirect('home-proyecto-docente', proyecto_id=proyecto.id_proyecto)

    posts = ProyectoPost.objects.filter(proyecto=proyecto).order_by('-fecha_creacion')
    reuniones = ReunionProyecto.objects.filter(proyecto=proyecto).order_by('-fecha')
    solicitudes = ProyectoRequest.objects.filter(proyecto=proyecto, estado='pendiente').order_by('-fecha_solicitud') if es_jefe and request.GET.get('seccion') == 'solicitudes' else []
    page_number = request.GET.get('page')
    from django.core.paginator import Paginator
    reuniones_paginadas = Paginator(reuniones, 5).get_page(page_number)

    # Obtener perfil del jefe de proyecto
    perfil_docente_jefe = None
    if hasattr(proyecto.jefe_proyecto, 'perfil_docente'):
        perfil_docente_jefe = proyecto.jefe_proyecto.perfil_docente

    # Perfiles docentes de los autores de los posts
    perfiles_docentes_posts = {}
    for post in posts:
        if hasattr(post.autor, 'perfil_docente'):
            perfiles_docentes_posts[post.id_post] = post.autor.perfil_docente
        else:
            perfiles_docentes_posts[post.id_post] = None

    # Cantidad máxima de integrantes
    cantidad_max_integrantes = proyecto.num_integrantes

    # Perfiles de los integrantes (incluyendo jefe)
    integrantes_con_perfil_docente = []
    if perfil_docente_jefe:
        integrantes_con_perfil_docente.append({'user': proyecto.jefe_proyecto, 'perfil': perfil_docente_jefe, 'es_jefe': True})
    for integrante in integrantes:
        if hasattr(integrante.alumno, 'perfil_docente'):
            integrantes_con_perfil_docente.append({'user': integrante.alumno, 'perfil': integrante.alumno.perfil_docente, 'es_jefe': False})

    context = {
        'proyecto': proyecto,
        'posts': posts,
        'reuniones': reuniones,
        'reuniones_paginadas': reuniones_paginadas,
        'es_jefe': es_jefe,
        'reunion_form': reunion_form,
        'post_form': post_form,
        'integrantes': integrantes,
        'solicitudes': solicitudes,
        'perfil_docente_jefe': perfil_docente_jefe,
        'perfiles_docentes_posts': perfiles_docentes_posts,
        'cantidad_max_integrantes': cantidad_max_integrantes,
        'integrantes_con_perfil_docente': integrantes_con_perfil_docente,
    }
    return render(request, 'proyectos/home_proyecto_docente.html', context)


@login_required
@rol_requerido('docente')
def crear_post_proyecto_docente(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id_proyecto=proyecto_id)
    if request.user != proyecto.jefe_proyecto:
        return HttpResponseForbidden('No tienes permiso para publicar en este proyecto.')
    if request.method == 'POST':
        form = ProyectoPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.proyecto = proyecto
            post.autor = request.user
            post.save()
            messages.success(request, 'Post creado correctamente.')
            return redirect('home-proyecto-docente', proyecto_id=proyecto_id)
    return redirect('home-proyecto-docente', proyecto_id=proyecto_id)


@login_required
@rol_requerido('docente')
def modificar_post_proyecto_docente(request, proyecto_id, post_id):
    post = get_object_or_404(ProyectoPost, id_post=post_id, proyecto_id=proyecto_id)
    if post.autor != request.user:
        return HttpResponseForbidden('No tienes permiso para modificar este post.')
    if request.method == 'POST':
        form = ProyectoPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post modificado correctamente.')
            return redirect('home-proyecto-docente', proyecto_id=proyecto_id)
    else:
        form = ProyectoPostForm(instance=post)
    return render(request, 'proyectos/modificar_post_proyecto_docente.html', {'form': form, 'post': post, 'proyecto': post.proyecto})


@login_required
@rol_requerido('docente')
def eliminar_post_proyecto_docente(request, proyecto_id, post_id):
    post = get_object_or_404(ProyectoPost, id_post=post_id, proyecto_id=proyecto_id)
    if post.autor != request.user:
        return HttpResponseForbidden('No tienes permiso para eliminar este post.')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post eliminado correctamente.')
        return redirect('home-proyecto-docente', proyecto_id=proyecto_id)
    return render(request, 'proyectos/eliminar_post_proyecto_docente.html', {'post': post, 'proyecto': post.proyecto})


# Reuniones en proyectos

@login_required
@rol_requerido('docente')
def crear_reunion_proyecto_docente(request, proyecto_id):
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
    return redirect('home-proyecto-docente', proyecto_id=proyecto_id)


@login_required
@rol_requerido('docente')
def modificar_reunion_proyecto_docente(request, proyecto_id, reunion_id):
    reunion = get_object_or_404(ReunionProyecto, id_reunion=reunion_id, proyecto_id=proyecto_id)
    if request.user != reunion.proyecto.jefe_proyecto:
        return HttpResponseForbidden('No tienes permiso para modificar esta reunión.')
    if request.method == 'POST':
        form = ReunionProyectoForm(request.POST, instance=reunion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reunión modificada correctamente.')
            return redirect('home-proyecto-docente', proyecto_id=proyecto_id)
    else:
        form = ReunionProyectoForm(instance=reunion)
    return render(request, 'proyectos/modificar_reunion_proyecto_docente.html', {'form': form, 'reunion': reunion, 'proyecto': reunion.proyecto})


@login_required
@rol_requerido('docente')
def eliminar_reunion_proyecto_docente(request, proyecto_id, reunion_id):
    reunion = get_object_or_404(ReunionProyecto, id_reunion=reunion_id, proyecto_id=proyecto_id)
    if request.user != reunion.proyecto.jefe_proyecto:
        return HttpResponseForbidden('No tienes permiso para eliminar esta reunión.')
    if request.method == 'POST':
        reunion.delete()
        messages.success(request, 'Reunión eliminada correctamente.')
        return redirect('home-proyecto-docente', proyecto_id=proyecto_id)
    return render(request, 'proyectos/eliminar_reunion_proyecto_docente.html', {'reunion': reunion, 'proyecto': reunion.proyecto})
