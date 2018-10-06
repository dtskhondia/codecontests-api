from __future__ import unicode_literals
from django.db import migrations


def create_initial_products(apps, schema_editor):
    Product = apps.get_model('api', 'Product')

    Product(name='Salame', description='Salame Toscano', price=12).save()
    Product(name='Olio Balsamico', description='Olio balsamico di Modena', price=10).save()
    Product(name='Parmigiano', description='Parmigiano Reggiano', price=8.50).save()
    Product(name='Olio', description='Olio Oliva Toscano', price=13).save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_products),
    ]