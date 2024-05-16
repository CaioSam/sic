from flask import Flask, render_template, request, redirect, session, url_for, flash, get_flashed_messages, make_response
from flask_paginate import Pagination, get_page_args
from decimal import Decimal
from datetime import datetime, timedelta 
from collections import defaultdict
import mysql.connector
from mysql.connector import Error
import csv

const express = require('express')
const app = express()
const port = process.env.PORT || 4000;
app = Flask(__name__)
app.secret_key = 'my_secret_key_12345'

# Configuração BD Locaweb
db_config = {
    "host": "controle_sici.mysql.dbaas.com.br",
    "user": "controle_sici",
    "password": "All8181@",
    "database": "controle_sici"
}

# Página Home
@app.route('/')
def home():
    return render_template('index.html')

# Cadastro de empresas
@app.route('/cadastro-empresas', methods=['GET', 'POST'])
def cadastro_empresas():
    if request.method == 'POST':
        codigo_empresa = request.form['codigo_empresa']
        razao_social = request.form['razao_social']
        valor_diaria = Decimal(request.form['valor_diaria'])

        try:
            with mysql.connector.connect(**db_config) as connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO empresas (codigo_empresa, razao_social, valor_diaria) VALUES (%s, %s, %s)"
                    val = (codigo_empresa, razao_social, valor_diaria)
                    cursor.execute(sql, val)
                    connection.commit()
            flash('Empresa Cadastrada!', 'success')
            return redirect(url_for('cadastro_empresas'))
        except Error as e:
            return f'Error: {e}'

    #return render_template('cadastro_empresas.html')

  # Consultar empresas cadastradas
    def consultar_empresas():
        try:
            with mysql.connector.connect(**db_config) as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM empresas"
                    cursor.execute(sql)
                    empresas = cursor.fetchall()
                    empresas_dict = []
                    for empresa in empresas:
                        empresas_dict.append({
                            'codigo_empresa': empresa[1],
                            'razao_social': empresa[2],
                            'valor_diaria': empresa[3]
                        })
                    return empresas_dict
        except Error as e:
            return f'Error: {e}'

    empresas = consultar_empresas()
    return render_template('cadastro_empresas.html', empresas=empresas)


# Cadastro de empregados
@app.route('/cadastro-empregados', methods=['GET', 'POST'])
def cadastro_empregados():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nome_completo = request.form['nome_completo']
        cargo = request.form['cargo']
        data_admissao = request.form['data_admissao']

        try:
            with mysql.connector.connect(**db_config) as connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO funcionarios (codigo, nome_completo, cargo, data_admissao) VALUES (%s, %s, %s, %s)"
                    val = (codigo, nome_completo, cargo, data_admissao)
                    cursor.execute(sql, val)
                    connection.commit()
            return 'Empregado cadastrado!'
        except Error as e:
            return f'Error: {e}'

    try:
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT razao_social FROM empresas"
                cursor.execute(sql)
                empresas = cursor.fetchall()
    except Error as e:
        return f'Error: {e}'

    funcionarios = consulta_empregados()
    return render_template('cadastro-empregados.html', empresas=empresas, funcionarios=funcionarios)

def consulta_empregados():
    try:
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM funcionarios"
                cursor.execute(sql)
                funcionarios = cursor.fetchall()
                funcionarios_dict = []
                for funcionario in funcionarios:
                    funcionarios_dict.append({
                        'codigo': funcionario[1],
                        'nome_completo': funcionario[2],
                        'cargo': funcionario[3],
                        'data_admissao': funcionario[4]
                    })
                return funcionarios_dict
    except Error as e:
        return f'Error retrieving employees: {e}'
   
# Cadastro de tarefas
@app.route('/cadastro_tarefas', methods=['GET', 'POST'])    
def cadastro_tarefas():
    tarefas=consulta_tarefas()
    if request.method == 'POST':
        data = request.form['data']
        funcionario_codigo = request.form['funcionario']
        tarefa = request.form['tarefa']
        quantidade = Decimal(request.form['quantidade'])
        valor = Decimal(request.form['valor'])
        total = quantidade * valor

        
        try:
            with mysql.connector.connect(**db_config) as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT nome_completo FROM funcionarios WHERE codigo = %s"
                    val = (funcionario_codigo,)
                    cursor.execute(sql, val)
                    funcionario_nome_completo = cursor.fetchone()[0]
        except Error as e:
            return f'Error: {e}'   

        try:
            with mysql.connector.connect(**db_config) as connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO tarefas (data, funcionario, tarefa, quantidade, valor, total) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (data, funcionario_codigo, tarefa, quantidade, valor, total)
                    cursor.execute(sql, val)
                    connection.commit()
            message = "Tarefa cadastrada!"
            tarefas= consulta_tarefas()
            return render_template('cadastro_tarefas.html', message=message, data=data, nome_completo=funcionario_nome_completo, tarefas=tarefas, tarefa_selecionada=tarefa, valor=valor)
        except Error as e:
            return f'Error: {e}'
    tarefas = consulta_tarefas()
    return render_template('cadastro_tarefas.html', tarefas=tarefas, valor=request.form.get('valor', ''), tarefa_selecionada=request.form.get('tarefa', ''))

