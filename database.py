import mysql.connector
import base64
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
        self.cursor.execute("SELECT Nombre, codigo, Precio FROM producto")
        return self.cursor.fetchall()

    def get_id_producto_por_nombre(self, nombre):
        query = "SELECT id_producto FROM producto WHERE nombre = %s"
        self.cursor.execute(query, (nombre,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def registrar_venta(self, id_producto, cantidad, precio_unitario, precio_total):
        precio_iva = precio_unitario * 1.19  # Asumiendo un IVA del 19%
        query = """INSERT INTO venta (id_producto, cantidad_producto, precio_unitario_producto, precio_iva_producto, precio_total_producto, fecha_venta) 
                   VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"""
        values = (id_producto, cantidad, precio_unitario, precio_iva, precio_total)
        self.cursor.execute(query, values)
        self.connection.commit()

    def get_ventas_diarias(self):
        query = """
        SELECT DATE(fecha_venta) as dia, SUM(precio_total_producto) as total_dia
        FROM venta
        GROUP BY DATE(fecha_venta)
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_ventas_mensuales(self):
        query = """
        SELECT DATE_FORMAT(fecha_venta, '%Y-%m') as mes, SUM(precio_total_producto) as total_mes
        FROM venta
        GROUP BY DATE_FORMAT(fecha_venta, '%Y-%m')
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_ventas_anuales(self):
        query = """
        SELECT YEAR(fecha_venta) as año, SUM(precio_total_producto) as total_año
        FROM venta
        GROUP BY YEAR(fecha_venta)
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_ventas_por_dia(self, dia):
        query = """
        SELECT producto.Nombre, venta.cantidad_producto, venta.precio_total_producto
        FROM venta
        JOIN producto ON venta.id_producto = producto.id_producto
        WHERE DATE(venta.fecha_venta) = %s
        """
        self.cursor.execute(query, (dia,))
        return self.cursor.fetchall()
    def get_id_proveedor_por_nombre(self, nombre):
        query = "SELECT id_proveedor FROM proveedores WHERE nombre_proveedor = %s"
        self.cursor.execute(query, (nombre,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_id_categoria_por_nombre(self, nombre):
        query = "SELECT id_categoria FROM categorias_prod WHERE nombre_categoria = %s"
        self.cursor.execute(query, (nombre,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    def agregar_producto(self, nombre, codigo, precio, cantidad, disponibilidad, id_proveedor, id_categoria, imagen):
        query = """
        INSERT INTO producto (nombre, codigo, precio, cantidad, disponibilidad, id_proveedor, id_categoria, imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (nombre, codigo, precio, cantidad, disponibilidad, id_proveedor, id_categoria, imagen)
        self.cursor.execute(query, values)
        self.connection.commit()


    def get_categorias(self):
        self.cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias_prod")
        return self.cursor.fetchall()

    def get_proveedores(self):
        self.cursor.execute("SELECT id_proveedor, nombre_proveedor FROM proveedores")
        return self.cursor.fetchall()
    def get_productos_por_categoria(self, id_categoria):
        query = """
        SELECT nombre, precio, imagen 
        FROM producto 
        WHERE id_categoria = %s
        """
        self.cursor.execute(query, (id_categoria,))
        return self.cursor.fetchall()
    def get_productos_cuidado_personal(self):
        query = """
        SELECT nombre, precio, imagen 
        FROM producto 
        WHERE id_categoria = 6
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def get_productos_hogar(self):
        query = """
        SELECT nombre, precio, imagen 
        FROM producto 
        WHERE id_categoria = 5
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def get_productos_papeleria(self):
        query = """
        SELECT nombre, precio, imagen 
        FROM producto 
        WHERE id_categoria = 7
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def get_productos_mecato(self):
        query = """
        SELECT nombre, precio, imagen 
        FROM producto 
        WHERE id_categoria = 8
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def get_productos_otros(self):
        query = """
        SELECT nombre, precio, imagen 
        FROM producto 
        WHERE id_categoria = 9
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def get_ultimo_producto(self):
        query = """
        SELECT nombre, precio, imagen 
        FROM producto 
        ORDER BY id_producto DESC 
        LIMIT 1
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            nombre, precio, imagen_blob = result
            imagen_base64 = base64.b64encode(imagen_blob).decode('utf-8')
            return nombre, precio, imagen_base64
        return None