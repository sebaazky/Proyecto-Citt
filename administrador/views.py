from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth import get_user_model
from alumno.models import Proyecto, Perfil_alumno
from .models import Track
import io
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from login.models import User
from django.utils.dateparse import parse_date
import pandas as pd
from django.utils import timezone
from datetime import timedelta
from .forms import PerfilAdministradorForm
from .models import PerfilAdministrador

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
        data = list(proyectos.values('nom_proyecto', 'jefe_proyecto__username', 'jefe_proyecto__rol', 'jefe_proyecto__email', 'descripcion', 'fecha_inicio', 'id_track__nom_track'))
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
        data = list(reuniones.values('track__nom_track', 'fecha', 'hora', 'modalidad', 'ubicacion', 'descripcion'))
        nombre_archivo = 'reporte_reuniones.' + formato
    elif tipo == 'alumnos_track':
        alumnos = User.objects.filter(rol='alumno')
        if selected_track:
            alumnos = alumnos.filter(id_track=selected_track)
        # Agrega la cantidad de proyectos asociados a cada alumno
        data = []
        for alumno in alumnos:
            proyectos_count = Proyecto.objects.filter(jefe_proyecto=alumno).count()
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
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo.replace('.pdf','.xls')}"'
            df.to_excel(response, index=False)
            return response
    return render(request, 'reporte_pdf.html', {
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
    return render(request, 'enviar_correos.html', {'tracks': tracks})

@admin_required
def admin_crear_docente(request):
    User = get_user_model()
    mensaje = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password, rol='docente')
                mensaje = 'Docente creado exitosamente.'
            else:
                mensaje = 'El usuario ya existe.'
    return render(request, 'crear_docente.html', {'mensaje': mensaje})

@admin_required
def admin_crear_usuario(request):
    from login.models import User
    roles = [r[0] for r in User.ROLES]
    mensaje = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        if username and email and rol and password:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                User.objects.create_user(username=username, email=email, password=password, rol=rol)
                mensaje = 'Usuario creado exitosamente.'
            else:
                mensaje = 'El usuario o correo ya existe.'
    return render(request, 'crear_usuario.html', {'roles': roles, 'mensaje': mensaje})

@admin_required
def admin_gestion_roles(request):
    # Los roles están definidos en User.ROLES
    roles = [r[0] for r in User.ROLES]
    if request.method == 'POST':
        if 'nuevo_rol' in request.POST:
            nuevo_rol = request.POST['nuevo_rol'].strip()
            if nuevo_rol and nuevo_rol not in roles:
                User.ROLES.append((nuevo_rol, nuevo_rol.capitalize()))
        elif 'eliminar_rol' in request.POST:
            eliminar_rol = request.POST['eliminar_rol']
            User.ROLES = [r for r in User.ROLES if r[0] != eliminar_rol]
    return render(request, 'gestion_roles.html', {'roles': [r[0] for r in User.ROLES]})

@admin_required
def admin_gestion_usuarios(request):
    docentes = User.objects.filter(rol='docente')
    alumnos = User.objects.filter(rol='alumno')
    # Usuarios inactivos hace más de 1 mes
    hace_un_mes = timezone.now() - timedelta(days=30)
    inactivos = User.objects.filter(last_login__lt=hace_un_mes)
    if request.method == 'POST':
        user_id = request.POST.get('eliminar_usuario')
        if user_id:
            User.objects.filter(id=user_id).delete()
    return render(request, 'gestion_usuarios.html', {'docentes': docentes, 'alumnos': alumnos, 'inactivos': inactivos})

@admin_required
def admin_gestion_tracks(request):
    tracks = Track.objects.all()
    if request.method == 'POST':
        if 'nuevo_track' in request.POST:
            nuevo_track = request.POST['nuevo_track'].strip()
            if nuevo_track and not Track.objects.filter(nom_track=nuevo_track).exists():
                Track.objects.create(nom_track=nuevo_track, id_usuario=request.user)
        elif 'eliminar_track' in request.POST:
            Track.objects.filter(id_track=request.POST['eliminar_track']).delete()
    return render(request, 'gestion_tracks.html', {'tracks': Track.objects.all()})

@admin_required
def admin_eliminar_usuario(request, user_id):
    from login.models import User
    if request.method == 'POST':
        User.objects.filter(id=user_id).delete()
    return redirect('admin-gestion-usuarios')

@admin_required
def admin_editar_track(request, track_id):
    from .models import Track
    track = Track.objects.get(id_track=track_id)
    mensaje = None
    if request.method == 'POST':
        nom_track = request.POST.get('nom_track')
        descripcion = request.POST.get('descripcion')
        id_usuario = request.POST.get('id_usuario')
        imagen = request.FILES.get('imagen')
        if nom_track:
            track.nom_track = nom_track
        if descripcion:
            track.descripcion = descripcion
        if id_usuario:
            from login.models import User
            try:
                docente = User.objects.get(id=id_usuario, rol='docente')
                track.id_usuario = docente
            except User.DoesNotExist:
                mensaje = 'Docente no válido.'
        if imagen:
            track.imagen = imagen
        track.save()
        mensaje = 'Track actualizado correctamente.'
    # Listar docentes para el select
    from login.models import User
    docentes = User.objects.filter(rol='docente')
    return render(request, 'editar_track.html', {'track': track, 'docentes': docentes, 'mensaje': mensaje})

@admin_required
def admin_agregar_track(request):
    from .models import Track
    from login.models import User
    mensaje = None
    docentes = User.objects.filter(rol='docente')
    if request.method == 'POST':
        nom_track = request.POST.get('nom_track')
        descripcion = request.POST.get('descripcion')
        id_usuario = request.POST.get('id_usuario')
        imagen = request.FILES.get('imagen')
        if nom_track and descripcion and id_usuario:
            try:
                docente = User.objects.get(id=id_usuario, rol='docente')
                track = Track(nom_track=nom_track, descripcion=descripcion, id_usuario=docente)
                if imagen:
                    track.imagen = imagen
                track.save()
                mensaje = 'Track creado exitosamente.'
            except User.DoesNotExist:
                mensaje = 'Docente no válido.'
        else:
            mensaje = 'Todos los campos son obligatorios.'
    return render(request, 'agregar_track.html', {'docentes': docentes, 'mensaje': mensaje})

@admin_required
def admin_perfil(request):
    perfil, created = PerfilAdministrador.objects.get_or_create(administrador=request.user)
    if request.method == 'POST':
        form = PerfilAdministradorForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return render(request, 'perfil_admin.html', {'form': form, 'perfil': perfil, 'guardado': True})
    else:
        form = PerfilAdministradorForm(instance=perfil)
    return render(request, 'perfil_admin.html', {'form': form, 'perfil': perfil})
