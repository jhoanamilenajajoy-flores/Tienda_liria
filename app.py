from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('iniciar.html')
if __name__ == '__main__':
    app.run(debug=True)
