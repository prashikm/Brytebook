# Generated by Django 3.1 on 2021-10-02 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20211001_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, default='cover/cover.png', max_length=200, null=True, upload_to='cover'),
        ),
    ]
