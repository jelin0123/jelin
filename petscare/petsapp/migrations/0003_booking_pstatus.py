# Generated by Django 5.0.1 on 2024-03-04 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petsapp', '0002_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='Pstatus',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]