# Generated by Django 4.0.4 on 2022-04-16 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hku_id', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('location', models.CharField(max_length=150)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VisitingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_datetime', models.DateTimeField(null=True)),
                ('exit_datetime', models.DateTimeField(null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studysafe.member')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studysafe.venue')),
            ],
        ),
    ]
