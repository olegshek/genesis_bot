from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.information.forms import InformationTextForm
from apps.information.models import InformationText, InformationFile, InformationPhoto, InformationVideo


class InformationTextAdmin(TranslationAdmin):
    form = InformationTextForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(InformationText, InformationTextAdmin)
admin.site.register(InformationFile)
admin.site.register(InformationPhoto)
admin.site.register(InformationVideo)
