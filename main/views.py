from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema

from main.models import ReferralCode
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from main.serializers import UserCreateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class ReferralCodeView(View):

    def post(self, request):
        referral_code = request.POST.get("referral_code")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if not all([referral_code, username, password, email]):
            return JsonResponse({"error": "Missing required parameters."}, status=400)

        try:
            owner_of_the_referral_code = ReferralCode.objects.get(code=referral_code)
            user_serializer = UserCreateSerializer(data=request.POST)
            if owner_of_the_referral_code and user_serializer.is_valid(
                raise_exception=True
            ):
                user = User.objects.create_user(
                    username=username, password=password, email=email
                )
                owner_of_the_referral_code.used_by.add(user)
                owner_of_the_referral_code.save()
                user.save()
                return JsonResponse({"success": "User registered successfully."})
            else:
                return JsonResponse(
                    {"error": "Invalid referral code for the given email."}, status=400
                )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"error": "Email parameter is missing."}, status=400)

        referral_code_obj = self.get_referral_code_by_email(email)
        if referral_code_obj:
            return JsonResponse({"referral_code": referral_code_obj.code})
        else:
            return JsonResponse(
                {"error": "Referral code not found for the specified email address."},
                status=404,
            )

    def get_referral_code_by_email(self, email):
        try:
            referrer = User.objects.get(email=email)
            return ReferralCode.objects.get(user=referrer)
        except ObjectDoesNotExist:
            return None


class ReferralListView(View):
    def get(self, request, referrer_id):
        try:
            referrer = User.objects.get(id=referrer_id)
            referral_code = ReferralCode.objects.get(user=referrer)
            used_users = referral_code.used_by.all()
            serialized_users = [
                {"username": user.username, "email": user.email} for user in used_users
            ]
            return JsonResponse({"used_users": serialized_users})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Referrer not found."}, status=404)
