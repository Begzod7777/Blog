# Generated by Django 5.1.7 on 2025-03-10 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_category_article_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='ads/')),
                ('link', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
