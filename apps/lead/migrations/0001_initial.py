# Generated by Django 3.1.6 on 2021-02-19 09:32

import core.utils
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=4000, verbose_name='Description')),
                ('description_ru', models.CharField(max_length=4000, null=True, verbose_name='Description')),
                ('description_uz', models.CharField(max_length=4000, null=True, verbose_name='Description')),
                ('description_en', models.CharField(max_length=4000, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(blank=True, max_length=20, null=True, verbose_name='Username')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Full name')),
                ('phone_number', models.CharField(max_length=20, null=True, verbose_name='Phone number')),
                ('language', models.CharField(choices=[('ru', 'Russian'), ('uz', 'Uzbek'), ('en', 'English')], max_length=2, null=True, verbose_name='Language')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', verbose_name='File')),
                ('description', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_ru', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_uz', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_en', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='', verbose_name='Photo')),
                ('description', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_ru', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_uz', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_en', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='RoomQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(unique=True, verbose_name='Quantity')),
            ],
            options={
                'verbose_name': 'Room quantity',
                'verbose_name_plural': 'Room quantities',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='', verbose_name='File')),
                ('description', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_ru', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_uz', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
                ('description_en', models.CharField(blank=True, max_length=198, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('name_ru', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('name_uz', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='residences', to='lead.photo', verbose_name='Photo')),
            ],
            options={
                'verbose_name': 'Residence',
                'verbose_name_plural': 'Residences',
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=core.utils.generate_number)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead', to='lead.apartment', verbose_name='Apartment')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='lead.customer', verbose_name='Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=core.utils.generate_number)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='lead.customer', verbose_name='Customer')),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='files',
            field=models.ManyToManyField(related_name='apartments', to='lead.File', verbose_name='Files'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='photos',
            field=models.ManyToManyField(related_name='apartments', to='lead.Photo', verbose_name='Photos'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='residence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='lead.residence', verbose_name='Residence'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='room_quantity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='lead.roomquantity', verbose_name='Room quantity'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='videos',
            field=models.ManyToManyField(related_name='apartments', to='lead.Video', verbose_name='Videos'),
        ),
    ]
