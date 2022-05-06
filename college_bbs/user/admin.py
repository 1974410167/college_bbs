from django.contrib import admin

# Register your models here.
from user.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    list_filter = ('name',)
    fields = ["name", "email", "phone"]
    search_fields = ('name',)


admin.site.register(UserProfile, UserProfileAdmin)
