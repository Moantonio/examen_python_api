import sqlite3
from datetime import datetime

# Conexión a la base de datos (se creará si no existe)
conn = sqlite3.connect('alumnos.db')

# Crear un cursor para ejecutar comandos SQL
cur = conn.cursor()

# Crear la tabla 'alumnos'
cur.execute('''
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    aprobado BOOLEAN NOT NULL,
    nota REAL NOT NULL,
    fecha TIMESTAMP NOT NULL
)
''')

# Lista de alumnos a insertar
alumnos = [
    ('Juan', 'Pérez', True, 7.5, '2024-09-01 00:00:00'),
    ('María', 'López', False, 4.2, '2024-09-02 00:00:00'),
    ('Carlos', 'García', True, 8.9, '2024-09-03 00:00:00'),
    ('Lucía', 'Martínez', True, 9.1, '2024-09-04 00:00:00'),
    ('Sofía', 'Fernández', False, 5.0, '2024-09-05 00:00:00')
]

# Insertar los registros en la tabla 'alumnos'
cur.executemany('''
    INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha)
    VALUES (?, ?, ?, ?, ?)
''', alumnos)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada y registros insertados correctamente.")
