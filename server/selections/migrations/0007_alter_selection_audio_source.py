from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("selections", "0006_alter_audiosource_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="selection",
            name="audio_source",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="selections.audiosource",
            ),
        ),
    ]
