# Generated by Django 4.1.7 on 2023-08-22 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prenotazione', '0007_remove_ristorante_menu_piatto_prezzo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recensione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=255)),
                ('descrizione', models.TextField()),
                ('valutazione', models.IntegerField()),
                ('ristorante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recensioni', to='prenotazione.ristorante')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recensioni', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('ristorante', 'utente')},
            },
        ),
    ]
