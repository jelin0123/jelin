# Generated by Django 5.0.1 on 2024-03-21 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petsapp', '0005_passwordreset'),
    ]

    operations = [
        migrations.CreateModel(
            name='complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=50)),
                ('Name', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
                ('Phone', models.IntegerField()),
                ('Complaint', models.CharField(max_length=500)),
            ],
        ),
    ]