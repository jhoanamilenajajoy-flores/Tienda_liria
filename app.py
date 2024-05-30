from flask import Flask, render_template, request, make_response, json
from database import Database
import pdfkit
from datetime import datetime

app = Flask(__name__)
db = Database(host="localhost", user="root", password="", database="tienda_liria")

def obtener_fecha_actual():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/informes_venta')
def informe_venta():
    return render_template('informes_venta.html')

@app.route('/dia')
def mostrar_dia():
    return render_template('dia.html')

@app.route('/mes')
def mostrar_mes():
    return render_template('mes.html')

@app.route('/año')
def mostrar_año():
    return render_template('año.html')

@app.route('/dia_semana')
def mostrar_dia_semana():
    return render_template('dia_semana.html')

@app.route('/iniciar')
def iniciar():
    productos = db.get_productos()
    return render_template('iniciar.html', productos=productos)

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    # Obtener datos para el recibo
    fecha = obtener_fecha_actual()
    nombre_tienda = "Tienda Liria"
    # Supongamos que los productos vienen en formato JSON desde el formulario
    productos = request.form.get('productos')
    productos = json.loads(productos)  # Convertir el JSON a una lista de diccionarios
    subtotal = request.form.get('subtotal')
    total = request.form.get('total')

    # Renderizar la plantilla HTML del recibo con los datos
    contenido_html = render_template('recibo.html', fecha=fecha, nombre_tienda=nombre_tienda, productos=productos, subtotal=subtotal, total=total)
    
    # Configurar pdfkit con la ruta completa a wkhtmltopdf si no está en PATH
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    
    # Generar el PDF a partir del HTML
    pdf = pdfkit.from_string(contenido_html, False, configuration=config)

    # Crear una respuesta Flask con el PDF generado
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=recibo.pdf'

    return response

@app.route('/categoria')
def categoria():
    return render_template('categoria.html')

@app.route('/deudores')
def deudores():
    return render_template('deudores.html')

@app.route('/abonar')
def abonar():
    return render_template('abonar.html')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

@app.route('/agregar_producto_venta', methods=['POST'])
def agregar_producto_venta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']
        precio_total = request.form['precio_total']
        db.agregar_producto_venta(nombre, cantidad, precio_unitario, precio_total)
        return "Producto agregado a la venta"
    else:
        return "Error al agregar el producto"

if __name__ == '__main__':
    app.run(debug=True)
