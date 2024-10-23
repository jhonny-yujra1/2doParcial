from flask import Flask, render_template, request, redirect, url_for, session
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto en producción

# Inicializar la sesión
@app.before_request
def initialize_session():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def lista_productos():
    return render_template('productos.html', productos=session['productos'])

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        
        # Comprobar si el ID ya existe
        for producto in session['productos']:
            if producto['id'] == nuevo_producto['id']:
                return "El ID ya existe. Por favor, elige uno diferente.", 400
        
        session['productos'].append(nuevo_producto)
        session.modified = True  # Marca la sesión como modificada
        return redirect(url_for('lista_productos'))

    return render_template('agregar_producto.html')

if __name__ == '__main__':
    app.run(debug=True)
