from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('MainApp', '0002_alter_predictionhistory_heatmap_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregister',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
