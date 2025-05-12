from flask import Flask
from controllers.home_controller import index, operar_conjuntos

app = Flask(__name__)

app.add_url_rule("/", view_func=index)
app.add_url_rule("/operar_conjuntos", view_func=operar_conjuntos, methods=["POST"])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)