
import db_connect    # conn (estabelece a conexão com o banco sqlite3 em ../data/caged.db)
import pre_process   # qry_base_table (consulta baseada em variáveis de input)
import pandas as pd  # read_sql_query

# abre a conexão com o banco de dados
conn = db_connect.sql_connection()

# Consultas simples (1 ou poucas linhas)
#   qry   = "SELECT * FROM regiao LIMIT 3;"
#   df    = pd.read_sql_query( qry, conn )

# Consultas baseadas em arquivos .sql (consultas complexas)
#   query = open('qry_uf_ocupcao.sql','r')
#   df    = pd.read_sql_query( query.read() , conn )
#   query.close()

# Consulta usando variáveis externas à instrução sql original
qry = pre_process.qry_base_table(
    input_dt_inicial = '201901'
    ,input_dt_final  = '202010'
    ,input_ocupacao  = 'Estatistico'
)

#  Execução da consulta contra o banco, guardando o resultado no data frame do pandas
df = pd.read_sql_query( qry, conn )

# fecha conexão com banco de dados
conn.close()
