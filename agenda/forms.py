from django import forms
from .models import Contacto, Direccion, Telefono

class ContactoForm(forms.ModelForm):
	class Meta:
		model = Contacto
		fields = ('nombre', 'apellidos', 'fotografia' ,'fecha_nacio')

class DireccionForm(forms.ModelForm):
	class Meta:
		model = Direccion
		fields = ('calle', 'numero_exterior', 'numero_interior' ,'colonia', 'municipio', 'estado', 'referencias')