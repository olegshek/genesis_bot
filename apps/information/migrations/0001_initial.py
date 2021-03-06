# Generated by Django 3.1.6 on 2021-02-19 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lead', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformationText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=4000, verbose_name='Text')),
                ('text_ru', models.CharField(max_length=4000, null=True, verbose_name='Text')),
                ('text_uz', models.CharField(max_length=4000, null=True, verbose_name='Text')),
                ('text_en', models.CharField(max_length=4000, null=True, verbose_name='Text')),
            ],
        ),
        migrations.CreateModel(
            name='InformationPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='information_photo', to='lead.photo', verbose_name='Photo')),
            ],
        ),
        migrations.CreateModel(
            name='InformationFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='information_file', to='lead.file', verbose_name='File')),
            ],
        ),
    ]
