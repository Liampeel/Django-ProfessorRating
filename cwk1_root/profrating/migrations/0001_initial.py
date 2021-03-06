# Generated by Django 3.0.4 on 2020-03-12 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('module_code', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Module Code')),
                ('module_name', models.CharField(max_length=30, verbose_name='Module Name')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('professor_id', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('semester', models.PositiveSmallIntegerField(choices=[[1, 1], [2, 2]])),
                ('rating', models.IntegerField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profrating.Module')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profrating.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4)),
                ('semester', models.PositiveSmallIntegerField(choices=[[1, 1], [2, 2]])),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profrating.Module')),
                ('professor', models.ManyToManyField(to='profrating.Professor')),
            ],
        ),
    ]
