from django import forms
from django.core.exceptions import ValidationError

from apps.lead.models import Apartment


class DescriptionForm(forms.ModelForm):
    description_en = forms.CharField(required=False)
    description_ru = forms.CharField(required=False)
    description_uz = forms.CharField(required=False)


class VideoForm(DescriptionForm):
    video = forms.FileField()

    def clean_video(self):
        video = self.cleaned_data['video']
        file_type = video.name.split('.')[-1]

        if file_type not in ['avi', 'mp4', '3gp']:
            raise ValidationError('Invalid format')

        return video


class ApartmentForm(forms.ModelForm):
    def clean(self):
        data = self.cleaned_data

        similar_apartments = Apartment.objects.filter(room_quantity=data['room_quantity'], residence=data['residence'])
        if self.instance:
            similar_apartments = similar_apartments.exclude(id=self.instance.id)

        if similar_apartments:
            raise ValidationError('Apartment with that room_quantity and residence already exist')

        return super().clean()
