# Generated by Django 5.0.9 on 2024-09-13 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0002_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='blood_virus_test',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Positive'), (2, 'Negative'), (3, 'Pending')]),
        ),
    ]
