from django.contrib.sitemaps import Sitemap
from .models import Article,UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Article)
def send_new_article_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Yangi maqola e’lon qilindi!',
            f'Yangi maqola: {instance.title}\nKo‘rish uchun: http://127.0.0.1:8000/article/{instance.id}/',
            'your-email@gmail.com',
            ['recipient-email@gmail.com'],
            fail_silently=False,
        )