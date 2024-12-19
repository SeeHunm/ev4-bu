import pymysql

class Conexion:
    def __init__(self, host, user, password, db):
        self.db = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db = db
        )
        self.cursor = self.db.cursor()

    def ejecuta_query(self, sql):
        self.cursor.execute(sql)
        return self.cursor

    def desconectar(self):
        self.db.close()

    def commit(self):
        self.db.commit()

    def rolback(self):
        self.db.rollback()

    def obtenerUsuario(self, username):
        try:
            sql = f"SELECT * FROM usuarios WHERE username ='{username}'"
            cursor=self.ejecuta_query(sql)
            datos=cursor.fetchall()
            return datos
        except Exception as e:
            print(e)
    
    def agregarUsuario(self, username, password_hash, nombre, apellidos, email, tipo_usuario):
        try:
            existing_user = self.obtenerUsuario(username)
            if existing_user:
                raise ValueError("Nombre de usuario ya está registrado")
            
            sql = f"""
            INSERT INTO usuarios (username, password_hash, nombre, apellidos, email, tipo_usuario) 
            VALUES ('{username}', '{password_hash}', '{nombre}', '{apellidos}', '{email}', '{tipo_usuario}')
            """
            self.ejecuta_query(sql)
            self.commit()
            
            return True
        
        except ValueError as e:
            print(f"Error: {e}")
            return False
        
        except Exception as e:
            print(f"Error al ejecutar la consulta. Error: {e}")
            self.rollback()
            return False

    