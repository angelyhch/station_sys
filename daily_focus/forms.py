from django import forms
from daily_focus.models import Focus, Station, Line, FocusImage
import time
import datetime


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ('line', )


class FocusForm(forms.ModelForm):
    class Meta:
        model = Focus
        fields = ('focus_content', 'focus_start', 'focus_end',  'station')
        widgets = {
            'focus_content': forms.Textarea(attrs={'class':'layui-input'}),
            'focus_line': forms.TextInput(attrs={'class':'layui-input'}),
            'focus_station': forms.TextInput(attrs={'class':'layui-input'}),
            'focus_start': forms.DateTimeInput(attrs={'class':'layui-input', 'type':'date'}),
            'focus_end': forms.DateTimeInput(attrs={'class':'layui-input', 'type':'date'}),
        }

    initial = {
        'focus_start': datetime.datetime.today(),
    }


class FocusImageForm(forms.ModelForm):
    class Meta:
        model = FocusImage
        fields = ('image', )
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class':'layui-input'})
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        ext = image.name.split('.', 1)[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'gif']:
            raise forms.ValidationError('扩展名错误.')
        return image
