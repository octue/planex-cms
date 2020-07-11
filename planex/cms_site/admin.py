from django.contrib import admin

from .models import PageSectionsOrderable, Section, SitePage


admin.site.register(PageSectionsOrderable)
admin.site.register(SitePage)
admin.site.register(Section)
