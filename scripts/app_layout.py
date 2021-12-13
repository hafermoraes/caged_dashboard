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
date_choice = html.Div(children = [
    #html.P("Horizonte temporal da análise: "),
    html.Label("De: "),
    dcc.Dropdown(
        id='from-date-dropdown',
        options=[{'label': i, 'value':i} for i in comp],
        clearable=False,
        value=comp[0]
    ),
    html.Label("Até: "),
    dcc.Dropdown(
        id='to-date-dropdown',
        options=[{'label': i, 'value':i} for i in comp],
        clearable=False,
        value=comp[-1]
    )
])

# Escolha da profissão
occp_dropdown = html.Div(children = [
    html.Label("Ocupação (CBO2002): "),
    dcc.Dropdown(
        id='occp-dropdown',
        options=[{'label': i, 'value':i} for i in occp['occp']],
        clearable=False,
        value='211205 - Estatistico'
    )
])

# Escolha do CNAE de referência
cnae_dropdown = html.Div(children = [
    html.Label("Seção do CNAE: "),
    dcc.Dropdown(
        id='cnae-dropdown',
        options=[{'label': i, 'value':i} for i in ref_cnae],
        clearable=False,
        value='Q - Saúde Humana e Serviços Sociais'
    )
])

# Escolha do Porte de referência
porte_dropdown = html.Div(children = [
    html.Label("Porte da empresa: "),
    dcc.Dropdown(
        id='porte-dropdown',
        options=[{'label': i, 'value':i} for i in ref_porte],
        clearable=False,
        value='De 100 a 249'
    )
])

# Escolha da UF de referência
# uf_dropdown = html.Div(children = [
#     html.Label("Estado: "),
#     dcc.Dropdown(
#         id='uf-dropdown',
#         options=[{'label': i, 'value':i} for i in ref_uf],
#         clearable=False,
#         value='São Paulo'
#     )
# ])


# Escolha da função de agregação (mediana ou média)
agg_radioitem = html.Div(children = [
    html.Label(["Função de agregação mensal: "]),
    dcc.RadioItems(
        options=[
            {'label': ' Mediana ', 'value': 'median'},
            {'label': ' Média ', 'value': 'mean'}
        ],
        value='median',
        labelStyle={'display': 'inline-block'}
    )
])


# dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Graphs

# estilo (CSS) para a barra lateral esquerda
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# barra lateral esquerda
sidebar = html.Div(
    [
        date_choice,
        html.Br(),
        occp_dropdown,
        html.Br(),
        cnae_dropdown,
        html.Br(),
        porte_dropdown,
        html.Br(),
        # uf_dropdown,
        # html.Br(),
        agg_radioitem
    ],
    style = SIDEBAR_STYLE,
)

# estilo para a barra de conteúdo (direita)
CONTENT_STYLE = {
    "margin-left": "22rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div(children =
    [
        html.H3("Comparativo salarial (base CAGED/eSocial)")
    ],
    style=CONTENT_STYLE,
)


# App.layout


## Dash Bootstrap !!
app.layout = html.Div( [sidebar, content] )

# callbacks
@app.callback(
    dash.dependencies.Output('to-date-dropdown', 'options'),
    [dash.dependencies.Input('from-date-dropdown', 'value')])
def update_output(value):
    comp_max = []
    for mes in comp:
        if mes >= value:
            comp_max.append(mes)
    return [{'label': i, 'value':i} for i in comp_max]


if __name__ == '__main__':
    app.run_server(debug=True)
