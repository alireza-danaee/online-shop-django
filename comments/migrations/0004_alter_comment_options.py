# Generated by Django 4.0 on 2022-04-23 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_rename_post_comment_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_on'], 'verbose_name': 'نظر', 'verbose_name_plural': 'نظرات'},
        ),
    ]