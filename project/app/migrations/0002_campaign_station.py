# Generated by Django 4.2.2 on 2023-07-16 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='station',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.station'),
            preserve_default=False,
        ),
    ]