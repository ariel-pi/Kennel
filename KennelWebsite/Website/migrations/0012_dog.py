# Generated by Django 5.0.1 on 2024-04-09 14:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0011_review'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('chip_id', models.CharField(help_text='Unique identifier, auto-generated', max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='CHIPID')),
                ('dog_name', models.CharField(max_length=20, verbose_name="Dog's name")),
                ('medicines', models.CharField(max_length=80, verbose_name="Dog's medicines")),
                ('vaccination', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], help_text='User type selection (yes/no)', max_length=3, verbose_name='Vaccination')),
                ('age', models.IntegerField(verbose_name="Dog's age")),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], help_text='User type selection (male/female)', max_length=8, verbose_name='Gender')),
                ('race', models.CharField(max_length=20, verbose_name="Dog's race")),
                ('weight', models.IntegerField(verbose_name="Dog's weight")),
                ('social_level', models.CharField(max_length=100, verbose_name="Dog's social level")),
                ('walking_requirements', models.CharField(max_length=100, verbose_name="Dog's walking requirements")),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
        ),
    ]
