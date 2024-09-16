# Generated by Django 5.0.9 on 2024-09-12 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Donor'), (2, 'Hospital')], null=True),
        ),
    ]
