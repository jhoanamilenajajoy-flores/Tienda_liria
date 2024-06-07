from flask import Flask, render_template, request, make_response, json, jsonify, send_file
from database import Database
import pdfkit
from datetime import datetime
import io

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
    ventas = db.get_ventas_diarias()
    return render_template('dia.html', ventas=ventas)

@app.route('/mes')
def mostrar_mes():
    ventas = db.get_ventas_mensuales()
    return render_template('mes.html', ventas=ventas)

@app.route('/año')
def mostrar_año():
    ventas = db.get_ventas_anuales()
    return render_template('año.html', ventas=ventas)

@app.route('/dia_semana')
def mostrar_dia_semana():
    dia = request.args.get('dia')
    ventas = db.get_ventas_por_dia(dia)
    return render_template('dia_semana.html', dia=dia, ventas=ventas)

@app.route('/iniciar')
def iniciar():
    productos = db.get_productos()
    return render_template('iniciar.html', productos=productos)

@app.route('/guardarproducto')
def guardarproducto():
    categorias = db.get_categorias()
    proveedores = db.get_proveedores()
    return render_template('guardarproducto.html', categorias=categorias, proveedores=proveedores)

@app.route('/hogar')
def hogar():
    productos_hogar = db.get_productos_hogar()
    return render_template('hogar.html', productos=productos_hogar)

@app.route('/mecato')
def mecato():
    productos_mecato = db.get_productos_mecato()
    return render_template('mecato.html', productos=productos_mecato)

@app.route('/papeleria')
def papeleria():
    productos_papeleria = db.get_productos_papeleria()
    return render_template('papeleria.html', productos=productos_papeleria)

@app.route('/cuidadopersonal')
def cuidado_personal():
    productos_cuidado_personal = db.get_productos_cuidado_personal()
    return render_template('cuidadopersonal.html', productos=productos_cuidado_personal)
@app.route('/otros')
def otros():
    productos_otros = db.get_productos_otros()
    return render_template('otros.html', productos=productos_otros)

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    fecha = obtener_fecha_actual()
    nombre_tienda = "Tienda Liria"
    productos = request.form.get('productos')
    productos = json.loads(productos)
    subtotal = request.form.get('subtotal')
    total = request.form.get('total')
    contenido_html = render_template('recibo.html', fecha=fecha, nombre_tienda=nombre_tienda, productos=productos, subtotal=subtotal, total=total)
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(contenido_html, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=recibo.pdf'
    return response

@app.route('/categoria')
def categoria():
    ultimo_producto = db.get_ultimo_producto()
    return render_template('categoria.html', producto=ultimo_producto)


@app.route('/deudores')
def deudores():
    return render_template('deudores.html')

@app.route('/abonar')
def abonar():
    return render_template('abonar.html')

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')


@app.route('/alimentacion')
def mostrar_alimentacion():
    id_categoria_alimentos = 4  
    productos = db.get_productos_por_categoria(id_categoria_alimentos)
    return render_template('alimentacion.html', productos=productos)


@app.route('/agregar_producto_venta', methods=['POST'])
def agregar_producto_venta():
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio_unitario = request.form['precio_unitario']
    precio_total = request.form['precio_total']
    db.agregar_producto_venta(nombre, cantidad, precio_unitario, precio_total)
    return "Producto agregado a la venta"

@app.route('/registrar_venta', methods=['POST'])
def registrar_venta():
    productos = request.get_json()
    for producto in productos:
        nombre = producto['nombre']
        cantidad = int(producto['cantidad'])
        precio_unitario = float(producto['precioUnitario'])
        precio_total = float(producto['precioTotal'])
        id_producto = db.get_id_producto_por_nombre(nombre)
        if id_producto:
            db.registrar_venta(id_producto, cantidad, precio_unitario, precio_total)
    return jsonify({"message": "Venta registrada con éxito"})

@app.route('/download_recibo')
def download_recibo():
    tipo = request.args.get('tipo')
    if tipo == 'dia':
        ventas = db.get_ventas_diarias()
        template = 'dia.html'
    elif tipo == 'mes':
        ventas = db.get_ventas_mensuales()
        template = 'mes.html'
    elif tipo == 'año':
        ventas = db.get_ventas_anuales()
        template = 'año.html'
    else:
        return "Tipo de recibo no válido", 400

    html = render_template(template, ventas=ventas)
    
    # Generar el PDF
    try:
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        options = {
            'enable-local-file-access': None
        }
        pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    except IOError as e:
        return f"Error al generar el PDF: {str(e)}", 500

    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'recibo_{tipo}.pdf'
    )


@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombreProducto']
    codigo = request.form['codigoProducto']
    precio = request.form['precioProducto']
    cantidad = request.form['cantidadProducto']
    disponibilidad = request.form['disponibilidadProducto']
    proveedor = request.form['proveedorProducto']
    categoria = request.form['categoriaProducto']
    imagen = request.files['imagenProducto']

    # Validar y convertir datos
    try:
        precio = float(precio)
        cantidad = int(cantidad)
        disponibilidad = int(disponibilidad)
        proveedor = int(proveedor)
        categoria = int(categoria)
    except ValueError as e:
        return jsonify({"message": f"Error en los datos: {str(e)}"}), 400

    # Guardar la imagen en una carpeta estática
    imagen_filename = f"static/images/{imagen.filename}"
    imagen.save(imagen_filename)

    db.agregar_producto(nombre, codigo, precio, cantidad, disponibilidad, proveedor, categoria, imagen_filename)
    return jsonify({"message": "Producto agregado con éxito"})


if __name__ == '__main__':
    app.run(debug=True)
