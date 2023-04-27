from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from .models import Privacy, Quiz

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    message="{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key
        )
    send_mail('Password Reset Token', message, settings.EMAIL_HOST_USER, [reset_password_token.user.email,])


@receiver(post_save, sender=Quiz)
def create_quiz_privacy(instance, sender, created, **kwargs):
    if created:
        Privacy.objects.create(
            quiz=instance,        
        )
