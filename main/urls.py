from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from main import api
from main.views import ReferralCodeView, ReferralListView

router = routers.DefaultRouter()
router.register(r"users", api.UserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "referral-code/",
        ReferralCodeView.as_view(),
        name="referral_code",
    ),
    path(
        "referrals/<int:referrer_id>/", ReferralListView.as_view(), name="referral_list"
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
