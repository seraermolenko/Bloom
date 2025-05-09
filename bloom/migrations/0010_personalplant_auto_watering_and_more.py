# Generated by Django 5.1.4 on 2025-05-04 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloom', '0009_personalplant_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalplant',
            name='auto_watering',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='personalplant',
            name='last_watered',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='personalplant',
            name='status',
            field=models.CharField(choices=[('Happy', 'Happy'), ('Thirsty', 'Thirsty'), ('Wet', 'Wet')], max_length=20, null=True),
        ),
    ]
