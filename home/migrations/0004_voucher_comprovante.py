# Generated by Django 5.1.2 on 2024-10-12 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_voucher_saldo'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='comprovante',
            field=models.ImageField(blank=True, upload_to='comprovantes/'),
        ),
    ]
