# Generated by Django 4.2.8 on 2024-01-03 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_rename_child_comment_boardchildcomment_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardchildcomment',
            old_name='comment',
            new_name='child_comment',
        ),
    ]
