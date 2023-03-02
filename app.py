from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Palinopsia20.@localhost/cadastro_exames'
db = SQLAlchemy(app)


class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50))
    data_de_nascimento = db.Column(db.Date)
    email = db.Column(db.String(50), unique=True)
    cpf = db.Column(db.String(11), unique=True)
    senha = db.Column(db.String(50))
    

@app.route("/", methods=['POST', 'GET'])
def homepage():
    return render_template("cadastro.html")


@app.route("/autenticar_cpf", methods=['POST', 'GET'])    
def autenticar_cpf():
    cpf = request.form.get('cpf')

    a = [int(char) for char in cpf if char.isdigit()]

    if len(a) != 11:
        return False

    if a == a[::-1]:
        return False

    for i in range(9, 11):
        value = sum((a[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != a[i]:
            return False
    return render_template("index.html")


@app.route("/autenticar", methods=['POST', 'GET'])    
def autenticar():
    nome = request.form.get('name')
    data_de_nascimento = request.form.get('date')
    email = request.form.get('email')
    cpf = request.form.get('cpf')
    senha = request.form.get('password')
    
    novo_paciente = Paciente(nome=nome, data_de_nascimento=data_de_nascimento, email=email, cpf=cpf, senha=senha)
    db.session.add(novo_paciente)
    db.session.commit()
    
    return render_template("index.html")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
