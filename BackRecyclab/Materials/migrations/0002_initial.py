# Generated by Django 4.1.13 on 2024-04-30 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('Materials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmation',
            name='collector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.collector'),
        ),
        migrations.AddField(
            model_name='confirmation',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Materials.transaction'),
        ),
    ]
