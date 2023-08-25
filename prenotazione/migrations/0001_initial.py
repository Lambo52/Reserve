# Generated by Django 4.2.4 on 2023-08-14 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ristorante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('carne', models.BooleanField(default=False)),
                ('pesce', models.BooleanField(default=False)),
                ('pizza', models.BooleanField(default=False)),
                ('vegan', models.BooleanField(default=False)),
                ('sushi', models.BooleanField(default=False)),
                ('fascia_prezzo', models.CharField(default='media', max_length=255)),
                ('descrizione', models.TextField()),
                ('telefono', models.BigIntegerField()),
                ('luogo', models.CharField(max_length=255)),
                ('posti_totali', models.PositiveIntegerField()),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ristoranti', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prenotazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('ora', models.TimeField()),
                ('numero_persone', models.IntegerField()),
                ('ristorante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prenotazioni', to='prenotazione.ristorante')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prenotazioni', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListaAttesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('ora', models.TimeField()),
                ('numero_persone', models.PositiveIntegerField()),
                ('ristorante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liste_attesa', to='prenotazione.ristorante')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liste_attesa', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]