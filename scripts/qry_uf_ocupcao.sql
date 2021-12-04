/* Base de cálculo para média de salário por estado*/
      select cbo.codigo || ' - ' || cbo.descricao as ocupacao
			 ,uf.descricao as uf
			 ,c.salario
		from caged               as c
   left join cbo2002ocupacao     as cbo  on c.cbo2002ocupacao     =  cbo.codigo
   left join sexo                as sx   on c.sexo                =   sx.codigo
   left join uf                          on c.uf                  =   uf.codigo
       where c.saldomovimentacao = '1' -- desconsidera o salário no momento do desligamento
	     and cbo.descricao in ('Estatistico')
;
