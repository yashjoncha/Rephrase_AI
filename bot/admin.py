from django.contrib import admin

from .models import TelegramUser, Translation


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "first_name", "last_name", "language_code", "first_seen", "last_seen")
    search_fields = ("username", "first_name", "last_name")
    readonly_fields = ("first_seen", "last_seen")


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ("user", "original_text", "translated_text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "original_text", "translated_text")
    readonly_fields = ("created_at",)