def consulta_tarefas():
    try:
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM tarefas ORDER BY id DESC LIMIT 30"
                cursor.execute(sql)
                tarefas = cursor.fetchall()
                tarefas_dict = []
                for tarefa in tarefas:
                    tarefas_dict.append({
                        'data': tarefa[1],
                        'funcionario': tarefa[2],
                        'tarefa': tarefa[3],
                        'qauntidade': tarefa[4],
                        'valor': tarefa[5],
                        'total': tarefa[6]
                    })
                return tarefas_dict
    except Error as e:
        print(f'Error: {e}')
        return f'Error: {e}'


@app.route('/get-funcionario-nome-completo/<int:funcionario_codigo>')
def get_funcionario_nome_completo(funcionario_codigo):
    try:
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT nome_completo FROM funcionarios WHERE codigo = %s"
                val = (funcionario_codigo,)
                cursor.execute(sql, val)
                nome_completo = cursor.fetchone()[0]
                if nome_completo:
                    return nome_completo
                else:
                    return ""
    except Error as e:
        return f'Error: {e}'

@app.route('/get_tarefas/<int:funcionario_codigo>')
def get_tarefas(funcionario_codigo):
    try:
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT data, tarefa, quantidade, valor, total FROM tarefas WHERE funcionario = %s ORDER BY data DESC LIMIT 30"
    except Error as e:
        return f'Error: {e}'

# Consultar e excluir tarefas
@app.route('/consulta_tarefas_por_periodo', methods=['GET', 'POST'])
def consulta_tarefas_por_periodo():    
    if request.method == 'POST':
        data_inicial = request.form['data_inicial']
        data_final = request.form['data_final']
        funcionario_codigo = request.form['funcionario']      

        try:
            with mysql.connector.connect(**db_config) as connection:
                with connection.cursor() as cursor:
                    sql = """
                        SELECT * FROM tarefas
                        WHERE data BETWEEN %s AND %s AND funcionario = %s
                        ORDER BY data DESC
                    """
                    val = (data_inicial, data_final, funcionario_codigo)
                    cursor.execute(sql, val)
                    tarefas = cursor.fetchall()

            tarefas_dict = []
            for tarefa in tarefas:
                tarefas_dict.append({
                    'id': tarefa[0],
                    'data': tarefa[1],
                    'funcionario': tarefa[2],
                    'tarefa': tarefa[3],
                    'quantidade': tarefa[4],
                    'valor': tarefa[5],
                    'total': tarefa[6]
                })
            if not tarefas_dict:
                flash("SEM TAREFAS LANÇADAS NESTE PERÍODO PARA ESTE FUNCIONÁRIO")

            flash_messages = [message for message in get_flashed_messages()]

            return render_template('consulta_tarefas_por_periodo.html', tarefas=tarefas_dict, data_inicial=data_inicial, data_final=data_final, funcionario_codigo=funcionario_codigo, flash_messages=flash_messages)

        except Error as e:
            return f'Error: {e}'

    return render_template('consulta_tarefas_por_periodo.html')

