#!/usr/bin/env python
# encoding: utf-8

import yaml
import json
import sqlite3
import pandas as pd
from flask import Flask, request, Response
from flasgger import Swagger


def load_ibge_json():
    with open('/home/red2581/mysite/ibge_municipios.json', 'r', encoding='utf-8') as file:
        ibge_muni_json = json.load(file)

    cod_ibge = []
    name_ibge = []

    for cidade in ibge_muni_json:
        cod_ibge.append(cidade['ibge_code'])
        name_ibge.append(cidade['municipio'])

    df_ibge = pd.DataFrame({'cod_municipio': cod_ibge,
                            'nome_municipio_ibge': name_ibge})

    return df_ibge


def createDB():
    conn = sqlite3.connect('database_teste.db')

    with open('/home/red2581/mysite/crop_data.sql', 'r', encoding='utf-8') as sql_file:
        try:
            sql_script = sql_file.read()
            conn.executescript(sql_script)

        except Exception:
            conn.cursor()

    query = "SELECT * FROM crop_data"
    df_raw = pd.read_sql_query(query, conn)

    conn.close()

    df = df_raw.copy()

    null_values = ['-', '...']

    for element_type in null_values:
        filter_curr_null_value = df['valor'] != element_type
        df = df[filter_curr_null_value]

    df['valor'] = df['valor'].astype(int)

    df_ibge = load_ibge_json()
    final_df = df.merge(df_ibge, on='cod_municipio', how='left')
    final_df['nome_municipio_ibge'] = final_df['nome_municipio_ibge'].fillna(value='Sem Registro')

    return final_df


app = Flask(__name__)
DB = createDB()
swagger = Swagger(app, template_file='swagger.yml')

@app.route('/', methods=['GET'])
def query_records():
    try:
        cod_ano = int(request.args.get('cod_ano'))
        cod_variavel = int(request.args.get('cod_variavel'))
        cod_produto_lavouras_temporarias = int(request.args.get('cod_produto_lavouras_temporarias'))
        cod_municipio = int(request.args.get('cod_municipio'))

    except Exception:
        return "Input precisam ser números inteiros.", 400

    filtro_ano = DB['cod_ano'] == cod_ano
    filtro_var = DB['cod_variavel'] == cod_variavel
    filtro_prod_lav_tmp = DB['cod_produto_lavouras_temporarias'] == cod_produto_lavouras_temporarias
    filtro_muni = DB['cod_municipio'] == cod_municipio

    db_filtered = DB[filtro_ano & filtro_var & filtro_prod_lav_tmp & filtro_muni]

    if len(db_filtered) == 0:
        return "Data not found.", 400

    resp = {}

    for column in db_filtered.columns:
        resp[column] = db_filtered[column].iloc[0]

    resp = str(resp).replace("'", "\"")

    return resp

@app.route('/swaggeryml', methods=['GET'])
def get_swagger():
    with open('/home/red2581/mysite/swagger.yml', 'r', encoding='utf-8') as swagger_file:
        swagger_spec = yaml.safe_load(swagger_file)

        return Response(yaml.dump(swagger_spec), content_type='text/yaml')
