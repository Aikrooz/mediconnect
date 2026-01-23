from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User,PatientProfileModel,DoctorProfileModel


class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password","role",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email","role","password1", "password2"),
            },
        ),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email","role","first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
admin.site.register(PatientProfileModel)
admin.site.register(DoctorProfileModel)
