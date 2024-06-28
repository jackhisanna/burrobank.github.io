from flask import Flask, render_template, request, redirect, url_for
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes WHERE NumCliente=%s AND Contrasena=%s", (usuario, contrasena))
        account = cur.fetchone()
        if account:
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrectos'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/nuevos_clientes', methods=['GET', 'POST'])
def nuevos_clientes():
    if request.method == 'POST':
        NumCliente = request.form['NumCliente']
        Nombre = request.form['Nombre']
        Telefono = request.form['Telefono']
        Direccion = request.form['Direccion']
        FechaNacimiento = request.form['FechaNacimiento']
        Email = request.form['Email']
        Contrasena = request.form['Contrasena']
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            flash('Correo electrónico no válido')
            return redirect(url_for('nuevos_clientes'))
        if not re.match(r"[0-9]{10}", Telefono):
            flash('Número de teléfono no válido')
            return redirect(url_for('nuevos_clientes'))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clientes (NumCliente, Nombre, Telefono, Direccion, FechaNacimiento, Email, Contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s)", (NumCliente, Nombre, Telefono, Direccion, FechaNacimiento, Email, Contrasena))
        mysql.connection.commit()
        cur.close()
        flash('Cliente agregado exitosamente')
        return redirect(url_for('nuevos_clientes'))
    return render_template('nuevos_clientes.html')

@app.route('/eliminar_cliente', methods=['GET', 'POST'])
def eliminar_cliente():
    if request.method == 'POST':
        NumCliente = request.form['NumCliente']
        
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM clientes WHERE NumCliente=%s", [NumCliente])
        mysql.connection.commit()
        cur.close()
        flash('Cliente eliminado exitosamente')
        return redirect(url_for('eliminar_cliente'))
    return render_template('eliminar_cliente.html')

if __name__ == '__main__':
    app.run()
