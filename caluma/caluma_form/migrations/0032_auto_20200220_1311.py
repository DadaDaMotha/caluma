# Generated by Django 2.2.10 on 2020-02-20 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("caluma_form", "0031_auto_20200220_0910")]

    operations = [
        migrations.AddField(
            model_name="document",
            name="source",
            field=models.ForeignKey(
                blank=True,
                help_text="Reference this document has been copied from",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="copies",
                to="caluma_form.Document",
            ),
        ),
        migrations.AddField(
            model_name="historicaldocument",
            name="source",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="Reference this document has been copied from",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="caluma_form.Document",
            ),
        ),
    ]
