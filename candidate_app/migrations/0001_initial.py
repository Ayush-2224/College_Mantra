# Generated by Django 5.1.2 on 2024-11-16 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('Candidate_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Phone', models.CharField(max_length=15)),
                ('Roll_No', models.CharField(max_length=15, unique=True)),
                ('Candidate_Name', models.CharField(max_length=255)),
                ('Gender', models.CharField(max_length=15)),
                ('DOB', models.DateField()),
                ('Candidate_Rank', models.IntegerField()),
                ('XII_Percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Category', models.CharField(max_length=15)),
                ('Nationality', models.CharField(max_length=15)),
                ('Address', models.CharField(max_length=255)),
                ('Email', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'Candidate',
            },
        ),
    ]
