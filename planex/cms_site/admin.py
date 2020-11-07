from django.contrib import admin

from .models import PageSectionsOrderable, Section, SectionsPage


admin.site.register(PageSectionsOrderable)
admin.site.register(SectionsPage)
admin.site.register(Section)
