
# raw zipped files
DATA       := data
RAW        := raw
SCRIPTS    := scripts
BASE_URL   := ftp://ftp.mtps.gov.br/pdet/microdados/NOVO%20CAGED
ZIPs       := 2020/202001/CAGEDMOV202001.7z \
			  2020/202002/CAGEDMOV202002.7z \
			  2020/202003/CAGEDMOV202003.7z \
			  2020/202004/CAGEDMOV202004.7z \
			  2020/202005/CAGEDMOV202005.7z \
			  2020/202006/CAGEDMOV202006.7z \
			  2020/202007/CAGEDMOV202007.7z \
			  2020/202008/CAGEDMOV202008.7z \
			  2020/202009/CAGEDMOV202009.7z \
			  2020/202010/CAGEDMOV202010.7z \
			  2020/202011/CAGEDMOV202011.7z \
			  2020/202012/CAGEDMOV202012.7z \
			  2021/202101/CAGEDMOV202101.7z \
			  2021/202102/CAGEDMOV202102.7z \
			  2021/202103/CAGEDMOV202103.7z \
			  2021/202104/CAGEDMOV202104.7z \
			  2021/202105/CAGEDMOV202105.7z \
			  2021/202106/CAGEDMOV202106.7z \
			  2021/202107/CAGEDMOV202107.7z \
			  2021/202108/CAGEDMOV202108.7z \
			  2021/202109/CAGEDMOV202109.7z \
			  2021/202110/CAGEDMOV202110.7z 

URL := $(foreach url, $(ZIPs), $(BASE_URL)/$(url) )

all: help

init-debian-based: ## Instalação dos softwares necessários em distribuições baseadas no Debian
	sudo apt-get install wget 
	sudo apt-get install p7zip
	sudo apt-get install sqlite3
	sudo apt-get install python3

fetch: 	## Baixa e prepara dados brutos do novo caged para importação no banco de dados
	@for u in $(URL); do            \
	  wget $$u -O $(RAW)/tmp.7z;    \
	  7z x $(RAW)/tmp.7z -o$(RAW)/; \
	  rm $(RAW)/tmp.7z;             \
	done;
	@for f in $(RAW)/*;                                 \
	do                                                  \
	  tail -n +2 $$f > $(RAW)/aux && mv $(RAW)/aux $$f; \
	done;

db: ## Cria e popula banco de dados caged.db com os dados brutos baixados do ftp do governo
	sqlite3 $(DATA)/caged.db < $(SCRIPTS)/reset_db.sql
	@for f in $(RAW)/*; do                                           \
	  sqlite3 -separator ";" $(DATA)/caged.db ".import $$f caged";   \
	done;
	rm $(RAW)/*

.PHONY: help
help: ## Exibe esta mensagem de ajuda
	@echo 'Documentação do Makefile para construção da base de comparação salarial'
	@echo ''
	@echo 'Uso:'
	@echo '    make [alvo]'
	@echo ''
	@echo 'Alvos:'
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\t%-20s %s\n", $$1, $$2}'
	@echo ''
