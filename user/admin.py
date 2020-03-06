from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Review

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    list_display = ('username','email','first_name','last_name','get_company','is_active')
    list_editable = ('is_active',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list() # Returns empty list
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_company(self, obj):
        return obj.profile.company
    get_company.admin_order_field  = 'company'
    get_company.short_description = 'Company'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Review)
