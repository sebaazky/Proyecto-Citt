from administrador.models import Track


def tracks_disponibles(request):
    return {
        'tracks': Track.objects.all()
    }
