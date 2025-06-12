from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth import get_user_model
from alumno.models import Proyecto, Perfil_alumno, Solicitud
from .models import Track
import io
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from login.models import User
from django.utils.dateparse import parse_date
import pandas as pd
from django.utils import timezone
from datetime import timedelta
from .forms import PerfilAdministradorForm, ProyectoForm, SolicitudForm, EventoForm, PerfilDocenteForm, CrearPerfilDocenteForm, CrearPerfilAlumnoForm, ModificarPerfilAlumnoForm, CrearUsuarioForm, ModificarUsuarioForm, CrearTrackForm, ModificarTrackForm
from .models import PerfilAdministrador, Track
from django.shortcuts import get_object_or_404
from docente.models import Evento, PerfilDocente
from django.contrib import messages


# Solo administradores pueden acceder


def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'administrador')(view_func)


@admin_required
def admin_home(request):
    return render(request, 'admin-home.html')


@admin_required
def admin_reporte_pdf(request):
    tracks = Track.objects.all()
    tipos = [
        ('proyectos', 'Proyectos'),
        ('reuniones', 'Reuniones'),
        ('alumnos_track', 'Alumnos por Track'),
        ('alumnos_totales', 'Alumnos Totales por Track'),
    ]
    tipo = request.GET.get('tipo', 'proyectos')
    selected_track = request.GET.get('track')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    formato = request.GET.get('formato', 'pdf')
    data = []
    nombre_archivo = 'reporte.pdf'
    fecha_generacion = timezone.now()
    # Filtros de fecha
    fecha_inicio_obj = parse_date(fecha_inicio) if fecha_inicio else None
    fecha_fin_obj = parse_date(fecha_fin) if fecha_fin else None
    if tipo == 'proyectos':
        proyectos = Proyecto.objects.all()
        if selected_track:
            proyectos = proyectos.filter(id_track=selected_track)
        if fecha_inicio_obj:
            proyectos = proyectos.filter(fecha_inicio__gte=fecha_inicio_obj)
        if fecha_fin_obj:
            proyectos = proyectos.filter(fecha_inicio__lte=fecha_fin_obj)
        # Mostrar todos los proyectos, sin importar el rol del jefe_proyecto
        data = list(proyectos.values('nom_proyecto', 'jefe_proyecto__username', 'jefe_proyecto__rol',
                    'jefe_proyecto__email', 'descripcion', 'fecha_inicio', 'id_track__nom_track'))
        nombre_archivo = 'reporte_proyectos.' + formato
    elif tipo == 'reuniones':
        from administrador.models import ReunionTrack
        reuniones = ReunionTrack.objects.all()
        if selected_track:
            reuniones = reuniones.filter(track=selected_track)
        if fecha_inicio_obj:
            reuniones = reuniones.filter(fecha__gte=fecha_inicio_obj)
        if fecha_fin_obj:
            reuniones = reuniones.filter(fecha__lte=fecha_fin_obj)
        data = list(reuniones.values('track__nom_track', 'fecha',
                    'hora', 'modalidad', 'ubicacion', 'descripcion'))
        nombre_archivo = 'reporte_reuniones.' + formato
    elif tipo == 'alumnos_track':
        alumnos = User.objects.filter(rol='alumno')
        if selected_track:
            alumnos = alumnos.filter(id_track=selected_track)
        # Agrega la cantidad de proyectos asociados a cada alumno
        data = []
        for alumno in alumnos:
            proyectos_count = Proyecto.objects.filter(
                jefe_proyecto=alumno).count()
            data.append({
                'username': alumno.username,
                'email': alumno.email,
                'id_track__nom_track': alumno.id_track.nom_track if alumno.id_track else '',
                'proyectos_count': proyectos_count
            })
        nombre_archivo = 'reporte_alumnos_track.' + formato
    elif tipo == 'alumnos_totales':
        alumnos = User.objects.filter(rol='alumno')
        data = list(alumnos.values('username', 'email', 'id_track__nom_track'))
        # Ordenar por track
        data = sorted(data, key=lambda x: x['id_track__nom_track'] or '')
        nombre_archivo = 'reporte_alumnos_totales.' + formato
    # Generar PDF o XLS
    if 'download' in request.GET and data:
        if formato == 'pdf':
            html = render_to_string('reporte_pdf_export.html', {
                'data': data,
                'tipo': tipo,
                'tracks': tracks,
                'selected_track': selected_track,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'now': fecha_generacion
            })
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=response)
            return response
        elif formato == 'xls':
            df = pd.DataFrame(data)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response[
                'Content-Disposition'] = f'attachment; filename="{nombre_archivo.replace('.pdf', '.xls')}"'
            df.to_excel(response, index=False)
            return response
    return render(request, 'reportes/reporte_pdf.html', {
        'tracks': tracks,
        'tipos': tipos,
        'tipo': tipo,
        'selected_track': selected_track,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'formato': formato,
        'data': data,
        'now': fecha_generacion
    })


