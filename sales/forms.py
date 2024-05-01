from django import forms

from .models import Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizaciones aquí
