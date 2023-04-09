from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['hostname', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
