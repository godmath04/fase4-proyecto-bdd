from flask import Flask, render_template, request, redirect, url_for, flash
from conexion import obtener_conexion

app = Flask(__name__)
# Esta clave es necesaria para que funcionen los mensajes de éxito
app.secret_key = 'clave_secreta_proyecto_fase4'

# --- RUTA DE INICIO ---
@app.route('/')
def index():
    return redirect(url_for('lista'))

# --- RUTA LISTAR (READ) ---
@app.route('/lista')
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

# --- RUTA REGISTRAR (CREATE) ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Si el usuario llenó el formulario y dio clic en "Guardar" (Método POST)
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['documentoIdentidad']
        fecha_nac = request.form['fechaNacimiento']
        
        # VALORES FIJOS PARA LA DEMOSTRACIÓN:
        # Asignamos Familia 1 y FeBautismoEntregada = 0 (Falso)
        id_familia = 1 
        fe_bautismo = 0 

        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                # Query de inserción directa
                query = """
                    INSERT INTO dbo.Catequizado 
                    (nombres, Apellidos, fechaNacimiento, documentoIdentidad, Familia_idFamilia, feBautismoEntregada)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                # Ejecutamos pasando las variables
                cursor.execute(query, (nombres, apellidos, fecha_nac, cedula, id_familia, fe_bautismo))
                conn.commit()
                conn.close()
                
                # Mensaje de éxito
                flash('¡Alumno registrado exitosamente en la Base de Datos!')
                return redirect(url_for('lista'))
            
            except Exception as e:
                flash(f"Error al guardar en SQL Server: {e}")
                return redirect(url_for('registro'))

    # Si el usuario solo entró a la página (Método GET)
    return render_template('registro.html')

# --- RUTA ELIMINAR (DELETE) ---
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            # Ejecutamos el borrado directo
            cursor.execute("DELETE FROM dbo.Catequizado WHERE idCatequizando = ?", (id,))
            conn.commit()
            conn.close()
            flash('Registro eliminado correctamente.')
        except Exception as e:
            flash(f"Error al eliminar: {e}")
    
    return redirect(url_for('lista'))

# --- RUTA EDITAR (UPDATE) ---
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # SI ES POST: El usuario modificó los datos y dio clic en "Actualizar"
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['documentoIdentidad']
        fecha_nac = request.form['fechaNacimiento']
        
        try:
            # Ejecutamos el UPDATE
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
            # Si falla, no redirigimos, nos quedamos aquí
    
    # SI ES GET: Buscamos los datos para llenar el formulario
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