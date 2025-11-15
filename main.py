# main.py
 
# INSTALACIÓN DE DEPENDENCIAS:
#   1. Instalar Python 3.9+ y MySQL.
#   2. Instalar librerías necesarias:
#        pip install fastapi uvicorn mysql-connector-python
#
 
# ---------------------------------------------------------------
# EJECUCIÓN DEL SERVIDOR:
#   Iniciar el servidor con:
#        uvicorn main:app --reload --port 8001
#        uvicorn main:app --reload --host 10.130.224.72 --port 8001
#        uvicorn main:app --reload --host 0.0.0.0 --port 8001
#
#   Documentación automática disponible en:
#        http://127.0.0.1:8001/docs   (Swagger UI)
#        http://127.0.0.1:8001/redoc  (ReDoc)
#
 

       
from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware  
from app.routers import autenticacion, perfil,usuario, empleado, servicio, categoria_servicio, cita, trabajos, tutoriales, dashboard, horarios  

app = FastAPI(title="Gestión de Usuarios - Annie Nails")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En entorno de desarrollo se acepta cualquier origen; en producción se recomienda restringir
    allow_credentials=True, # Habilita el uso de cookies o autenticación
    allow_methods=["*"],    # Métodos HTTP permitidos
    allow_headers=["*"],    # Encabezados permitidos
)

 
app.include_router(autenticacion.router)

app.include_router(perfil.router)

app.include_router(usuario.router)

app.include_router(empleado.router)
 
app.include_router(servicio.router)

app.include_router(categoria_servicio.router)

app.include_router(cita.router) 

app.include_router(trabajos.router)

app.include_router(tutoriales.router)

app.include_router(dashboard.router)    

app.include_router(horarios.router)

