# ProyectoFinal-Annie.nails.and.beauty_Appmovil-backend

API backend para la aplicación móvil "Annie Nails & Beauty" basada en FastAPI y MySQL.

**Descripción:**
- Backend REST construido con FastAPI que expone rutas para autenticación, gestión de usuarios, citas, servicios, empleados, trabajos, tutoriales y un dashboard estadístico.

**Estructura principal:**
- `main.py` : entrada de la aplicación.
- `app/routers/` : rutas / endpoints (autenticacion, usuario, cita, servicio, dashboard, etc.).
- `app/models/` : modelos Pydantic usados como `request`/`response_model`.
- `app/data/` : capa de acceso a datos (consultas SQL).
- `app/core/` : configuración, seguridad y conexión a base de datos.
- `annienails.sql` : volcado SQL para crear las tablas / datos iniciales.

**Requisitos (local):**
- Python 3.10+ (recomendado)
- MySQL (servidor) accesible desde la máquina donde ejecute la API
- Git (si subirás/eliminarás el repositorio)

**Dependencias típicas (pip):**
- `fastapi`
- `uvicorn[standard]`
- `mysql-connector-python`
- `python-jose[cryptography]`
- `passlib[bcrypt]`
- `python-multipart`

Puedes instalar TODO con (después de crear `requirements.txt` o manualmente):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install fastapi uvicorn[standard] mysql-connector-python python-jose[cryptography] passlib[bcrypt] python-multipart
```

**Configuración de la base de datos:**
- Crea una base de datos MySQL llamada `annienails` (o cambia el valor en `app/core/db.py`).
- Importa el archivo SQL con las tablas y datos iniciales:

```powershell
mysql -u root -p
# dentro del cliente mysql:
CREATE DATABASE annienails CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE annienails;
SOURCE .\annienails.sql;
EXIT;
```

(Sustituye `root` y contraseña por el usuario correcto.)

**Variables sensibles / configuración:**
- El secreto y algoritmo están en `app/core/configuracion.py`. Para producción, usa variables de entorno o un gestor de secretos en vez de mantener la clave en el código.

**Ejecutar la API (desarrollo) — PowerShell:**

```powershell
# desde la raíz del proyecto
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

**Rutas principales (ejemplos):**
- `POST /autenticacion/iniciar-sesion` — iniciar sesión (form: `username`, `password`).
- `POST /autenticacion/registrar` — registrar usuario.
- `GET /citas/` — listar citas.
- `GET /citas/{id}` — obtener cita por id.
- `POST /citas/` — crear cita.
- `PUT /citas/{id}` — actualizar cita (parcial si `CitaActualizar` es parcial).
- `PATCH /citas/{id}` — actualizar estado (requiere token admin).
- `GET /dashboard` — estadísticas (requiere token).

Para probar rutas protegidas, obtén `access_token` con `/autenticacion/iniciar-sesion` y añade el header:

```
Authorization: Bearer <access_token>
```

Si el `push` falla por autenticación, usa un PAT (token) o configura SSH.

**Contacto / Autor:**
- Proyecto por Annie (repo: `Annymoreno04/ProyectoFinal-Annie.nails.and.beauty_Appmovil-backend`).

---