
import db_connect    # conn (estabelece a conexão com o banco sqlite3 em ../data/caged.db)
import pre_process   # qry_base_table (consulta baseada em variáveis de input)
import pandas as pd  # read_sql_query(), unique(), tolist()

# abre a conexão com o banco de dados
conn = db_connect.sql_connection()

# Variáveis de interação com o usuário do dashboard
#  Ocupação
occp      = pd.read_sql_query( con = conn, sql = "select codigo || ' - ' || descricao as occp from cbo2002ocupacao order by 1 asc" )['occp']
#  Competência (horizonte temporal da análise via slider)
comp      = pd.read_sql_query( con = conn, sql = "select distinct competenciamov as comp from caged order by 1 asc" )['comp']
#  Referências para cards e bar-plots comparativos entre CNAE, porte, UF e escolaridade
ref_cnae  = pd.read_sql_query( con = conn, sql = "select codigo || ' - ' || descricao as cnae from secao order by 1 asc" )['cnae']
ref_porte = pd.read_sql_query( con = conn, sql = "select codigo + 0E0, descricao from tamestabjan order by 1 asc" )['descricao']
ref_uf    = pd.read_sql_query( con = conn, sql = "select codigo + 0E0, descricao from uf order by 1 asc" )['descricao']
ref_educ  = pd.read_sql_query( con = conn, sql = "select codigo + 0E0, descricao from graudeinstrucao order by 1 asc" )['descricao']


#  Execução da consulta contra o banco, guardando o resultado no data frame do pandas
qry = pre_process.qry_base_table( input_dt_inicial = '201901', input_dt_final  = '202010', input_ocupacao  = 'Estatistico' )
df  = pd.read_sql_query( con = conn, sql = qry )


# Cards

# Gráficos

# Callbacks

# Layout

# Main


