from django import forms
from .models import Lead, Activity, FollowUp


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'name',
            'email',
            'phone',
            'company',
            'source',
            'status',
            'score',
            'assigned_to',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter lead name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'source': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Lead score'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'activity_type',
            'description',
        ]

        widgets = {
            'activity_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter activity details...'
            }),
        }
        from .models import FollowUp


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ['scheduled_at', 'note', 'completed']

        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter follow-up notes'
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }