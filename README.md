# AulaGram

Proyecto educativo tipo Instagram hecho con Django, SQLite y Tailwind CSS. La estructura prioriza que un estudiante pueda seguir el recorrido completo de una peticion: URL → vista → formulario → modelo → plantilla.

## Funcionalidades incluidas

- Registro, inicio y cierre de sesion.
- Usuario personalizado con roles: **Administrador**, **Creador** y **Usuario** (CR-01).
- Permisos aplicados en servidor y reflejados en la interfaz.
- Perfil editable, avatar y catalogo estandarizado de habilidades (CR-10).
- Feed, publicaciones con imagen, edicion y eliminacion.
- Likes sin duplicados y comentarios moderables.
- Panel administrativo de Django y pantalla sencilla para cambiar roles.
- Datos demo realistas: 10 cuentas, perfiles, avatares, 7 publicaciones, likes y conversaciones.

> La tabla recibida menciona CR-03 “Vacante”, pero tambien solicita un producto tipo Instagram. Esta Fase 1 implementa la base social y deja los modulos de proyectos/vacantes o actividades/torneos para una fase posterior, evitando mezclar tres dominios en los mismos modelos.

## Instalacion

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`. Todas las cuentas demo usan la contrasena `AulaGram2026!`. Ademas de las tres cuentas base, el comando crea siete perfiles sociales ficticios como `sofia.ramos`, `mateo.codes`, `vale.camina` y `luna.ceramica`:

- `admin_demo`: puede gestionar roles y moderar.
- `creador_demo`: muestra un rol intermedio para futuras capacidades.
- `estudiante_demo`: permisos normales.

`seed_demo` es idempotente: se puede ejecutar otra vez para recuperar datos faltantes sin duplicar publicaciones, likes o comentarios. Las fotos originales generadas para esta demo estan en `seed_assets/`.

Para usar `/admin/`, crea un superusuario:

```powershell
python manage.py createsuperuser
```

## Mapa de aprendizaje

| Concepto | Donde estudiarlo |
|---|---|
| Modelo de usuario y roles | `accounts/models.py` |
| Perfil creado automaticamente | `accounts/signals.py` |
| Registro y edicion con dos formularios | `accounts/forms.py`, `accounts/views.py` |
| Autorizacion en servidor | `accounts/views.py`, `posts/views.py` |
| Relaciones ForeignKey, OneToOne y ManyToMany | `accounts/models.py`, `posts/models.py` |
| Restriccion de like unico | `posts/models.py` |
| Carga y validacion de imagenes | `posts/forms.py` |
| ORM optimizado | funcion `feed` en `posts/views.py` |
| Tailwind y permisos de interfaz | carpeta `templates/` |
| Comandos personalizados | `accounts/management/commands/seed_demo.py` |
| Comportamiento esperado | `accounts/tests.py`, `posts/tests.py` |

## Fase 1 y siguientes pasos

Esta entrega cubre la infraestructura, autenticacion, CR-01 y la parte de perfil/habilidades de CR-10. El CRUD social sirve como caso practico completo. Un orden recomendable para continuar es:

1. Seguidores y feed solo de cuentas seguidas.
2. Notificaciones.
3. Recuperacion de contrasena y verificacion de correo.
4. API REST con Django REST Framework.
5. Si el dominio definitivo es reclutamiento, agregar `Project` y `Vacancy` (CR-03) como una aplicacion nueva; si es torneos, agregar `Activity`, estados y cupos en otra aplicacion.

## Tailwind CSS

Para que el aula no necesite Node, Tailwind se carga mediante CDN en `templates/base.html`. Es ideal para aprendizaje y desarrollo. Para produccion debe instalarse el CLI de Tailwind, compilar un CSS minimo y eliminar el script CDN.

## Pruebas

```powershell
python manage.py test
python manage.py check
```

SQLite (`db.sqlite3`) y las imagenes subidas se excluyen de Git para mantener limpio el repositorio.