@app.route('/excluir_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
def excluir_tarefa(tarefa_id):
    try:
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM tarefas WHERE id = %s"
                val = (tarefa_id,)
                cursor.execute(sql, val)
                connection.commit()

            flash("TAREFA EXCLUÍDA")

        data_inicial = request.form.get('data_inicial')
        data_final = request.form.get('data_final')
        funcionario_codigo = request.form.get('funcionario')

        return render_template('consulta_tarefas_por_periodo.html', data_inicial=data_inicial, data_final=data_final, funcionario_codigo=funcionario_codigo)
    
    except Error as e:
        return f'Error: {e}'
    
    return redirect(url_for('consulta_tarefas_por_periodo', data_inicial=data_inicial, data_final=data_final, funcionario_codigo=funcionario_codigo))
    
    
# Complementar mínima diária    
@app.route('/complementar_tarefas_periodo', methods=['GET', 'POST'])
def complementar_tarefas_periodo():
    if request.method == 'POST':
        data_inicial = request.form['data_inicial']
        data_final = request.form['data_final']
        try:
            with mysql.connector.connect(**db_config) as connection:
                with connection.cursor() as cursor:
                    sql = "SELECT data, funcionario, SUM(total) as total FROM tarefas WHERE tarefa = 'CORTE' AND data BETWEEN %s AND %s GROUP BY data, funcionario HAVING total < 52.35"
                    val = (data_inicial, data_final)
                    cursor.execute(sql, val)
                    tarefas = cursor.fetchall()
                    for tarefa in tarefas:
                        data = tarefa[0]
                        funcionario = tarefa[1]
                        total_faltante = Decimal('52.35') - tarefa[2]

                        sql_check = "SELECT 1 FROM tarefas WHERE data = %s AND funcionario = %s AND tarefa = 'COMPLEMENTO'"
                        val_check = (data, funcionario)
                        cursor.execute(sql_check, val_check)
                        if cursor.fetchone():  # Se houver um COMPLEMENTO não iserir um novo, né
                            continue

                        sql = "INSERT INTO tarefas (data, funcionario, tarefa, quantidade, valor, total) VALUES (%s, %s, 'COMPLEMENTO', %s, %s, %s)"
                        val = (data, funcionario, 1, total_faltante, total_faltante)
                        cursor.execute(sql, val)
                        connection.commit()
                    flash('Tarefas complementadas com sucesso!', 'success')
        except Error as e:
            flash(f'Error: {e}', 'danger')

        return redirect(url_for('complementar_tarefas_periodo'))
    return render_template('complementar_tarefas_periodo.html')

# GERAR RELATÓRIO 
@app.route('/relatorio/<data_inicial>/<data_final>')
def relatorio(data_inicial=None, data_final=None):
    if data_inicial is None or data_final is None:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
        data_final = datetime.strptime(data_final, '%Y-%m-%d')

    relatorio = gerar_relatorio(data_inicial, data_final)

    return render_template('relatorio.html', relatorio=relatorio, data_inicial=data_inicial, data_final=data_final)

@app.route('/gerar-relatorio', methods=['POST'])
def gerar_relatorio_view():
    data_inicial = request.form['data_inicial']
    data_final = request.form['data_final']

    data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
    data_final = datetime.strptime(data_final, '%Y-%m-%d')

    relatorio = gerar_relatorio(data_inicial, data_final)

    return render_template('relatorio.html', relatorio=relatorio, data_inicial=data_inicial, data_final=data_final)

def gerar_relatorio(data_inicial, data_final):
    try:
        with mysql.connector.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                sql = """
                    SELECT f.codigo, f.nome_completo, t.data, t.tarefa, t.quantidade, t.valor, t.total
                    FROM funcionarios f
                    JOIN tarefas t ON f.codigo = t.funcionario
                    WHERE t.data BETWEEN %s AND %s
                    ORDER BY f.codigo, t.data
                """
                val = (data_inicial, data_final)
                cursor.execute(sql, val)
                relatorio_data = cursor.fetchall()
    except Error as e:
        return f'Error: {e}'

    funcionarios_data = defaultdict(list)
    for row in relatorio_data:
        funcionarios_data[row[0]].append({
            'nome_completo': row[1],
            'data': row[2],
            'tarefa': row[3],
            'quantidade': row[4],
            'valor': row[5],
            'total': row[6]
        })
        
    for funcionario_codigo, funcionario_tarefas in funcionarios_data.items():
        total_geral = sum(tarefa['total'] for tarefa in funcionario_tarefas)
        funcionario_tarefas.append({'total_geral': total_geral})    

    return funcionarios_data

@app.route('/relatorio_csv', methods=['GET', 'POST'])
def relatorio_csv():
    if request.method == 'POST':
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        try:
            with mysql.connector.connect(**db_config) as connection:
                with connection.cursor() as cursor:
                    sql = """
                        SELECT tarefas.funcionario, SUM(tarefas.total) AS total, 
                               COUNT(CASE WHEN tarefas.tarefa = 'FALTA' THEN 1 ELSE NULL END) AS falta_count
                        FROM tarefas
                        WHERE tarefas.data BETWEEN %s AND %s
                        GROUP BY tarefas.funcionario
                    """
                    val = (data_inicio, data_fim)
                    cursor.execute(sql, val)
                    relatorio_data = cursor.fetchall()

            # Cria arquivo CSV
            with open('relatorio.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Funcionario', 'Total', 'Falta Count'])
                for row in relatorio_data:
                    writer.writerow([row[0], row[1], row[2]])

            flash('Relatório gerado com sucesso!', 'success')

            return redirect(url_for('relatorio_csv'))
        except Error as e:
            return f'Error: {e}'


    return render_template('relatorio_csv.html')

if __name__ == '__main__':
    app.run()
