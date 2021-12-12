# -*- coding: utf-8 -*-

# Rode este app digitando `python3 app.py` no terminal
#  e visite http://127.0.0.1:8050/ no seu navegador.

import dash
import datetime
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import db_connect    # conn (estabelece a conexão com o banco sqlite3 em ../data/caged.db)
import pre_process   # qry_base_table (consulta baseada em variáveis de input)
import pandas as pd  # read_sql_query(), unique(), tolist()

# abre a conexão com o banco de dados
conn = db_connect.sql_connection()


# Variáveis de interação com o usuário do dashboard
#  Ocupação
occp      = pd.read_sql_query( con = conn, sql = "select codigo || ' - ' || descricao as occp from cbo2002ocupacao" )
#  Competência (horizonte temporal da análise via slider)
comp      = pd.read_sql_query( con = conn, sql = "select mes as comp from competencia order by 1 asc" )['comp'].tolist()
#  Referências para cards e bar-plots comparativos entre CNAE, porte, UF e escolaridade
ref_cnae  = pd.read_sql_query( con = conn, sql = "select codigo || ' - ' || descricao as cnae from secao order by 1 asc" )['cnae']
ref_porte = pd.read_sql_query( con = conn, sql = "select codigo + 0E0, descricao from tamestabjan order by 1 asc" )['descricao']
ref_uf    = pd.read_sql_query( con = conn, sql = "select codigo + 0E0, descricao from uf order by 2 asc" )['descricao']
ref_educ  = pd.read_sql_query( con = conn, sql = "select codigo + 0E0, descricao from graudeinstrucao order by 1 asc" )['descricao']


# Escolha do horizonte temporal
date_slider = html.Div([
    dcc.RangeSlider(
        id      ='id_date_slider',
        min     = 0,
        max     = len(comp)-1,
        marks   = {comp.index(s): str(s) for s in comp},
        value   = [ 0, len(comp)-1 ],
        tooltip = {"placement": "bottom", "always_visible": False}
    ),
    html.Div(id='output-container-date-slider')
])

# Escolha da profissão
occp_dropdown = html.Div([
    dcc.Dropdown(
        id='occp-dropdown',
        options=[{'label': i, 'value':i} for i in occp['occp']],
        clearable=False,
        value='211205 - Estatistico'
    ),
    html.Div(id='output-container-occp-dropdown')
])

# Escolha do CNAE de referência
cnae_dropdown = html.Div([
    dcc.Dropdown(
        id='cnae-dropdown',
        options=[{'label': i, 'value':i} for i in ref_cnae],
        clearable=False,
        value='Q - Saúde Humana e Serviços Sociais'
    ),
    html.Div(id='output-container-cnae-dropdown')
])

# Escolha do Porte de referência
porte_dropdown = html.Div([
    dcc.Dropdown(
        id='porte-dropdown',
        options=[{'label': i, 'value':i} for i in ref_porte],
        clearable=False,
        value='De 100 a 249'
    ),
    html.Div(id='output-container-porte-dropdown')
])

# Escolha da UF de referência
uf_dropdown = html.Div([
    dcc.Dropdown(
        id='uf-dropdown',
        options=[{'label': i, 'value':i} for i in ref_uf],
        clearable=False,
        value='São Paulo'
    ),
    html.Div(id='output-container-uf-dropdown')
])


# dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Graphs



# App.layout

## Dash Bootstrap !!
app.layout = dbc.Container(
    [
        html.H1("Comparativo salarial (base CAGED/eSocial)"),
        html.Hr(),
        html.P("Horizonte temporal da análise: "),
        date_slider,
        html.P("Ocupação: "),
        occp_dropdown,
        html.P("Seção do CNAE: "),
        cnae_dropdown,
        html.P("Porte da empresa: "),
        porte_dropdown,
        html.P("Estado: "),
        uf_dropdown
    ], # dbc.container
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=True)
