from django.test import TestCase
from django.contrib.auth.models import User
from main.models import ReferralCode
from main.services import ReferralCodeService
from django.core.cache import cache
from datetime import datetime, timedelta

# Тесты для проверки сервиса работы с реферальными кодами и кеширования

class ReferralCodeServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        expiration_date = datetime.now() + timedelta(days=7)
        self.referral_code = ReferralCode.objects.create(
            user=self.user, code="123", expiration_date=expiration_date
        )

    def test_get_referral_code_cached(self):
        cache.set(f"referral_code_{self.user.id}", self.referral_code.code)
        retrieved_code = ReferralCodeService.get_referral_code(self.user.id)
        self.assertEqual(retrieved_code, self.referral_code.code)

    def test_get_referral_code_not_cached(self):
        cache.delete(f"referral_code_{self.user.id}")
        retrieved_code = ReferralCodeService.get_referral_code(self.user.id)
        self.assertEqual(retrieved_code, self.referral_code.code)

        self.assertEqual(
            cache.get(f"referral_code_{self.user.id}"), self.referral_code.code
        )
