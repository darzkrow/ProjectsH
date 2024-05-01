from django.shortcuts import render, redirect, get_object_or_404
from .models import Reventos

from django.utils import timezone

from .models import Person, AccessSEDE
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import date

from .forms import SearchForm, PersonForms, AccessForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def EvSeguridad(request):
    context = {
        'reventos': Reventos.objects.all()
    }
    return render(request,'sgsv/EvSeguridad.html', context) 



@login_required
def home(request):
    pcount = Person.objects.filter(is_deleted=0).count
    acount= AccessSEDE.objects.count()
    return render(request,'sgsv/person/index.html', {'pcount':pcount, 'acount':acount})


@login_required
def SearchPerson(request):

    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                person = Person.objects.get(dni=dni)
                return redirect('PersonDetail', person)
            except Person.DoesNotExist:
                request.session['dni_no_registrado'] = dni
                return redirect('cperson')
    else:
        form = SearchForm()
   
    return render(request, 'sgsv/person/search.html', { 'form': form})

# def SearchPerson(request):
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             dni = form.cleaned_data['dni']
#             try:
#                 person = Person.objects.get(dni=dni)
#                 return redirect('PersonDetail', person)
#             except Person.DoesNotExist:
#                 return redirect('cperson')
#     else:
#         form = SearchForm()
#     person = Person.objects.filter(is_deleted=0)
#     return render(request, 'sgv/lperson.html', {'person': person, 'form': form})

@login_required
def Cperson(request):
    if request.method == "POST":
        form = PersonForms(request.POST, request.FILES)
        if form.is_valid():
            new_person= form.save()
            return redirect('PersonDetail', dni=new_person.dni)
    else:
        form = PersonForms()
    return render(request, 'sgsv/person/cPerson.html', {'form': form})


@login_required
def PersonDetail(request,dni):
    person = get_object_or_404(Person, dni=dni)
    paccess = AccessSEDE.objects.filter(visitor=person).order_by('entry', 'hours')
    return render(request, 'sgsv/person/pdetail.html',{'person': person, 'paccess': paccess})

@login_required
def daccess(request,dni):
    person= get_object_or_404(Person, dni=dni)
    access = AccessSEDE.objects.filter(visitor=person)
    return render(request, 'sgsv/access/daccess.html', {'access': access, 'person': person})

@login_required
def detailaccess(request, access_id):
    try:
        access = AccessSEDE.objects.get(pk=access_id)  # Use get() for single object retrieval
    except AccessSEDE.DoesNotExist:
        # Handle the case where access_id is not found (e.g., display an error message)
        return HttpResponse("Access not found")
    context = {'access': access}
    return render(request, 'sgsv/access/detailaccess.html', context)

@login_required
def Eperson(request, dni):
    person = get_object_or_404(Person, dni=dni)
    if request.method == 'POST':
        form = PersonForms(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect('lperson')
    else:
        form = PersonForms(instance=person)
    return render(request, 'sgsv/person/eperson.html', {'form': form, 'person': person})


@login_required
def SoftdeletePerson(request, pk):
    person = get_object_or_404(Person, pk=pk)
    action_text = 'Restaurar' if person.is_deleted else 'Eliminar'
    if request.method == 'POST':
        if 'delete' in request.POST:
            person.is_deleted = 1
        elif 'restore' in request.POST:
            person.is_deleted = 0
        person.save()
        return redirect('lperson')  # Cambia esto a la URL deseada
    return render(request, 'sgsv/person/softdelete.html', {'person': person, 'action_text': action_text})

@login_required
def Tperson(request):
    person = Person.objects.filter(is_deleted=True)
    return render(request, 'sgsv/person/tperson.html', {'person': person})
@login_required
def lperson(request):
    person = Person.objects.filter(is_deleted=0)
    return render(request,'sgsv/person/lperson.html', {'person':person})

@login_required
def laccess(request):
    laccess = AccessSEDE.objects.all()

    return render(request, 'sgsv/access/laccess.html', {'laccess': laccess})


@login_required
def Eaccess(request, dni):
    access = get_object_or_404(AccessSEDE, pk=dni)
    if request.method == 'POST':
        form = AccessForm(request.POST, instance=access)
        if form.is_valid():
            form.save()
            return redirect('lperson')  # Reemplaza 'nombre_de_la_url_de_exito' con la URL a la que quieres redirigir después de la edición
    else:
        form = AccessForm(instance=access)
    return render(request, 'sgsv/access/daccess.html', {'form': form})


@login_required
def raccess(request, dni):
    person_access = get_object_or_404(Person, dni=dni)
    if request.method == "POST":
        form = AccessForm(request.POST)
        if form.is_valid():
            access = form.save(commit=False)
            now = timezone.localtime()
            # Verificar si la fecha y hora del acceso son iguales a la fecha y hora actuales
            if access.entry == now.date():
                access.visitor = person_access
                access.save()
                return redirect('PersonDetail', dni=person_access.dni)
            else:
                form.add_error(None, 'La fecha y la hora del acceso deben ser las actuales.')
    else:
        form = AccessForm()
    return render(request, 'sgsv/access/raccess.html', {'form': form, 'person_access': person_access})


@login_required
def reportexcel(request):
    accesses = AccessSEDE.objects.all().order_by('entry')

    # Crear un libro de trabajo y una hoja de cálculo
    wb = Workbook()
    ws = wb.active
    ws.title = "Accesos Hoy"

    # Agregar encabezados a la hoja de cálculo
    ws.append(['Fecha', 'Nombre y Apellido', 'Cedula','Oficina', 'Hora de Entrada', 'Hora de Salida', 'Observaciones'])

    # Agregar datos de accesos a la hoja de cálculo
    for access in accesses:
        ws.append([access.entry, 
                   access.visitor.first_name + ' ' + access.visitor.last_name, 
                   access.visitor.dni,
                   access.departaments, 
                   access.hours, 
                   access.hoursEx,
                   access.obs])

    # Crear la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="accesos_hoy.xlsx"'

    # Guardar el libro de trabajo en la respuesta HTTP
    wb.save(response)

    return response