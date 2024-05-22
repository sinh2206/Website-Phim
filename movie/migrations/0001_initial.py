# Generated by Django 5.0.6 on 2024-05-22 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=100)),
                ('actors', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('rating', models.FloatField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_url', models.URLField()),
                ('category', models.CharField(choices=[('popular', 'Popular'), ('new', 'New')], default='popular', max_length=50)),
            ],
        ),
    ]
