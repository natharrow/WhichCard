# Generated by Django 3.0.4 on 2020-05-13 19:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20200513_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]