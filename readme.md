# 🧠 Task Manager API – FastAPI + JWT + SQLite

Una API RESTful de gestión de tareas hecha con **FastAPI**, con autenticación mediante **JWT**, base de datos con **SQLite** y desplegable fácilmente en **Render**.

## 🚀 Características principales

✅ Registro e inicio de sesión de usuarios  
✅ Tokens JWT para autenticación segura  
✅ CRUD completo de tareas  
✅ Cada usuario sólo accede a sus propias tareas  
✅ Base de datos con SQLAlchemy (SQLite por defecto)  
✅ Proyecto listo para producción y despliegue gratuito

---

## 📁 Estructura del proyecto

ask-manager-api/
├── app/
│ ├── main.py # Punto de entrada
│ ├── models.py # Modelos de SQLAlchemy
│ ├── schemas.py # Esquemas de Pydantic
│ ├── auth.py # JWT y auth
│ ├── database.py # Conexión a la BD
│ ├── routes/
│ │ ├── users.py # Registro y login
│ │ └── tasks.py # Endpoints de tareas
├── start.sh # Script para Render
├── requirements.txt # Dependencias
├── .env # Variables de entorno
├── .gitignore
└── README.md


---

## 🧪 Rutas de la API

### 🔐 Autenticación
- `POST /register` – Registro de usuario
- `POST /login` – Login (devuelve token JWT)

### ✅ Tareas (autenticación requerida)
- `GET /tasks/` – Ver tareas del usuario actual
- `POST /tasks/` – Crear nueva tarea
- `PUT /tasks/{id}` – Editar tarea
- `DELETE /tasks/{id}` – Eliminar tarea

> 🔒 Usa el token JWT en el header:
>  
> `Authorization: Bearer <token>`

---

## 🧑‍💻 Instalación local

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/JJMMC/task-manager-api]
   cd task-manager-api

2. Crea y activa el entorno virtual:
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instala dependencias:
   pip install -r requirements.txt

4. Crea el archivo .env:
   SECRET_KEY=clave_secreta_segura
   DATABASE_URL=sqlite:///./tasks.db

5. Ejecuta la app:
   uvicorn app.main:app --reload

## 🔍 Pruebas con Pytest
✅ Ejecuta pruebas básicas con:
    - pytest
✅ Puedes agregar tus tests en archivos tipo test_*.py en la raíz o carpeta tests/.


## 🌐 Despliegue en Render
✅Sube el proyecto a un repositorio GitHub.

✅Crea una cuenta en https://render.com.

✅Conecta tu repo y crea un nuevo "Web Service".

✅Configura:

    - Start Command: ./start.sh

    - Runtime: Python 3.11+

    - Environment Variables: define SECRET_KEY, etc.

¡Listo! Render lo construye y lo despliega automáticamente.


## 📘 Tecnologías usadas
 - FastAPI

 - SQLAlchemy

 - SQLite

 - PyJWT (jose)

 - Passlib

 - Uvicorn

✨ Autor
[JJMMC]








python3 -m app.main #regeneramos la DB

uvicorn app.main:app --reload                         
