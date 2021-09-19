from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages
from .forms import ContactoForm, DireccionForm
from .models import *


def inicio(request):
	contactos = Contacto.objects.all().order_by('nombre') #Lista de contactos ordenada alfabeticamente por nombre
	context = {
		"titulo" : "Inicio", 
		"contactos" : contactos, 
		"size": len(contactos)
	}
	return render(request, "inicio.html", context)


def contacto_nuevo(request):
	if request.method == "POST":
		form = ContactoForm(request.POST, request.FILES) #crear modelform
		if form.is_valid(): #verficar form
			nuevo_contacto = form.save() #guardar contacto
			return redirect('contacto_editar', pk=nuevo_contacto.pk)
	else:
		form = ContactoForm()

	context = {
    	"titulo":"Registrar contacto",
    	"form":form
    }
	return render(request, "contacto_nuevo.html", context)


def contacto_editar(request, pk):

	contacto = get_object_or_404(Contacto, pk=pk)
	direccion = Direccion.objects.filter(contacto=pk)
	telefonos = Telefono.objects.filter(contacto=pk)
	#se utiliza inlineformset_factory debido a que se esta trabajando con objetos con llave foranea
	formset_telefono = inlineformset_factory(Contacto, Telefono, fields=("tipo", "alias", "numero"), can_delete=True, extra=0)

	if request.method == "POST":
		form_contacto = ContactoForm(request.POST, request.FILES, instance=contacto)
		if form_contacto.is_valid(): #validar form del contacto
			form_contacto.save() #actualizar

		if direccion.exists(): # la direccion existe, se debe actualizar
			direccion = direccion[0]
			form_direccion = DireccionForm(request.POST, instance=direccion)
			if form_direccion.is_valid():
				form_direccion.save()
		else: #la direccion no existe, se debe registrar
			form_direccion = DireccionForm(request.POST)
			direccion = form_direccion.save(commit = False)
			if form_direccion.is_valid():
				direccion.contacto = contacto
				direccion.save()

		form_telefono = formset_telefono(request.POST, instance=contacto)#pasar POST a formset de telefonos
		if form_telefono.is_valid(): #validar formset
			form_telefono.save() #guardar cambios
		messages.success(request, 'La información del contacto ha sido actualizada.')
	else:
		form_contacto = ContactoForm(instance=contacto)
		if direccion.exists():
			direccion = direccion[0]
			form_direccion = DireccionForm(instance=direccion)
		else:
			form_direccion = DireccionForm()
	
	form_telefono = formset_telefono(instance=contacto)
	
	context = {
    	"titulo":"Editar contacto",
    	"contacto": contacto,
    	"direccion": direccion,
    	"telefonos": [(index, telefonos[index]) for index in range(0, len(telefonos))],
    	"form_telefono": form_telefono,
    	"ESTADOS": ESTADOS,
    	"TIPOS_TELEFONO": TIPOS_TELEFONO,
    }
	return render(request, "contacto_editar.html", context)

def contacto_eliminar(request, pk):
	contacto = get_object_or_404(Contacto, pk=pk)
	contacto.delete()
	messages.success(request, 'El contacto fue eliminado.')
	return redirect('inicio')

def telefono_eliminar(request, pk):
	telefono = get_object_or_404(Telefono, pk=pk)
	contacto_pk = telefono.contacto.pk
	telefono.delete()
	messages.success(request, 'El teléfono fue eliminado.')
	return redirect('contacto_editar', pk=contacto_pk)