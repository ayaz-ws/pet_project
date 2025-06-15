from django import forms


from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "nickname", "bio", "location"]
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'padding: 6px 10px;'
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш никнейм'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город, страна'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о себе...'
            }),
        }
