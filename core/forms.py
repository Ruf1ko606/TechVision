from django import forms
# Убедись, что мы импортируем ОБЕ модели
from .models import ContactMessage, ConsultationRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'E-mail для ответа',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Ваш вопрос или сообщение',
                'rows': 10,
                'required': 'required'
            }),
        }

# ВОТ ФОРМА, КОТОРУЮ НЕ УДАЛОСЬ НАЙТИ
class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        # Мы берем только те поля, которые заполняет пользователь
        fields = ['full_name', 'company_name', 'phone_number', 'email']


