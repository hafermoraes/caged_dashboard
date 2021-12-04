
      select c.competenciamov as mes
			 ,rg.descricao as regiao
			 ,uf.descricao as uf
			 ,mun.descricao as municipio
			 ,sc.codigo || ' - ' || sc.descricao as secao
			 ,cnae.codigo || ' - ' || cnae.descricao as cnae
			 ,ct.descricao as categoria
			 ,cbo.codigo || ' - ' || cbo.descricao as ocupacao
			 ,ed.descricao as instrucao
			 ,rc.descricao as raca
			 ,sx.descricao as sexo
			 ,tam.descricao as tamanho
			 ,c.salario
			 ,case when c.saldomovimentacao = '1' then 'admissão' else 'desligamento' end as movimentacao
			 ,def.descricao as deficiencia
			 ,tpar.descricao as trab_parcial
			 ,tint.descricao as trab_intermitente
			 ,orig.descricao as origem_info
		from caged               as c
   left join categoria           as ct   on c.categoria           =   ct.codigo
   left join cbo2002ocupacao     as cbo  on c.cbo2002ocupacao     =  cbo.codigo
   left join graudeinstrucao     as ed   on c.graudeinstrucao     =   ed.codigo
   left join municipio           as mun  on c.municipio           =  mun.codigo
   left join racacor             as rc   on c.racacor             =   rc.codigo
   left join sexo                as sx   on c.sexo                =   sx.codigo
   left join regiao              as rg   on c.regiao              =   rg.codigo
   left join uf                          on c.uf                  =   uf.codigo
   left join secao               as sc   on c.secao               =   sc.codigo
   left join subclasse           as cnae on c.subclasse           = cnae.codigo
   left join tamestabjan         as tam  on c.tamestabjan         =  tam.codigo
   left join tipodeficiencia     as def  on c.tipodedeficiencia   =  def.codigo
   left join indtrabintermitente as tint on c.indtrabintermitente = tint.codigo
   left join indtrabparcial      as tpar on c.indtrabparcial      = tpar.codigo
   left join indicadoraprendiz   as apr  on c.indicadoraprendiz   =  apr.codigo
   left join origemdainformacao  as orig on c.origemdainformacao  = orig.codigo
   -- limit 5
;
