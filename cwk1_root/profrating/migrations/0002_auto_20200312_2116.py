# Generated by Django 3.0.4 on 2020-03-12 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profrating', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profrating.Module'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='professor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profrating.Professor'),
        ),
    ]
