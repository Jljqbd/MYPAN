# Generated by Django 2.2.3 on 2020-03-22 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestWebapp', '0002_auto_20200322_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='id',
        ),
        migrations.AlterField(
            model_name='people',
            name='Pno',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]