# Generated by Django 4.2.2 on 2023-06-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_mail_customer_email'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='customer',
            name='store_custo_last_na_2e448d_idx',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='colleetion',
            new_name='collection',
        ),
        migrations.RemoveField(
            model_name='address',
            name='zip',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Failed')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='promotions',
            field=models.ManyToManyField(to='store.promotion'),
        ),
    ]
