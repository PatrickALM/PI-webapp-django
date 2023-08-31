# Generated by Django 4.2.4 on 2023-08-30 15:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='livrosdb',
            options={'verbose_name': 'Livro'},
        ),
        migrations.AddField(
            model_name='livrosdb',
            name='ano_de_publicacao',
            field=models.PositiveIntegerField(default=2023, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2023)]),
        ),
        migrations.AlterField(
            model_name='livrosdb',
            name='img_livro',
            field=models.BinaryField(blank=True),
        ),
    ]
