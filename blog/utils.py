from .models import Notification

def send_notification(user, message, link=None):
    Notification.objects.create(user=user, message=message, link=link)
