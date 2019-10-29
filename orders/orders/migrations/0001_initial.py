# Generated by Django 2.2.6 on 2019-10-29 15:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('code', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=200)),
                ('location_id', models.IntegerField()),
                ('state', models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddIndex(
            model_name='session',
            index=models.Index(fields=['location_id'], name='orders_sess_locatio_277a05_idx'),
        ),
        migrations.AddIndex(
            model_name='session',
            index=models.Index(fields=['state'], name='orders_sess_state_b717c3_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together={('name', 'location_id')},
        ),
        migrations.AddField(
            model_name='order',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Session'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['session'], name='orders_orde_session_aeca3b_idx'),
        ),
    ]
