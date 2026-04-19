from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Complaint, ComplaintRemark, ComplaintRating

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('role', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Fields', {'fields': ('role', 'avatar')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Complaint)
admin.site.register(ComplaintRemark)
admin.site.register(ComplaintRating)
