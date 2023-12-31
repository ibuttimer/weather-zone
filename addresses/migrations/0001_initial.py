# Generated by Django 4.2.3 on 2023-08-28 15:04

import addresses.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('components', addresses.models.CompressedJsonTextField(max_length=500, verbose_name='Address components')),
                ('formatted_addr', models.CharField(max_length=250, verbose_name='Formatted address')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('is_default', models.BooleanField(default=False, help_text="Designates that this record represents the user's default address.", verbose_name='default')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-is_default'],
                'unique_together': {('latitude', 'longitude')},
            },
            bases=(utils.models.ModelMixin, models.Model),
        ),
    ]
