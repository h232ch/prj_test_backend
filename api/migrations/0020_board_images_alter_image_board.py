# Generated by Django 4.2.8 on 2024-01-07 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_board_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='board_images', to='api.image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_images', to='api.board'),
        ),
    ]
