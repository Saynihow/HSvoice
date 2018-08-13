from django import forms
from django.forms import BaseModelFormSet
from django.contrib.auth.models import User
from django.apps import apps
Image = apps.get_model('hearthstone', 'Image')
Voice = apps.get_model('hearthstone', 'Voice')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密碼', widget=forms.PasswordInput)
    password2 = forms.CharField(label='重複密碼', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ["author"]

class Voiceform(forms.ModelForm):
    class Meta:
        model = Voice
        exclude = ["author"]

    def __init__(self, request, *args, **kwargs):
        super(Voiceform, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(author=request.user)

class VoiceUpdateform(forms.ModelForm):
    class Meta:
        model = Voice
        exclude = ["author","image","file_type","publish"]
    '''
    def __init__(self, request, id, *args, **kwargs):
        super(VoiceUpdateform, self).__init__(*args, **kwargs)
        self.queryset = Voice.objects.get(id=id)

    def save(self, commit=True):
        instance = super(VoiceUpdateform, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    '''



