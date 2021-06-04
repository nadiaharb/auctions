# Generated by Django 3.2.1 on 2021-05-29 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_activelistings_newlisting_watchlist_watchlistitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newlisting',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.activelistings')),
            ],
        ),
    ]