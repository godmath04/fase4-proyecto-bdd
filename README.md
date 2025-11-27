# Sistema de Gestión de Catequesis - Fase 4

Este proyecto consiste en una aplicación web desarrollada en **Python (Flask)** que interactúa con una base de datos **Microsoft SQL Server**. Implementa un sistema CRUD (Crear, Leer, Actualizar, Eliminar) para la gestión de personas en procesos de catequesis.

Proyecto desarrollado como parte de la **Fase 4 del Proyecto Integrador**.

## 👥 Equipo de Trabajo [6 - 5620]
* **Jorge Ramos**
* **Fabio Gonzales**
* **Luis Pineda**

## 🚀 Funcionalidades
* **Autenticación (Login):** Sistema de seguridad de gestión de sesiones Flask-Login. Protege el acceso a las rutas internas
* **Conexión a Base de Datos:** Uso de `pyodbc` para conectar Python con SQL Server.
* **Listado (READ):** Visualización de personas registradas en la tabla `Catequizado`.
* **Registro (CREATE):** Formulario para ingresar nuevos alumnos.
* **Edición (UPDATE):** Modificación de datos existentes.
* **Eliminación (DELETE):** Borrado lógico o físico de registros.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.12+
* **Framework Web:** Flask
* **Base de Datos:** Microsoft SQL Server (Express Edition)
* **Driver:** ODBC Driver 17 for SQL Server
* **Frontend:** HTML5 + Jinja2 Templates + Bootstrap 5

## 📋 Requisitos Previos
Para ejecutar este proyecto necesitas:
1. Tener instalado **Python**,
2. Tener instalado **SQL Server** y el **ODBC Driver 17**.
3. Haber ejecutado el script de base de datos de la **Fase 3** (`DB_Catequesis`).

## ⚙️ Instalación y Ejecución

### 1. Clonar o descargar el repositorio
Descarga los archivos en tu carpeta de preferencia.

### 2. Crear y activar entorno virtual (Opcional pero recomendado)
```bash
# Crear entorno
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

```

### 3. Instalar dependencias 
pip install flask pyodbc

### 4. Configurar la Base de Datos
Asegúrate de que la base de datos DB_Catequesis esté creada y poblada. Verifica el archivo conexion.py para confirmar que el SERVER coincida con el nombre de tu instancia local de SQL Server.

### 5. Ejecutar aplicación
```bash
python app.py
```

### 6. Acceder

Abre tu navegador web e ingresa a: http://127.0.0.1:5000

### 7. Credenciales de Acceso (Pruebas)

EL sistema está protegido. Para ingresar y probar el CRUD se utiliza el usuario:
```bash
admin_sanjuan | hash_admin
```
