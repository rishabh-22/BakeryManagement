# Generated by Django 3.1.7 on 2021-03-11 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('quantity', models.CharField(max_length=50)),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('quantity', models.IntegerField()),
                ('cost_price', models.FloatField()),
                ('sell_price', models.FloatField()),
                ('mfg_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('ingredients', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Items',
            },
        ),
    ]
