from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "123"

# BANCO
def db():
    return sqlite3.connect("banco.db")

def criar():
    conn = db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        servico TEXT,
        data TEXT,
        hora TEXT
    )
    """)

    conn.commit()
    conn.close()

# SERVIÇOS
servicos = {
    1: {"nome": "Corte de cabelo", "preco": 30},
    2: {"nome": "Manicure", "preco": 25},
    3: {"nome": "Pedicure", "preco": 30},
    4: {"nome": "Escova", "preco": 40},
}

# LOGIN
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["user"] == "admin" and request.form["pass"] == "123":
            session["logado"] = True
            return redirect("/home")
    return render_template("login.html")

# HOME
@app.route("/home")
def home():
    if not session.get("logado"):
        return redirect("/")
    return render_template("home.html", servicos=servicos)

# AGENDAR
@app.route("/agendar", methods=["GET","POST"])
def agendar():
    if not session.get("logado"):
        return redirect("/")

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        servico = request.form["servico"]
        data = request.form["data"]
        hora = request.form["hora"]

        conn = db()
        c = conn.cursor()

        c.execute("""
        INSERT INTO agendamentos(nome,telefone,servico,data,hora)
        VALUES (?,?,?,?,?)
        """, (nome, telefone, servico, data, hora))

        conn.commit()
        conn.close()

        return redirect("/lista")

    return render_template("agendar.html", servicos=servicos)

# LISTA
@app.route("/lista")
def lista():
    if not session.get("logado"):
        return redirect("/")

    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM agendamentos")
    dados = c.fetchall()
    conn.close()

    return render_template("lista.html", dados=dados)

# INICIAR
criar()

if __name__ == "__main__":
    app.run(debug=True)