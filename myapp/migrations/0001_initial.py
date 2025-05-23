# Generated by Django 5.2.1 on 2025-05-15 01:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_conta', models.CharField(max_length=100)),
                ('valor', models.FloatField()),
                ('data_vencimento', models.DateField()),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('nome', models.CharField(max_length=100)),
                ('idade', models.IntegerField()),
                ('telefone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Republica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_pago', models.FloatField()),
                ('data_pagamento', models.DateField(auto_now_add=True)),
                ('forma_pagamento', models.CharField(max_length=50)),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagamentos', to='myapp.conta')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagamentos', to='myapp.pessoa')),
            ],
        ),
        migrations.AddField(
            model_name='pessoa',
            name='republica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pessoas', to='myapp.republica'),
        ),
        migrations.AddField(
            model_name='conta',
            name='republica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas', to='myapp.republica'),
        ),
    ]
