# CRUD de Tareas (Django)

Aplicación Django para gestionar tareas con autenticación de usuarios: crear, listar, completar y eliminar tareas.

## Requisitos
- Python 3.13 (o compatible con Django 5.1)
- pip

Opcional (solo producción):
- Base de datos Postgres disponible vía `DATABASE_URL`

## Configuración rápida (local)

1) Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

2) Instalar dependencias

```bash
pip install -r requirements.txt
```

3) Migraciones y archivos estáticos

```bash
python manage.py migrate
python manage.py collectstatic --no-input
```

4) Ejecutar el servidor de desarrollo

```bash
# Puedes escuchar en localhost
python manage.py runserver

# O escuchar en todas las interfaces (útil en contenedores o LAN)
python manage.py runserver 0.0.0.0:8000
```

5) Abrir en el navegador
- Local: http://127.0.0.1:8000
- En red: http://<tu-ip-lan>:8000

Nota: 0.0.0.0 es solo la dirección de escucha, no la abras en el navegador.

## Usuarios y admin
- Para crear un superusuario (admin):

```bash
python manage.py createsuperuser
```

- Panel admin: http://127.0.0.1:8000/admin

## Variables de entorno
- `SECRET_KEY`: clave secreta de Django (por defecto usa una de desarrollo)
- `DATABASE_URL`: si está definida, se usa Postgres (por ejemplo `postgresql://usuario:pass@host:puerto/dbname`). Si no está, se usa SQLite local (`db.sqlite3`).
- `RENDER_EXTERNAL_HOSTNAME`: si despliegas en Render, se añade automáticamente a `ALLOWED_HOSTS`.

## Cómo funciona

### Apps y rutas
- App principal: `task`
- Rutas definidas en `listaTareas/urls.py` que apuntan a `task/views.py`:
  - `/` → `home`
  - `/signup/` → registro de usuario
  - `/signin/` → inicio de sesión
  - `/logout/` → cerrar sesión
  - `/task/` → lista de tareas activas (requiere login)
  - `/task_completed/` → lista de tareas completadas (requiere login)
  - `/task/create/` → crear tarea (requiere login)
  - `/task/<id>/` → detalle/edición de tarea (requiere login)
  - `/task/<id>/complete/` → marcar como completada (POST; requiere login)
  - `/task/<id>/delated/` → eliminar (POST; requiere login)
  - `/admin/` → panel de administración

### Modelo
- `Task` (`task/models.py`):
  - `title` (CharField)
  - `description` (TextField, opcional)
  - `created` (DateField, auto_now_add)
  - `decompleted` (DateField, puede ser nulo; indica completada)
  - `important` (BooleanField)
  - `user` (ForeignKey a `auth.User`)

### Formularios
- `TaskForm` (`task/forms.py`): ModelForm para crear/editar `Task` con campos `title`, `description`, `important`.

### Vistas clave
- Autenticación con formularios de Django (`UserCreationForm`, `AuthenticationForm`).
- Rutas protegidas con `@login_required`.
- CRUD de tareas: crear (`created_task`), editar (`task_detail`), completar (`complete_task`), eliminar (`delated_task`).

## Despliegue
- Usa `build.sh` para preparar el entorno (instala dependencias, `collectstatic`, `migrate`).
- En producción, define `DATABASE_URL` y `SECRET_KEY` y usa un servidor como Gunicorn/Uvicorn detrás de un proxy. Ejemplo (Gunicorn):

```bash
gunicorn listaTareas.wsgi:application --bind 0.0.0.0:8000
```

## Problemas comunes
- DisallowedHost con `0.0.0.0`: navega con `127.0.0.1` o tu IP LAN; `0.0.0.0` es solo la dirección de escucha. `ALLOWED_HOSTS` incluye `localhost`, `127.0.0.1` y `0.0.0.0` por conveniencia.
- Error de Postgres en local: el proyecto ahora usa SQLite si no hay `DATABASE_URL`.
- VS Code marca `dj_database_url` como no resuelto: selecciona el intérprete del venv (`venv/bin/python`).
