# Generated by Django 5.0.1 on 2024-04-10 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0016_boardinghouse_map_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardinghouse',
            name='map_location',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]