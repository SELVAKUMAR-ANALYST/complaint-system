from django import forms
from .models import Complaint, ComplaintRemark

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'category', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-premium', 'placeholder': 'e.g., Laptop Screen Flickering'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-premium', 'rows': 4, 'placeholder': 'Describe your issue in detail...'}),
            'category': forms.RadioSelect(attrs={'class': 'd-none'}),
        }
