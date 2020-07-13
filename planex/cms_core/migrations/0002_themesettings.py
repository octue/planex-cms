# Generated by Django 2.2.14 on 2020-07-12 15:33

import django.core.serializers.json
import django.db.models.deletion
import jsoneditor.fields.postgres_jsonfield
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("cms_core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ThemeSettings",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "theme",
                    jsoneditor.fields.postgres_jsonfield.JSONField(
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        help_text="Paste a JSON object containing material ui theme options",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False, on_delete=django.db.models.deletion.CASCADE, to="wagtailcore.Site"
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]