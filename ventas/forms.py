from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente

class LoginForm(forms.Form):
    rut = forms.CharField(max_length=12, label='RUT')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class RegistroClienteForm(UserCreationForm):
    nombre = forms.CharField(max_length=30, required=True)
    apellido = forms.CharField(max_length=30, required=True)
    rut = forms.CharField(max_length=12, required=True)
    telefono = forms.CharField(max_length=12, required=True)

    class Meta:
        model = User
        fields = ('nombre', 'apellido', 'rut', 'telefono', 'password1', 'password2')

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.startswith('+569'):
            raise forms.ValidationError("El número de teléfono debe comenzar con +569")
        return telefono

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['rut']  # Usamos el RUT como nombre de usuario
        if commit:
            user.save()
            Cliente.objects.create(
                usuario=user,
                rut=self.cleaned_data['rut'],
                telefono=self.cleaned_data['telefono']
            )
        return user

class PedidoForm(forms.Form):
    # Aquí puedes agregar campos para seleccionar productos y cantidades
    pass

class CheckoutForm(forms.Form):
    TIPO_ENTREGA_CHOICES = [
        ('local', 'Retiro en local'),
        ('domicilio', 'Despacho a domicilio'),
    ]

    telefono = forms.CharField(max_length=12)
    tipo_entrega = forms.ChoiceField(choices=TIPO_ENTREGA_CHOICES, widget=forms.RadioSelect)
    direccion = forms.CharField(max_length=200, required=False)

    def clean(self):
        cleaned_data = super().clean()
        tipo_entrega = cleaned_data.get('tipo_entrega')
        direccion = cleaned_data.get('direccion')

        if tipo_entrega == 'domicilio' and not direccion:
            raise forms.ValidationError("La dirección es requerida para despacho a domicilio.")

        return cleaned_data

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'telefono']
