import pyodbc

def obtener_conexion():
    """
    Función para conectar a SQL Server desde la Web.
    Retorna: Objeto de conexión o None si falla.
    """
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LUISPERSONAL\\SQLEXPRESS;'
            'DATABASE=DB_Catequesis;'
            'UID=admin_parroquial;'
            'PWD=P@sswordAdmin123;'
            'TrustServerCertificate=yes;'
        )
        return connection
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None