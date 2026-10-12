from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Photo, Profile, Project, Skill, THEMES


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. Letters, numbers and spaces are allowed.'

    def clean_username(self):
        username = ' '.join(self.cleaned_data['username'].split())
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('That username is already taken.')
        return username

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        exclude.add('username')
        return exclude


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'tagline', 'course', 'school', 'email',
                  'bio', 'avatar', 'theme_color']
        labels = {
            'full_name': 'Full name',
            'tagline': 'Tagline',
            'avatar': 'Profile photo',
            'theme_color': 'Theme color',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
            'theme_color': forms.RadioSelect(choices=THEMES),
            'tagline': forms.TextInput(attrs={'placeholder': 'e.g. Aspiring web developer'}),
            'course': forms.TextInput(attrs={'placeholder': 'e.g. BS Information Technology'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']
        labels = {'name': 'Skill', 'level': 'How good are you? (0-100)'}
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Python'}),
            'level': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 5}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'tech', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Student Portfolio'}),
            'description': forms.TextInput(attrs={'placeholder': 'What does it do?'}),
            'tech': forms.TextInput(attrs={'placeholder': 'e.g. Django, CSS'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. School event'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }   