from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB = Path("pedidos.db")

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS pedidos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL,
            pagamento TEXT NOT NULL,
            entrega TEXT NOT NULL,
            total REAL NOT NULL
        )""")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/pedidos", methods=["POST"])
def criar_pedido():
    dados = request.get_json(force=True)
    obrigatorios = ["nome","telefone","endereco","pagamento","entrega","total"]
    faltando = [c for c in obrigatorios if not dados.get(c)]
    if faltando:
        return jsonify({"erro":"Campos obrigatórios ausentes","campos":faltando}), 400

    with sqlite3.connect(DB) as conn:
        cur = conn.execute(
            "INSERT INTO pedidos(nome,telefone,endereco,pagamento,entrega,total) VALUES(?,?,?,?,?,?)",
            (dados["nome"],dados["telefone"],dados["endereco"],dados["pagamento"],dados["entrega"],float(dados["total"]))
        )
        pedido_id = cur.lastrowid
    return jsonify({"mensagem":"Pedido registrado com sucesso","pedido_id":pedido_id}), 201

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
