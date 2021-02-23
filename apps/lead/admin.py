from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.lead.forms import DescriptionForm, ApartmentForm, VideoForm
from apps.lead.models import Residence, RoomQuantity, Photo, File, Apartment, Video


class DescriptionAdmin(admin.ModelAdmin):
    form = DescriptionForm


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm


class ApartmentAdmin(TranslationAdmin):
    form = ApartmentForm
    filter_horizontal = ('photos', 'videos', 'files')


admin.site.register(Residence, TranslationAdmin)
admin.site.register(RoomQuantity)
admin.site.register(Photo, DescriptionAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(File, DescriptionAdmin)
admin.site.register(Apartment, ApartmentAdmin)
