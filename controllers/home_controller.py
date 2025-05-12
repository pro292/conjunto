from flask import render_template, request, jsonify
from models.conjunto import conjunto

def index():
    data = {
        #"title": "Mi Página de Inicio",
        #"message": "Bienvenido a mi sitio web!"
    }
    return render_template("index.html", data=data)

def operar_conjuntos():
    data = request.json
    conjunto_a = list(map(str.strip, data.get('conjuntoA', '').split(',')))
    conjunto_b = list(map(str.strip, data.get('conjuntoB', '').split(',')))
    operacion = data.get('operacion', '')

    A = conjunto()
    B = conjunto()
    
    A = conjunto(elementos = conjunto_a)
    B = conjunto(elementos = conjunto_b)

    if operacion == "union":
        resultado = A.union(B)
    elif operacion == "interseccion":
        resultado = A.interseccion(B)
        print(f"Resultado Intersección (Python): {resultado}")
    elif operacion == "diferencia":
        resultado = A.diferencia(B)
    elif operacion == "diferenciaSimetrica":
        resultado = A.diferencia_simetrica(B)
    elif operacion == "subconjunto":
        resultado = "Sí" if A.subconjunto(B) else "No"
    elif operacion == "superconjunto":
        resultado = "Sí" if A.superconjunto(B) else "No"
    else:
        resultado = "Operación no válida"

    # 4️⃣ Enviamos el resultado como un JSON
    if isinstance(resultado, conjunto):
        resultado = resultado.to_dict()
    return jsonify({"resultado": resultado})