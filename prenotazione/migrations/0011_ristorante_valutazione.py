# Generated by Django 4.1.7 on 2023-08-23 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prenotazione', '0010_recensione_valutazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='ristorante',
            name='valutazione',
            field=models.FloatField(default=0.0),
        ),
    ]