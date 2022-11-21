# Generated by Django 3.1.13 on 2022-11-14 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_y_apellido', models.CharField(max_length=30)),
                ('fecha_de_nacimiento', models.DateField(help_text='Formato AAAA-MM-DD')),
                ('sexo', models.CharField(choices=[('MASCULINO', 'Masculino'), ('FEMENINO', 'Femenino'), ('OTRO', 'Otro')], max_length=10)),
                ('telefono', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('CV_pdf', models.FileField(upload_to='uploads/CVs')),
                ('creado_a', models.DateTimeField(auto_now_add=True)),
                ('modificado_a', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
