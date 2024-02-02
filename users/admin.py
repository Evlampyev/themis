from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', 'is_staff', 'is_active']


admin.site.unregister(User) # Unregister the default User
admin.site.register(User, UserAdmin) # Убрал таким образом поле e-mail, которое пока не используется
