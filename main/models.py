from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


class ReferralCode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="referral_code_user"
    )
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    used_by = models.ManyToManyField(
        User, related_name="used_referral_codes", blank=True
    )

    def deactivate_other_codes(self):
        ReferralCode.objects.filter(user=self.user, is_active=True).exclude(
            pk=self.pk
        ).update(is_active=False)

    def save(self, *args, **kwargs):
        # Если код активен, деактивируем другие активные коды
        if self.is_active:
            self.deactivate_other_codes()
        super().save(*args, **kwargs)
        # после сохранения объекта ReferralCode, очищаем кеш для этого пользователя.
        cache.delete(f"referral_code_{self.user_id}")

    def __str__(self):
        return f"Referral code for {self.user.username}"
