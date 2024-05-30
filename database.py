import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
    

    def get_productos(self):
        self.cursor.execute("SELECT nombre_producto, cantidad, precio_unitario, precio_total FROM venta")
        return self.cursor.fetchall()
    def get_productos(self):
        self.cursor.execute("SELECT Nombre, codigo, Precio FROM producto")
        return self.cursor.fetchall()
    def agregar_producto_venta(self, nombre, cantidad, precio_unitario, precio_total):
        query = "INSERT INTO venta (nombre, cantidad, precio_unitario, precio_total) VALUES (%s, %s, %s, %s)"
        values = (nombre, cantidad, precio_unitario, precio_total)
        self.cursor.execute(query, values)
        self.connection.commit()