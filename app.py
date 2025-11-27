from flask import Flask, render_template, request, redirect, url_for, flash
from conexion import obtener_conexion
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'clave_secreta_proyecto_fase4'

# --- CONFIGURACIÓN DEL LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- CLASE USUARIO ---
class Usuario(UserMixin):
    def __init__(self, id, nombre, username):
        self.id = id
        self.nombre = nombre
        self.username = username

# --- CARGADOR DE USUARIO ---
@login_manager.user_loader
def load_user(user_id):
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT idUsuario, nombre, userName FROM dbo.Usuario WHERE idUsuario = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(row[0], row[1], row[2])
    return None

# --- RUTA DE LOGIN (PÚBLICA) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            # Buscamos al usuario en la tabla Usuario creada en Fase 3
            cursor.execute("SELECT idUsuario, nombre, userName, contraseña FROM dbo.Usuario WHERE userName = ?", (username,))
            user_data = cursor.fetchone()
            conn.close()
            # Verificamos si existe el usuario y si la contraseña coincide
            if user_data and user_data[3] == password:
                user_obj = Usuario(user_data[0], user_data[1], user_data[2])
                login_user(user_obj)
                flash(f'¡Bienvenido, {user_data[1]}!')
                return redirect(url_for('index'))
            else:
                flash('Usuario o contraseña incorrectos.')
    
    return render_template('login.html')

# --- RUTA DE LOGOUT ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.')
    return redirect(url_for('login'))

# --- RUTA DE INICIO (PROTEGIDA) ---
@app.route('/')
@login_required 
def index():
    return redirect(url_for('lista'))

# --- RUTA LISTAR (PROTEGIDA) ---
@app.route('/lista')
@login_required
def lista():
    conn = obtener_conexion()
    datos = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT idCatequizando, nombres, Apellidos, documentoIdentidad, fechaNacimiento, feBautismoEntregada FROM dbo.Catequizado")
            datos = cursor.fetchall()
            conn.close()
        except Exception as e:
            flash(f"Error al cargar lista: {e}")
    
    return render_template('lista.html', catequizados=datos)

# --- RUTA REGISTRAR (PROTEGIDA) ---
@app.route('/registro', methods=['GET', 'POST'])
@login_required
def registro():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['documentoIdentidad']
        fecha_nac = request.form['fechaNacimiento']
        
        id_familia = 1 
        fe_bautismo = 0 

        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO dbo.Catequizado 
                    (nombres, Apellidos, fechaNacimiento, documentoIdentidad, Familia_idFamilia, feBautismoEntregada)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, (nombres, apellidos, fecha_nac, cedula, id_familia, fe_bautismo))
                conn.commit()
                conn.close()
                flash('¡Alumno registrado exitosamente en la Base de Datos!')
                return redirect(url_for('lista'))
            
            except Exception as e:
                flash(f"Error al guardar en SQL Server: {e}")
                return redirect(url_for('registro'))

    return render_template('registro.html')

# --- RUTA ELIMINAR (PROTEGIDA) ---
@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dbo.Catequizado WHERE idCatequizando = ?", (id,))
            conn.commit()
            conn.close()
            flash('Registro eliminado correctamente.')
        except Exception as e:
            flash(f"Error al eliminar: {e}")
    
    return redirect(url_for('lista'))

# --- RUTA EDITAR (PROTEGIDA) ---
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['documentoIdentidad']
        fecha_nac = request.form['fechaNacimiento']
        
        try:
            query = """
                UPDATE dbo.Catequizado 
                SET nombres = ?, Apellidos = ?, documentoIdentidad = ?, fechaNacimiento = ?
                WHERE idCatequizando = ?
            """
            cursor.execute(query, (nombres, apellidos, cedula, fecha_nac, id))
            conn.commit()
            flash('Datos actualizados correctamente.')
            return redirect(url_for('lista'))
        except Exception as e:
            flash(f"Error al actualizar: {e}")
    
    cursor.execute("SELECT * FROM dbo.Catequizado WHERE idCatequizando = ?", (id,))
    data = cursor.fetchone()
    conn.close()

    if data:
        return render_template('editar.html', catequizado=data)
    else:
        flash("Registro no encontrado.")
        return redirect(url_for('lista'))

if __name__ == '__main__':
    app.run(debug=True)