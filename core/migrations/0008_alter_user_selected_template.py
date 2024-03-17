# Generated by Django 5.0.1 on 2024-03-12 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_templateselection_alter_user_selected_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='selected_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.templateselection'),
        ),
    ]
