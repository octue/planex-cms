from django.contrib import admin

from .models import AccreditedDocument, AccreditedImage, ParticlesConfiguration, SocialMediaSettings, ThemeSettings


admin.site.register(AccreditedDocument)
admin.site.register(AccreditedImage)
admin.site.register(ParticlesConfiguration)
admin.site.register(SocialMediaSettings)
admin.site.register(ThemeSettings)
