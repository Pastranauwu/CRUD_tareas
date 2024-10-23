from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Se crea el modelo para la base de datos de la aplicacion task
class Task(models.Model): 
    title = models.CharField(max_length=100) #texto de maximo 100 caracteres
    description = models.TextField(blank=True) #igual maneja texto y si no pasa nada el campo queda vacio
    created = models.DateField(auto_now_add=True)#campo de creacion para fecha que se generara automaticamente
    decompleted = models.DateField(null = True) #campo de finalizacion que por defecto es nula
    important = models.BooleanField(default=False) #campo de importancia por defecto ninguna es tan importante
    user = models.ForeignKey(User, on_delete= models.CASCADE)#usamos cascade para eliminar los datos si se elimina el usuario de la tabla principal

    def __str__(self):
        return self.title + ' -  de ' + self.user.username