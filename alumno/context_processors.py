from administrador.models import Track, TrackRequest

def tracks_disponibles(request):
    # Menú restringido para alumnos en onboarding
    user = getattr(request, 'user', None)
    mostrar_menu_restringido = False
    if user and user.is_authenticated and hasattr(user, 'rol') and user.rol == 'alumno':
        try:
            perfil = user.perfil_alumno
            tiene_perfil = perfil.nombres and perfil.apellido_paterno
        except Exception:
            tiene_perfil = False
        if not tiene_perfil:
            mostrar_menu_restringido = True
        else:
            solicitud = TrackRequest.objects.filter(alumno=user).order_by('-fecha_solicitud').first()
            if not solicitud or (solicitud and solicitud.estado != 'aprobada'):
                mostrar_menu_restringido = True
    return {
        'tracks': Track.objects.all(),
        'mostrar_menu_restringido': mostrar_menu_restringido
    }
