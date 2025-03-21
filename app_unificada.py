import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar, DateEntry
import customtkinter as ctk
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import os

# Código de la aplicación Tkinter (versión escritorio)
class AtrasosApp:
    # [Todo el código actual de app_tkinter.py]
    pass  # Aquí irá todo el código de la clase AtrasosApp

# Código de la aplicación Flask (versión web)
app = Flask(__name__)
app.secret_key = 'clave_secreta'

# [Todo el código actual de app.py]
# ... 

def iniciar_app_escritorio():
    root = tk.Tk()
    app = AtrasosApp(root)
    root.mainloop()

def iniciar_app_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--web':
        print("Iniciando versión web...")
        iniciar_app_web()
    else:
        print("Iniciando versión de escritorio...")
        iniciar_app_escritorio()
