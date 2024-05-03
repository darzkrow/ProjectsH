from django import forms
from django.core.validators import RegexValidator
from .models import Person, AccessSEDE, Reventos



class EventForm(forms.ModelForm):
    class Meta:
        model = Reventos
        fields = ['nEvent','nDate','nTime','nLocation','nDescription']
        widgets = {
            'nDate': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'nTime': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'nDescriptions':forms.Textarea(attrs={'style': 'height: 80px;'})
          }


class SearchForm(forms.Form):
    dni = forms.CharField(widget=forms.HiddenInput())
    dni = forms.CharField(label='Buscar por Numero de Cedula:', max_length=10)
    fields = ['dni']
    widgets = {
        'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
    }


class PersonForms(forms.ModelForm):
    dni_validator = RegexValidator(r'^\d{6,10}$', 'Ingrese solo números válidos con un mínimo de 6 dígitos.')
    name_validator = RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$', 'Ingrese solo letras válidas para el nombre.')

    class Meta:
        model = Person
        fields = ['nac', 'dni', 'first_name', 'last_name', 'gender']
        widgets = {
            'nac': forms.Select(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dni'].validators.append(self.dni_validator)
        self.fields['first_name'].validators.append(self.name_validator)
        self.fields['last_name'].validators.append(self.name_validator)

        # Deshabilitar los campos Dni y photo si ya existe una instancia
        if self.instance.pk:
            self.fields['dni'].disabled = True
          
    # Sobrescribe el método clean para mostrar errores personalizados
    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get('dni')
        if dni and not dni.isdigit():
            self.add_error('dni', 'Ingrese solo números válidos con un mínimo de 6 dígitos.')
        return cleaned_data
    

class AccessForm(forms.ModelForm):
    class Meta:
        model = AccessSEDE
        fields =  ['entry','hours','hoursEx','departaments','obs']
        widgets = {
            'entry': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'hours': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hoursEx': forms.TimeInput(attrs={'type': 'time','class': 'form-control'}),
            'departaments': forms.Select(attrs={'class': 'form-control'}),
           
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
           
        }

