# Laboratorio: Código Seguro y Modelo OWASP

## 1. Datos generales

- **Nombre completo: Rubén Edgardo Iglesias Alfaro
- **Carné:** Completar
- **Correo institucional: rubenedgardo70080@gmail.com
- **Asignatura: Lenguajes de Programación con Aspectos de Seguridad
- **Fecha: 08/11/2026

## 2. Descripción

Este laboratorio consiste en desarrollar una aplicación web utilizando Python, implementando controles básicos de seguridad basados en buenas prácticas y el modelo OWASP. Se aplican mecanismos de validación de entradas, consultas parametrizadas, protección de contraseñas, registro de eventos de autenticación y detección de incidentes, incluyendo el cálculo de las métricas MTTD y MTTR.

## 3. Estructura del proyecto

```text
nombre-del-repositorio/
└── lab-las/
    ├── templates/
    │   ├── login.html
    │   └── registro.html
    ├── app.py
    ├── crearDB.py
    ├── detector.py
    ├── usuarios.db
    ├── eventos.log
    ├── respuesta.log
    └── README.md
```

## 4. Ejecución del proyecto

**Paso 1.** Clonar el repositorio.

```bash
git clone URL_DEL_REPOSITORIO
```

**Paso 2.** Ingresar al proyecto.

```bash
cd lab-las
```
# Puede ser que ya este dentro del directorio, asi que revise eso antes si ha descargado el codigo en zip.

**Paso 3.** Instalar las dependencias.

# Crear entorno virtual
```bash
python -m venv venv
```

# Activar entorno virtual (tenga cuidado con las plecas porque depende de si usa gitbash o powershell como terminal)
```bash
venv\Scripts\activate
```
# Instalar Flask
```bash
pip install flask
```

# Antes de entrar a registrar usuarios en login
```bash
python crearDB.py
```
# Ejecute la app y dejela corriendo 
```bash
python app.py
```

# Luego de registar usuarios, forzar algun tipo de fallo o registro normal y se guardara en eventos.log
```bash
python detector.py
```
**Paso 4.** Ejecutar la aplicación.
# Ejecute la app y dejela corriendo 
```bash
python app.py
```
# En su navegador valla al siguiente url para registro y para login

# Registrar usuarios nuevos.
```bash
http://127.0.0.1:5000/registro
```
# Para ingresar con algún usuario creado
```bash
http://127.0.0.1:5000/login
```
