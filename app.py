from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Asegurarse de que el directorio data existe
if not os.path.exists('data'):
    os.makedirs('data')

# Rutas de archivos de datos
PROFESORES_FILE = 'data/profesores.json'
ATRASOS_FILE = 'data/atrasos.json'

# Cargar datos
def cargar_datos():
    profesores = []
    atrasos = []
    
    if os.path.exists(PROFESORES_FILE):
        with open(PROFESORES_FILE, 'r') as f:
            profesores = json.load(f)
    
    if os.path.exists(ATRASOS_FILE):
        with open(ATRASOS_FILE, 'r') as f:
            atrasos = json.load(f)
    
    return profesores, atrasos

# Guardar datos
def guardar_datos(profesores, atrasos):
    with open(PROFESORES_FILE, 'w') as f:
        json.dump(profesores, f)
    
    with open(ATRASOS_FILE, 'w') as f:
        json.dump(atrasos, f)

# Rutas
@app.route('/')
def index():
    profesores, atrasos = cargar_datos()
    return render_template('index.html', profesores=profesores, atrasos=atrasos)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    profesores, atrasos = cargar_datos()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        horario_programado = request.form['horario_programado']
        horario_real = request.form['horario_real']
        fecha = request.form['fecha']

        # Calcular atraso
        h_prog = datetime.strptime(horario_programado, '%H:%M')
        h_real = datetime.strptime(horario_real, '%H:%M')
        diferencia = h_real - h_prog
        
        horas, segundos = divmod(diferencia.seconds, 3600)
        minutos, _ = divmod(segundos, 60)

        atraso = {
            'nombre': nombre,
            'horario_programado': horario_programado,
            'horario_real': horario_real,
            'fecha': fecha,
            'atraso': f'{horas}h {minutos}m'
        }

        # Guardar atraso
        atrasos.append(atraso)
        
        # Agregar profesor si no existe
        if nombre not in profesores:
            profesores.append(nombre)

        # Guardar datos
        guardar_datos(profesores, atrasos)
        
        return redirect(url_for('index'))

    return render_template('registrar.html', profesores=profesores)

@app.route('/reporte/profesor/<nombre>')
def reporte_profesor(nombre):
    profesores, atrasos = cargar_datos()
    atrasos_profesor = [a for a in atrasos if a['nombre'] == nombre]
    
    # Calcular total
    total_horas = 0
    total_minutos = 0
    
    for atraso in atrasos_profesor:
        horas = int(atraso['atraso'].split('h')[0])
        minutos = int(atraso['atraso'].split('h')[1].split('m')[0])
        total_horas += horas
        total_minutos += minutos

    total_horas += total_minutos // 60
    total_minutos = total_minutos % 60
    
    return render_template('reporte_profesor.html', 
                         profesor=nombre,
                         atrasos=atrasos_profesor,
                         total=f'{total_horas}h {total_minutos}m')

@app.route('/reporte/general')
def reporte_general():
    profesores, atrasos = cargar_datos()
    
    # Calcular total
    total_horas = 0
    total_minutos = 0
    
    for atraso in atrasos:
        horas = int(atraso['atraso'].split('h')[0])
        minutos = int(atraso['atraso'].split('h')[1].split('m')[0])
        total_horas += horas
        total_minutos += minutos

    total_horas += total_minutos // 60
    total_minutos = total_minutos % 60
    
    return render_template('reporte_general.html',
                         atrasos=atrasos,
                         total=f'{total_horas}h {total_minutos}m')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
