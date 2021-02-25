from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.lead.forms import DescriptionForm, ApartmentForm, VideoForm
from apps.lead.models import Residence, RoomQuantity, Photo, File, Apartment, Video, Customer, Lead, Feedback


class DescriptionAdmin(admin.ModelAdmin):
    form = DescriptionForm


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm


class ApartmentAdmin(TranslationAdmin):
    form = ApartmentForm
    filter_horizontal = ('photos', 'videos', 'files')


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CustomerAdmin(ReadOnlyAdmin):
    list_display = ('id', 'phone_number', 'full_name')


class LeadAdmin(ReadOnlyAdmin):
    list_display = (
        'number', 'customer'
    )


admin.site.register(Residence, TranslationAdmin)
admin.site.register(RoomQuantity)
admin.site.register(Photo, DescriptionAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(File, DescriptionAdmin)
admin.site.register(Apartment, ApartmentAdmin)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Feedback, LeadAdmin)