@admin_required
def admin_enviar_correos(request):
    tracks = Track.objects.all()
    enviados = 0
    # AJAX para obtener correos según destinatario y track
    if request.method == 'GET' and request.GET.get('ajax') == '1':
        destinatario = request.GET.get('destinatario')
        track_id = request.GET.get('track')
        users = User.objects.all()
        if destinatario == 'alumnos':
            users = users.filter(rol='alumno')
        elif destinatario == 'docentes':
            users = users.filter(rol='docente')
        if track_id:
            users = users.filter(id_track=track_id)
        correos = list(users.values('id', 'email', 'username'))
        return JsonResponse({'correos': correos})
    # Envío de correos
    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        destinatario = request.POST.get('destinatario')
        track_id = request.POST.get('track')
        selected_ids = request.POST.getlist('selected_ids[]')
        users = User.objects.all()
        if destinatario == 'alumnos':
            users = users.filter(rol='alumno')
        elif destinatario == 'docentes':
            users = users.filter(rol='docente')
        if track_id:
            users = users.filter(id_track=track_id)
        if selected_ids:
            users = users.filter(id__in=selected_ids)
        correos = [u.email for u in users if u.email]
        if correos:
            send_mail(
                asunto or 'Mensaje CITT',
                mensaje,
                'cittduoc2025@gmail.com',
                correos,
                fail_silently=False,
            )
            enviados = len(correos)
        return render(request, 'enviar_correos.html', {'tracks': tracks, 'enviados': enviados})
    return render(request, 'correos/enviar_correos.html', {'tracks': tracks})


@admin_required
def admin_perfil(request):
    perfil, created = PerfilAdministrador.objects.get_or_create(
        administrador=request.user)
    if request.method == 'POST':
        form = PerfilAdministradorForm(
            request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return render(request, 'perfil_admin.html', {'form': form, 'perfil': perfil, 'guardado': True})
    else:
        form = PerfilAdministradorForm(instance=perfil)
    return render(request, 'perfil/perfil_admin.html', {'form': form, 'perfil': perfil})


def listar_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/listar_proyectos_admin.html', {'proyectos': proyectos})


def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-gestion-proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear_proyecto_admin.html', {'form': form})


def modificar_proyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('admin-gestion-proyectos')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/modificar_proyecto_admin.html', {'form': form})


def eliminar_proyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id_proyecto=id_proyecto)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('admin-gestion-proyectos')
    return render(request, 'proyectos/eliminar_proyecto_admin.html', {'proyecto': proyecto})


def listar_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request, 'solicitudes/listar_solicitudes_admin.html', {'solicitudes': solicitudes})


def modificar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('admin-gestion-solicitudes')
    else:
        form = SolicitudForm(instance=solicitud)
    return render(request, 'solicitudes/modificar_solicitud_admin.html', {'form': form})


def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    if request.method == 'POST':
        solicitud.delete()
        return redirect('admin-gestion-solicitudes')
    return render(request, 'solicitudes/eliminar_solicitud_admin.html', {'solicitud': solicitud})


def listar_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha_evento', '-hora')
    return render(request, 'eventos/listar_eventos_admin.html', {'eventos': eventos})


def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-gestion-eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento_admin.html', {'form': form})


def modificar_evento(request, id_evento):
    evento = get_object_or_404(Evento, id_evento=id_evento)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('admin-gestion-eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/modificar_evento_admin.html', {'form': form})


def eliminar_evento(request, id_evento):
    evento = get_object_or_404(Evento, id_evento=id_evento)
    if request.method == 'POST':
        evento.delete()
        return redirect('admin-gestion-eventos')
    return render(request, 'eventos/eliminar_evento_admin.html', {'evento': evento})


@admin_required
def admin_listar_docentes(request):
    docentes = PerfilDocente.objects.select_related(
        'docente', 'genero', 'carrera').filter(docente__isnull=False)
    return render(request, 'docentes/listar_docentes_admin.html', {'docentes': docentes})


