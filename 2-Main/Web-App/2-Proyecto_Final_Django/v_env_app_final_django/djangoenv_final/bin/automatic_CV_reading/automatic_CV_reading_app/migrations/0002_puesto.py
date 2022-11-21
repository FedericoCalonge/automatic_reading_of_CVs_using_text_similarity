# Generated by Django 3.1.13 on 2022-11-21 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automatic_CV_reading_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('descripcion', models.TextField()),
                ('ubicacion', models.CharField(max_length=20)),
                ('creado_a', models.DateTimeField(auto_now_add=True)),
                ('modificado_a', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
