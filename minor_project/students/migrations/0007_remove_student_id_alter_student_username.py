# Generated by Django 5.1.2 on 2024-11-11 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_remove_student_rank_alter_student_c_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]