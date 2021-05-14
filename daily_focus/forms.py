from django import forms
from daily_focus.models import Focus, FocusImage


class FocusForm(forms.ModelForm):
    class Meta:
        model = Focus
        fields = ('focus_content', 'focus_start', 'focus_end', 'line', 'station')
        widgets = {
            'focus_content': forms.Textarea(attrs={'class':'layui-input'}),
            'focus_line': forms.TextInput(attrs={'class':'layui-input'}),
            'focus_station': forms.TextInput(attrs={'class':'layui-input'}),
            'focus_start': forms.DateTimeInput(attrs={'class':'layui-input', 'type':'date'}),
            'focus_end': forms.DateTimeInput(attrs={'class':'layui-input', 'type':'date'}),
        }


class FocusImageForm(forms.ModelForm):
    class Meta:
        model = FocusImage
        fields = ('image', )
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class':'layui-input'})
        }