from django.contrib import admin
from advertisements.models import Advertisement
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

admin.site.register(Advertisement)


# Чтобы удобно создавать токены для пользователей
class TokenInline(admin.StackedInline):
    model = Token
    max_num = 1
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    inlines = [TokenInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)