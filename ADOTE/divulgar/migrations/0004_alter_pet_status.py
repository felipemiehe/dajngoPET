# Generated by Django 4.1.5 on 2023-01-15 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divulgar', '0003_pet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='status',
            field=models.CharField(choices=[('P', 'Para adoção'), ('A', 'Adotado')], default='P', max_length=1),
        ),
    ]
