# Generated by Django 5.0.1 on 2024-03-23 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0008_booking_owner_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='boarding_house',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Website.boardinghouse'),
        ),
    ]
