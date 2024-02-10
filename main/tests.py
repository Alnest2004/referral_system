import pytest
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.urls import reverse
from main.models import ReferralCode, User
from main.services import ReferralCodeService
from django.core.cache import cache
from datetime import datetime, timedelta
from main.views import ReferralCodeView
from rest_framework import status
import asyncio

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


class ReferralCodeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test_user", email="test@example.com")
        self.referral_code = ReferralCode.objects.create(
            user=self.user, code="123", expiration_date="2024-12-31"
        )

    async def test_post_async(self):
        data = {
            "referral_code": self.referral_code.code,
            "username": "name_user",
            "password": "name_password",
            "email": "test@gmail.com",
        }
        response = await sync_to_async(self.client.post)(
            reverse("referral_code"), data=data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "User registered successfully."})

    async def test_get_async(self):
        response = await sync_to_async(self.client.get)(reverse("referral_code"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"error": "Email parameter is missing."}
        )

    async def test_get_referral_code_by_email_async(self):
        referral_code_obj = await self.get_referral_code_by_email("test@example.com")
        self.assertEqual(referral_code_obj, self.referral_code)

    async def get_referral_code_by_email(self, email):
        try:
            referrer = await sync_to_async(User.objects.get)(email=email)
            return await sync_to_async(ReferralCode.objects.get)(user=referrer)
        except ObjectDoesNotExist:
            return None
