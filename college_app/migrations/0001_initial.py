# Generated by Django 5.1.2 on 2024-11-16 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('College_ID', models.AutoField(primary_key=True, serialize=False)),
                ('College_Name', models.CharField(max_length=255)),
                ('College_Type', models.CharField(max_length=20)),
                ('Contact_No', models.CharField(max_length=15)),
                ('Location', models.CharField(max_length=255, null=True)),
                ('Email', models.EmailField(max_length=254)),
                ('Website', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'College',
            },
        ),
    ]
