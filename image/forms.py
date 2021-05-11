from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

    def clean_url(self):
        url = self.cleaned_data['url']
        # valid_extensions = ['jpg', 'jpeg', 'png']
        # extension = url.rsplit('.', 1)[1].lower()
        # if extension not in valid_extensions:
        #     raise forms.ValidationError("The given url does not match valid image extension.")
        return url

    def save(self, commit=True, force_insert=False, force_update=False):
        image = super(ImageForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = f'{slugify(image.title)}.{image_url.rsplit(".", 1)[1].lower()}'
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image


class ImageUploadModelForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image', 'description')

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data['image']
        ext = image.name.split('.')[-1]
        if ext not in['jpg', 'jpeg', 'png', 'pdf', 'xlsx',]:
            raise forms.ValidationError('传输文件格式错误。')
        return image
