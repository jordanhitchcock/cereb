from django.contrib import admin

from .models import Visitors

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'template_name', 'visit_dt', 'ip', 'signup_email', 'contact_name', 'contact_email', 'contact_content')

admin.site.register(Visitors, VisitorAdmin)
