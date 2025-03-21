from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_notas'

# Rutas de archivos de datos
DATA_DIR = 'data'
DATOS_FILE = os.path.join(DATA_DIR, 'datos.json')

# Asegurarse de que el directorio data existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Cargar datos
def cargar_datos():
    if os.path.exists(DATOS_FILE):
        with open(DATOS_FILE, 'r') as f:
            return json.load(f)
    else:
        # Estructura inicial de datos
        datos_iniciales = {
            "cursos": {
                "1C": {
                    "nombre": "Primero C",
                    "alumnos": []
                },
                "2C": {
                    "nombre": "Segundo C",
                    "alumnos": []
                }
            },
            "asignaturas": {
                "Lenguaje": {
                    "nombre_completo": "Lenguaje y Comunicación",
                    "max_notas": 7
                },
                "Matematicas": {
                    "nombre_completo": "Matemáticas",
                    "max_notas": 7
                },
                "Ingles": {
                    "nombre_completo": "Inglés",
                    "max_notas": 7
                },
                "Cs_Naturales": {
                    "nombre_completo": "Ciencias Naturales",
                    "max_notas": 7
                },
                "Cs_Sociales": {
                    "nombre_completo": "Ciencias Sociales",
                    "max_notas": 7
                },
                "Instrumental": {
                    "nombre_completo": "Instrumental",
                    "max_notas": 7
                }
            },
            "configuracion": {
                "nombre_establecimiento": "CEIA Amigos del Padre Hurtado",
                "jefe_utp": "Nombre del Jefe UTP",
                "año_escolar": "2025"
            }
        }
        guardar_datos(datos_iniciales)
        return datos_iniciales

def guardar_datos(datos):
    with open(DATOS_FILE, 'w') as f:
        json.dump(datos, f, indent=4)

def calcular_promedios():
    datos = cargar_datos()
    promedios = {}
    
    for curso_id, curso in datos['cursos'].items():
        total_promedios = 0
        num_alumnos = len(curso['alumnos'])
        
        if num_alumnos > 0:
            for alumno in curso['alumnos']:
                total_promedios += alumno.get('promedio_general', 0)
            promedios[curso_id] = total_promedios / num_alumnos
        else:
            promedios[curso_id] = 0
    
    return promedios

@app.route('/')
def index():
    datos = cargar_datos()
    promedios = calcular_promedios()
    return render_template('index.html', 
                         cursos=datos['cursos'],
                         promedios=promedios)

@app.route('/curso/<curso>')
def ver_curso(curso):
    datos = cargar_datos()
    if curso not in datos['cursos']:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('index'))
    
    return render_template('curso.html',
                         curso=datos['cursos'][curso],
                         curso_id=curso,
                         asignaturas=datos['asignaturas'])

@app.route('/importar', methods=['GET', 'POST'])
def importar_alumnos():
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        archivo = request.files['archivo']
        curso = request.form.get('curso')
        
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        if archivo and curso:
            try:
                contenido = archivo.read().decode('utf-8')
                alumnos = [linea.strip() for linea in contenido.split('\n') if linea.strip()]
                
                datos = cargar_datos()
                for nombre in alumnos:
                    nuevo_alumno = {
                        "id": f"{curso}_{len(datos['cursos'][curso]['alumnos']) + 1:03d}",
                        "nombre": nombre,
                        "notas": {
                            asig: {"notas": [], "promedio": 0}
                            for asig in datos['asignaturas']
                        },
                        "promedio_general": 0
                    }
                    datos['cursos'][curso]['alumnos'].append(nuevo_alumno)
                
                guardar_datos(datos)
                flash(f'Se importaron {len(alumnos)} alumnos exitosamente', 'success')
                return redirect(url_for('ver_curso', curso=curso))
            
            except Exception as e:
                flash(f'Error al importar alumnos: {str(e)}', 'error')
                return redirect(request.url)
    
    return render_template('importar.html')

@app.route('/alumno/nuevo', methods=['GET', 'POST'])
def nuevo_alumno():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        curso = request.form.get('curso')
        
        if not nombre or not curso:
            flash('Por favor complete todos los campos', 'error')
            return redirect(request.url)
        
        datos = cargar_datos()
        nuevo_alumno = {
            "id": f"{curso}_{len(datos['cursos'][curso]['alumnos']) + 1:03d}",
            "nombre": nombre,
            "notas": {
                asig: {"notas": [], "promedio": 0}
                for asig in datos['asignaturas']
            },
            "promedio_general": 0
        }
        
        datos['cursos'][curso]['alumnos'].append(nuevo_alumno)
        guardar_datos(datos)
        
        flash('Alumno agregado exitosamente', 'success')
        return redirect(url_for('ver_curso', curso=curso))
    
    return render_template('nuevo_alumno.html')

@app.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    if request.method == 'POST':
        datos = cargar_datos()
        datos['configuracion'].update({
            'nombre_establecimiento': request.form.get('nombre_establecimiento'),
            'jefe_utp': request.form.get('jefe_utp'),
            'año_escolar': request.form.get('año_escolar')
        })
        guardar_datos(datos)
        flash('Configuración actualizada exitosamente', 'success')
        return redirect(url_for('index'))
    
    datos = cargar_datos()
    return render_template('configuracion.html', config=datos['configuracion'])

if __name__ == '__main__':
    app.run(debug=True)
