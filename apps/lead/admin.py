from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.lead.forms import DescriptionForm, ApartmentForm
from apps.lead.models import Residence, RoomQuantity, Photo, File, Apartment, Video


class DescriptionAdmin(admin.ModelAdmin):
    form = DescriptionForm


class ApartmentAdmin(TranslationAdmin):
    form = ApartmentForm
    filter_horizontal = ('photos', 'videos', 'files')


admin.site.register(Residence, TranslationAdmin)
admin.site.register(RoomQuantity)
admin.site.register(Photo, DescriptionAdmin)
admin.site.register(Video, DescriptionAdmin)
admin.site.register(File, DescriptionAdmin)
admin.site.register(Apartment, ApartmentAdmin)
