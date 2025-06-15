from django import forms

from .models import ChatMessage


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Введите сообщение...',
                'class': 'form-control'
            }),
        }
        labels = {
            'body': ''
        }
