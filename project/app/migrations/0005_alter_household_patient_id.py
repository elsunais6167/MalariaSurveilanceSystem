# Generated by Django 4.2.2 on 2023-07-22 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_campaign_campreport_campaign_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='patient_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient', unique=True),
        ),
    ]
