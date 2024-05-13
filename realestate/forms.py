from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Property, PropertyType, Neighborhood, Event


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Message')


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'description', 'address', 'property_type', 'price', 'neighborhood', 'area', 'balcony',
                  'status', 'image1', 'image2', 'image3', 'image4']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in $'}),
            'neighborhood': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'image', 'description']


class PropertyFilterForm(forms.Form):
    property_type = forms.ModelChoiceField(queryset=PropertyType.objects.all(), empty_label="All", required=False)
    neighborhood = forms.ModelChoiceField(queryset=Neighborhood.objects.all(), empty_label="All", required=False)
    price_range = forms.ChoiceField(choices=[
        ("", "All"),
        ("0-50000", "$0 - $50,000"),
        ("50000-100000", "$50,000 - $100,000"),
        ("100000-150000", "$100,000 - $150,000"),
        ("150000-200000", "$150,000 - $200,000"),
        ("200000-250000", "$200,000 - $250,000"),
        ("250000-300000", "$250,000 - $300,000"),
        ("300000-350000", "$300,000 - $350,000"),
        ("350000-400000", "$350,000 - $400,000"),
        ("400000-450000", "$400,000 - $450,000"),
        ("450000-500000", "$450,000 - $500,000"),
        ("500000+", "$500,000+"),
    ], required=False)


class ReportForm(forms.Form):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    year = forms.IntegerField(label='Select Year:')
    month = forms.ChoiceField(choices=MONTH_CHOICES, label='Select Month: ')


class ContactAgentForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.IntegerField()
    message = forms.CharField(widget=forms.Textarea)
