# Generated by Django 4.2.5 on 2023-09-21 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('videolink', models.FilePathField()),
                ('duration', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('lessons', models.ManyToManyField(to='study.lessons')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('surname', models.TextField()),
                ('products', models.ManyToManyField(to='study.products')),
            ],
        ),
        migrations.CreateModel(
            name='StudentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed', models.TimeField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.lessons')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.students')),
            ],
        ),
    ]
