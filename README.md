# Sistema de Gestión de Atrasos

Sistema para registrar y gestionar atrasos de profesores, con generación de reportes individuales y generales.

## Versiones Disponibles

### 1. Versión Web (Railway)
- Implementada con Flask
- Diseño responsive y moderno
- Almacenamiento persistente de datos
- Reportes detallados

### 2. Versión Desktop
- Implementada con Tkinter
- Interfaz gráfica nativa
- Uso local

## Instalación

### Versión Web
```bash
cd web
pip install -r requirements.txt
python app.py
```

### Versión Desktop
```bash
pip install tkcalendar customtkinter
python app_tkinter.py
```

## Características

- Registro de atrasos con fecha y hora
- Gestión de profesores
- Cálculo automático de tiempo de atraso
- Reportes por profesor
- Reporte general
- Interfaz intuitiva y fácil de usar

## Despliegue en Railway

1. Fork este repositorio
2. Conéctalo a Railway
3. Railway detectará automáticamente la configuración en la carpeta `web/`
4. La aplicación se desplegará automáticamente

## Estructura del Proyecto

```
.
├── web/                    # Versión web (Railway)
│   ├── app.py             # Aplicación Flask
│   ├── Procfile           # Configuración Railway
│   ├── requirements.txt   # Dependencias web
│   └── templates/         # Plantillas HTML
├── app_tkinter.py         # Versión desktop
└── README.md             # Este archivo
```

## Tecnologías Utilizadas

- Python 3.x
- Flask (versión web)
- Bootstrap 5
- Tkinter/CustomTkinter (versión desktop)
- Railway (despliegue)
