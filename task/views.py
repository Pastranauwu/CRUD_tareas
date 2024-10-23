# con get404 podemos buscar una elemento y mandar un error 404 si no se encontro
from django.shortcuts import render, redirect, get_object_or_404
# es para ejecutar cada que una ruta sea ejecutada
from django.http import HttpResponse
# esta importacion regresa un formulario ya preestablecido por django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# esta permite la creacion de usuarios y los guarda en la base de datos
from django.contrib.auth.models import User
# importamos las funciones para hacer login, logaout y autenticar a un usuario ya predefinidas
from django.contrib.auth import login, logout, authenticate
# importamos el formulario creado para nuestras tareas
from .forms import TaskForm
# importamos el modelo de tareas con los campos necesarios
from .models import Task
#importamos la libreria para marcar el tiempo exacto
from django.utils import timezone
#para proteger las demas rutas despues de logiar
from django.contrib.auth.decorators import login_required


# Create your views here.


"""
aqui definimos las funciones para llamar desde urls.py, es nuestra carpeta creada
con python manage.py startapp task por ello se llama task se pudo poner cualquier otro nombre
posteriormente definimos las funciones.

*crear una funcion tenemos dos formas*
1)

# def helloworld(request):
#     return HttpResponse('HOLA MUNDO') mandar un http respose y regresa desde un string hasta un html

2)
def home(request):
    return render(request, 'home.html') un render que dependiendo de la peticion podemos mandar directo un html

podemos utilizar los llamados del request para poder revisar si es una llamada GET o un POST (nos piden o envian datos al servidor)

por otra parte de la estrucutura debemos para poder almacenar los datos previamente cuando sale le mensaje de error de las
migraciones realizarlas 

3) 
def cerrarSesion(request):
    logout(request)
    return redirect('home')
con redirect podemos redireccionar a una pagina previamente creada 

*Diferencias entre los metodos render, redirect*
con render recargamos los elementos de la misma pagina o de otra especificada pero en la misma ruta
y con redirect nos desplazamos directamente a la otra ruta.


*Diferencias entre GET Y POST *
Para diferenciar que acciones debemos hacer si se estan pidiendo consultas al servidor o si se estan mandando datos
en este caso con el if request.method podemos comprobar si es 'GET' O 'POST'

*CRUD*
Para poder manejar las altas bajas y cambios podemos recurrir a from django.contrib.auth import login, logout, authenticate 
teniendo los metodos y formularios directamente.
Por otro lado para modificar los formularios definidos en los modelos de la base de datos que definimos, utilizar .save() .delete() nos ayuda a guardar
en la base sqlite que tenemos ya sea un nuevo objeto de un modelo ya definido y modificarlo o eliminarlo

"""


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                print("Recibiendo datos")
                print(request.POST)
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                print('guardado')
                login(request, user)
                return redirect('task')
            except Exception as e:
                print(
                    f"Ocurrió un error al intentar registrar el usuario: {e}")
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "El usuario ya existe"},
                )
        else:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "error": "Contraseñas no coinciden"},
            )

#se coloca el @login_required para proteger las rutas y queno puedan acceder al menos que exista un login previo
@login_required
def task(request):
    # llamamos a todas las tareas guardadas y filtradas
    tareas = Task.objects.filter(user=request.user, decompleted__isnull = True)
    return render(request, "tareas.html", {'task': tareas})


def home(request):
    return render(request, "home.html")


def cerrarSesion(request):
    logout(request)
    return redirect('home')


def signin(request):
    if (request.method == 'GET'):
        return render(request, "signin.html", {'form': AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if (user is None):
            return render(request, "signin.html", {'form': AuthenticationForm, 'error': 'Contraseña o usuario invalida'})
        else:
            login(request, user)
            return redirect('task')

@login_required
def created_task(request):
    if (request.method == 'GET'):
        return render(request, 'created_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('task')
        except ValueError:
            return render(request, 'created_task.html', {
                'form': TaskForm, 'error': 'Ingresa datos validos'
            })

@login_required
def task_detail(request, id):
    if (request.method == 'GET'):
            new_task = get_object_or_404(Task, pk=id, user= request.user)
            form = TaskForm(instance = new_task)
            print(id)
            return render(request, 'mostrarTarea.html', {'task': new_task, 'form': form})
    else:
        try:
            new_task = get_object_or_404(Task, pk=id, user=request.user)
            form = TaskForm(request.POST, instance=new_task)
            form.save()
            return redirect('task')
        except Exception as e:
            return render(request, 'mostrarTarea.html', {'task': new_task,  'form': form, 'error': 'Error en la actualizacion'})

@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if(request.method == 'POST'):
        task.decompleted = timezone.now()
        task.save()
    return redirect('task')

@login_required
def delated_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if(request.method == 'POST'):
        task.delete()
    return redirect('task')

@login_required
def task_completed(request):
    # llamamos a todas las tareas guardadas y filtradas
    tareas = Task.objects.filter(user=request.user, decompleted__isnull = False)
    return render(request, "tareas.html", {'task': tareas})