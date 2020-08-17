import re

from flask import request, jsonify
import flask
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def check_cnpj(cnpj):
    """Check if CNPJ is in a valid format and return True."""
    pattern = "^[0-9][0-9]\.[0-9][0-9][0-9]\.[0-9][0-9][0-9]/" \
             "[0-9][0-9][0-9][0-9]\-[0-9][0-9]$"

    if re.match(pattern, cnpj):
        query = """SELECT * FROM estabelecimentos WHERE
                cnpj = "%s";""" % (cnpj)
                
        conn = sqlite3.connect('transations.db')
        cur = conn.cursor()
        transations = cur.execute(query).fetchall()
        
        if len(transations) == 0:
            return False

        return True
    else:
        return False

def check_cpf(cpf):
    """Check if CPF is in a valid format and return True."""
    pattern = '^[0-9][0-9][0-9]\.[0-9][0-9][0-9]\.[0-9][0-9][0-9]\-[0-9][0-9]'
    
    if re.match(pattern, cpf):
        return True
    else:
        return False

def check_value(value):
    """Check if the value is in a valid format and return True."""
    if isinstance(value, float):
        value = str(value).split('.')
    
        if len(value[1]) <= 2:
            return True

    # If value is not float or has more than 2 decimals, return False
    return False

@app.errorhandler(404)
def page_not_found(e):
    err = str(e)
    return "<h1>" + err + "</h1><p>O recurso não pode ser encontrado.</p>", e

@app.route('/api/v1/transacao', methods=['POST'])
def save_transation():
    """Validate the transation format, insert it to database and return 201."""
    cnpj = request.json['estabelecimento']
    cpf = request.json['cliente']
    value = request.json['valor']
    description = request.json['descricao']

    # Check the entire data
    if check_cnpj(cnpj) and check_cpf(cpf) and check_value(value):
        
        # Once the data is checked, make and execute a query with it
        query = """INSERT INTO recebimentos (cliente, cnpj_estabelecimento,
                   valor, descricao) VALUES ("%s", "%s", %s, "%s");
        """ % (cpf, cnpj, value, description)
        
        conn = sqlite3.connect('transations.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        
        return jsonify({"aceito": True}), 201

    else:
        return jsonify({"aceito": False}), 400

@app.route('/api/v1/estabelecimento', methods=['GET'])
def get_transations_from_emporium():
    """Return list with all transations of a specific emporium.""" 
    query_parameters = request.args
    # No need to check the CNPJ now, do it below 
    cnpj = query_parameters.get('cnpj')

    try:
        # Make and execute query to get the list of transations
        query = """SELECT * FROM recebimentos WHERE
                cnpj_estabelecimento = "%s";""" % (cnpj)
                
        conn = sqlite3.connect('transations.db')
        cur = conn.cursor()
        transations = cur.execute(query).fetchall()
                
        # If the query does not return anything, return 400
        if len(transations) == 0:
            return page_not_found(400)

        # Make and execute query to get the emporium data
        query = """SELECT * FROM estabelecimentos WHERE
                cnpj = "%s";""" % (cnpj)
                
        emporium_data = cur.execute(query).fetchone()

        # Next step: Formatting and returning all this data to client
        return list_transations_from_emporium(transations, emporium_data)

    except sqlite3.OperationalError:
        return page_not_found(404)

def list_transations_from_emporium(transations, emporium_data):
    """Format and return formatted list to client."""
    total_value = 0
    receivements = []

    # Format transation list
    for transation in transations:
        receivements.append({
            "cliente": transation[1],
            "valor": transation[3], 
            "descricao": transation[4]
            })
        total_value += transation[3]

    # Format emporium data
    emporium = {
        "nome": emporium_data[0], 
        "cnpj": emporium_data[1], 
        "dono": emporium_data[2], 
        "telefone": emporium_data[3]
        }

    # Format final response (emporium data, transation list and total value)
    response = {
        "estabelecimento": emporium, 
        "recebimentos": receivements, 
        "total_recebido": total_value
        }
        
    return jsonify(response)    
    
    #elif request.method == 'POST':
        
app.run()