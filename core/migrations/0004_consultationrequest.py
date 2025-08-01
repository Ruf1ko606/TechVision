# Generated by Django 5.2.4 on 2025-07-31 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_project_challenge_project_outcome_project_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='Имя и Отчество')),
                ('company_name', models.CharField(max_length=200, verbose_name='Название компании')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Заявка обработана')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.service', verbose_name='Запрошенная услуга')),
            ],
            options={
                'verbose_name': 'Заявка на консультацию',
                'verbose_name_plural': 'Заявки на консультацию',
                'ordering': ['-created_at'],
            },
        ),
    ]
