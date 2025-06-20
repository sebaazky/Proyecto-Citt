# Generated by Django 5.2 on 2025-06-05 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id_carrera', models.AutoField(db_column='idCarrera', primary_key=True, serialize=False)),
                ('nom_carrera', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id_comuna', models.AutoField(db_column='idComuna', primary_key=True, serialize=False)),
                ('nom_comuna', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id_genero', models.AutoField(db_column='idGenero', primary_key=True, serialize=False)),
                ('nom_genero', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ReunionTrack',
            fields=[
                ('id_reunion', models.AutoField(db_column='idReunion', primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('modalidad', models.CharField(choices=[('presencial', 'Presencial'), ('virtual', 'Virtual')], default='presencial', max_length=20)),
                ('link_virtual', models.URLField(blank=True, help_text='Enlace para reuniones virtuales', null=True)),
                ('ubicacion', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoEvento',
            fields=[
                ('id_tipo_evento', models.AutoField(primary_key=True, serialize=False, verbose_name='idTipoEvento')),
                ('nombre_tipo_evento', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id_track', models.AutoField(db_column='idTrack', primary_key=True, serialize=False)),
                ('nom_track', models.CharField(max_length=30)),
                ('descripcion', models.CharField(default='Descripción del track', max_length=250)),
                ('imagen', models.ImageField(default='images/default_track.png', upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='TrackRequest',
            fields=[
                ('id_solicitud', models.AutoField(db_column='idSolicitud', primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')], default='pendiente', max_length=10)),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
