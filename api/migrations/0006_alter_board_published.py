# Generated by Django 4.2.8 on 2023-12-26 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_board_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='published',
            field=models.DateTimeField(null=True),
        ),
    ]
