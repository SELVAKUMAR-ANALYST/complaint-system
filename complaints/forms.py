from django import forms
from .models import Complaint, ComplaintRemark, ComplaintRating

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'category', 'description', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-premium', 'placeholder': 'e.g., Laptop Screen Flickering'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-premium', 'rows': 4, 'placeholder': 'Describe your issue in detail...'}),
            'category': forms.RadioSelect(attrs={'class': 'd-none'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control form-control-premium', 'accept': '.jpg,.jpeg,.png,.pdf,.doc,.docx,.xlsx,.txt'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = ComplaintRating
        fields = ['stars', 'feedback']
        widgets = {
            'stars': forms.HiddenInput(attrs={'id': 'rating-stars-input'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control form-control-premium', 'rows': 3, 'placeholder': 'Share your experience (optional)...'}),
        }
