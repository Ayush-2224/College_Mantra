# Generated by Django 5.1.2 on 2024-11-09 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_college_student_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='college_name',
            field=models.CharField(max_length=255),
        ),
    ]