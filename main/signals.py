from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import ReferralCode


# второй более интересный способ это обработчик сигнала,
# который вызывается перед сохранением каждого экземпляра модели "ReferralCode"
@receiver(pre_save, sender=ReferralCode)
def ensure_single_active_code(sender, instance, **kwargs):
    if instance.is_active:
        existing_active_codes = ReferralCode.objects.filter(
            user=instance.user, is_active=True
        ).exclude(pk=instance.pk)
        if existing_active_codes.exists():
            raise ValidationError("Only one active referral code allowed per user.")
