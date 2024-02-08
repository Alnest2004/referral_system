from django.contrib import admin

from main.models import ReferralCode


@admin.register(ReferralCode)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "expiration_date", "is_active")
    list_display_links = ("user", "code", "created_at", "expiration_date", "is_active")
    list_filter = ("user", "code", "created_at", "expiration_date", "is_active")
    search_fields = ("user", "code", "created_at", "expiration_date", "is_active")
    save_on_top = True
    save_as = True
