# Generated by Django 4.2.4 on 2023-08-16 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prenotazione', '0005_delete_piatto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Piatto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('immagine', models.ImageField(blank=True, null=True, upload_to='piatti/')),
                ('titolo', models.CharField(max_length=255)),
                ('descrizione', models.TextField()),
                ('ristorante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='piatti', to='prenotazione.ristorante')),
            ],
        ),
    ]