@admin_required
def admin_crear_perfil_docente(request):
    if request.method == 'POST':
        form = CrearPerfilDocenteForm(request.POST, request.FILES)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.docente.rol = 'docente'  # Refuerza el rol
            perfil.docente.save()
            perfil.save()
            return redirect('admin-gestion-docentes')
    else:
        form = CrearPerfilDocenteForm()
    return render(request, 'docentes/crear_perfil_docente.html', {'form': form})


@admin_required
def admin_modificar_docente(request, pk):
    docente = get_object_or_404(PerfilDocente, pk=pk)
    if request.method == 'POST':
        form = PerfilDocenteForm(request.POST, request.FILES, instance=docente)
        if form.is_valid():
            form.save()
            return redirect('admin-gestion-docentes')
    else:
        form = PerfilDocenteForm(instance=docente)
    return render(request, 'docentes/modificar_docente.html', {'form': form})


@admin_required
def admin_eliminar_docente(request, pk):
    docente = get_object_or_404(PerfilDocente, pk=pk)
    if request.method == 'POST':
        docente.delete()
        return redirect('admin-gestion-docentes')
    return render(request, 'docentes/eliminar_docente.html', {'docente': docente})


@admin_required
def admin_listar_alumnos(request):
    alumnos = Perfil_alumno.objects.select_related('alumno', 'genero', 'carrera', 'track_interes') \
                                   .filter(alumno__rol='alumno')
    return render(request, 'alumnos/listar_alumnos_admin.html', {'alumnos': alumnos})


@admin_required
def admin_crear_alumno(request):
    if request.method == 'POST':
        form = CrearPerfilAlumnoForm(request.POST, request.FILES)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.alumno.rol = 'alumno'
            perfil.alumno.save()
            perfil.save()
            return redirect('admin-gestion-alumnos')
    else:
        form = CrearPerfilAlumnoForm()
    return render(request, 'alumnos/crear_perfil_alumno.html', {'form': form})


@admin_required
def admin_modificar_alumno(request, pk):
    alumno = get_object_or_404(Perfil_alumno, pk=pk)
    if request.method == 'POST':
        form = ModificarPerfilAlumnoForm(
            request.POST, request.FILES, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('admin-gestion-alumnos')
    else:
        form = ModificarPerfilAlumnoForm(instance=alumno)
    return render(request, 'alumnos/modificar_alumno.html', {'form': form})


@admin_required
def admin_eliminar_alumno(request, pk):
    alumno = get_object_or_404(Perfil_alumno, pk=pk)
    if request.method == 'POST':
        alumno.delete()
        return redirect('admin-gestion-alumnos')
    return render(request, 'alumnos/eliminar_alumno.html', {'alumno': alumno})


def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.rol == 'administrador')(view_func)


User = get_user_model()


@login_required
def admin_listar_usuarios(request):
    usuarios = User.objects.exclude(is_superuser=True)
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})


@login_required
def admin_crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('admin-gestion-usuarios')
    else:
        form = CrearUsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


@login_required
def admin_modificar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ModificarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('admin-gestion-usuarios')
    else:
        form = ModificarUsuarioForm(instance=usuario)
    return render(request, 'usuarios/modificar_usuario.html', {'form': form})


@login_required
def admin_eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('admin-gestion-usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})


@login_required
def listar_tracks(request):
    tracks = Track.objects.all()
    return render(request, 'tracks/listar_tracks.html', {'tracks': tracks})


@login_required
def crear_track(request):
    if request.method == 'POST':
        form = CrearTrackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Track creado correctamente.')
            return redirect('admin-listar-tracks')
    else:
        form = CrearTrackForm()
    return render(request, 'tracks/crear_track.html', {'form': form})


@login_required
def modificar_track(request, id_track):
    track = get_object_or_404(Track, id_track=id_track)
    if request.method == 'POST':
        form = ModificarTrackForm(request.POST, request.FILES, instance=track)
        if form.is_valid():
            form.save()
            messages.success(request, 'Track modificado correctamente.')
            return redirect('admin-listar-tracks')
    else:
        form = ModificarTrackForm(instance=track)
    return render(request, 'tracks/modificar_track.html', {'form': form})


@login_required
def eliminar_track(request, id_track):
    track = get_object_or_404(Track, id_track=id_track)
    if request.method == 'POST':
        track.delete()
        messages.success(request, 'Track eliminado correctamente.')
        return redirect('admin-listar-tracks')
    return render(request, 'tracks/eliminar_track.html', {'track': track})
