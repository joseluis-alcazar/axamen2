from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configura la conexión con la base de datos Access
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\aldeb\OneDrive\Documentos\TaskDB.accdb;')

@app.route('/')
def mostrar_tareas():
    cursor = conn.cursor()
    cursor.execute('SELECT id, descripcion, estado FROM Tareas')
    tareas = cursor.fetchall()
    return render_template('tareas.html', tareas=tareas)

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        estado = 'No Completado'  # Asegúrate de que el estado sea una cadena de caracteres
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Tareas (descripcion, estado) VALUES (?, ?)', (descripcion, estado))
        conn.commit()
    return redirect(url_for('mostrar_tareas'))

@app.route('/marcar_completado/<int:id>')
def marcar_completado(id):
    cursor = conn.cursor()
    cursor.execute('UPDATE Tareas SET estado = ? WHERE id = ?', ('Completado', id))  # Asegúrate de que 'Completado' sea una cadena de caracteres
    conn.commit()
    return redirect(url_for('mostrar_tareas'))

@app.route('/marcar_no_completado/<int:id>')
def marcar_no_completado(id):
    cursor = conn.cursor()
    cursor.execute('UPDATE Tareas SET estado = ? WHERE id = ?', ('No Completado', id))  # Asegúrate de que 'No Completado' sea una cadena de caracteres
    conn.commit()
    return redirect(url_for('mostrar_tareas'))

@app.route('/eliminar_tarea/<int:id>')
def eliminar_tarea(id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Tareas WHERE id = ?', (id,))
    conn.commit()
    return redirect(url_for('mostrar_tareas'))

if __name__ == '__main__':
    app.run(debug=True)
