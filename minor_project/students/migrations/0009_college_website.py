# Generated by Django 5.1.2 on 2024-11-11 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_college_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='website',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
