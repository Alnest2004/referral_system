from django.core.cache import cache

from main.models import ReferralCode


class ReferralCodeService:
    @staticmethod
    def get_referral_code(user_id):
        # Проверяем кеш для реферального кода
        referral_code = cache.get(f"referral_code_{user_id}")
        if referral_code is not None:
            return referral_code

        # Если не найдено в кеше, получаем из базы данных
        referral_code = ReferralCode.objects.get(user_id=user_id).code

        # Сохраняем в кеше
        cache.set(f"referral_code_{user_id}", referral_code)

        return referral_code
