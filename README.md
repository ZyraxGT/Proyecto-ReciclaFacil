# API de Registro e Inicio de Sesión

Este proyecto es una API básica con Flask que permite registrar usuarios e iniciar sesión el cual incluye tambien una pequeño prototipo, con funciones basicas y botones de uso.
Por Juan Angel Rangel Cediel
Programa Analisis y desarrollo de software SENA FICHA:2834914

## Endpoints

- `/registro` [POST]: Registra un usuario (requiere `usuario` y `contrasena`).
- `/login` [POST]: Inicia sesión con usuario y contraseña.

## Requisitos

- Python 3
- Flask

## Cómo ejecutar

1. Instala las dependencias:

```
pip install -r requirements.txt
```

2. Ejecuta la aplicación:

```
python app.py
```
