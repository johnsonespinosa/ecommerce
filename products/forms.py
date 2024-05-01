from django import forms

from products.models import Category, Supplier, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }


class ProductSearchForm(forms.Form):
    name = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)
