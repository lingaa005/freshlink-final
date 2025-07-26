from django.contrib import admin
from .models import (
    User,
    Producer,
    Vendor,
    Rating,
    VendorGroupChatMessage,
    ChatMessage
)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Producer, Vendor, Rating, VendorGroupChatMessage, ChatMessage



class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'fssai_license', 'flagged_review_count', 'reported_to_govt')
    search_fields = ('company_name', 'fssai_license')
    list_filter = ('reported_to_govt',)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_location')
    search_fields = ('user__username', 'street_location')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'producer', 'rating', 'is_safety_concern', 'created_at')
    list_filter = ('is_safety_concern', 'rating')
    search_fields = ('review',)

@admin.register(VendorGroupChatMessage)
class VendorGroupChatMessageAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'message', 'timestamp')
    search_fields = ('message', 'vendor__user__username')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'message', 'timestamp')
    search_fields = ('message', 'sender__username', 'receiver__username')
