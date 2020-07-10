from django.contrib import admin
from .models import SitePage, Section, PageSectionsOrderable


admin.site.register(PageSectionsOrderable)
admin.site.register(SitePage)
admin.site.register(Section)
