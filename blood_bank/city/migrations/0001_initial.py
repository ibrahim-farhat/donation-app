# Generated by Django 5.0.9 on 2024-09-12 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
            ],
        ),
    ]
