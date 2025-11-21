🚀 Módulo de Gestión de Tareas – Backend (Django + DRF + PostgreSQL + Docker + Nginx)
Este proyecto es un backend profesional para un módulo de gestión de tareas (similar a Jira).
Está construido con:
•	Django 5
•	Django REST Framework
•	PostgreSQL
•	Docker + Docker Compose
•	Gunicorn
•	Nginx (reverse proxy)
•	Swagger (Documentación API)
Incluye:
•	Backlog (Historias de usuario)
•	Sprint Board (Kanban)
•	Cards
•	Miembros
•	Columns
•	Templates
•	Checklist
•	Dashboard / Métricas
•	Autenticación
•	Configuración de producción
________________________________________
📦 Requisitos
Antes de ejecutar este proyecto, asegúrate de tener instalado:
•	Docker → https://www.docker.com/products/docker-desktop
•	Docker Compose (ya viene con Docker Desktop)
No necesitas instalar Python ni Postgres en tu PC.
Todo corre dentro de contenedores.
________________________________________
📁 Estructura del Proyecto
task_management/
│── backlog/                  # App de historias y plantillas
│── sprint/                   # App del tablero Kanban (sprints)
│── core/                     # Configuración principal (settings, urls)
│── deploy/                   # Configuración de Nginx
│   └── nginx.conf
│── static/                   # Archivos estáticos (se generan solos)
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
│── manage.py
________________________________________
▶️ Cómo ejecutar el proyecto
1. Clonar el repositorio
git clone https://github.com/tu-usuario/tu-repo.git
cd task_management
2. Crear los contenedores
docker-compose up --build -d
Esto construye 3 contenedores:
Contenedor	Función
db	Base de datos PostgreSQL
web	Django + Gunicorn
nginx	Reverse proxy para servir la API y los estáticos
________________________________________
🔐 3. Crear un superusuario (admin)
docker-compose exec web python manage.py createsuperuser
Ingresa:
•	Username
•	Email
•	Password
________________________________________
🎨 4. Generar archivos estáticos
Solo la primera vez:
docker-compose exec web python manage.py collectstatic --noinput
________________________________________
🌐 5. Acceder al admin
URL	Descripción
http://localhost/admin/	Panel administrativo Django
________________________________________
🔄 Comandos útiles
Ver logs del servidor:
docker-compose logs -f web
Reiniciar solo el backend:
docker-compose restart web
Detener todos los servicios:
docker-compose down
Borrar contenedores + volúmenes (reset total):
docker-compose down -v
________________________________________
🐘 Base de datos (PostgreSQL)
El proyecto usa automáticamente estas variables:
POSTGRES_DB=tasks_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
Y se conecta al host interno:
DATABASE_HOST=db

