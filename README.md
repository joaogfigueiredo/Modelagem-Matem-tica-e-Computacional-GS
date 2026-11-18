# Modelagem Matemática e Computacional: redistribuição da frota de ônibus

Trabalho da Global Solution 2026.2 (FIAP, 1º CC). O enunciado pede um modelo matemático e computacional da distribuição atual da frota de ônibus entre as regiões da cidade, uma proposta de redistribuição e a avaliação dos resultados na gestão do transporte público.

**Cidade:** Belo Horizonte. **Regiões:** as 4 áreas de operação (consórcios): Pampulha, BH Leste, Dez e Dom Pedro II. **Dados:** reais, da Prefeitura de BH (BHTRANS), agosto de 2026.

## Resultado em uma frase

Com 101 ônibus remanejados (3,5% da frota de 2.866), a diferença de carga entre as regiões cai de 27% (razão máx/mín de 1,27) para praticamente zero. Dez recebe 93 ônibus e Pampulha cede 95.

## Como rodar

```bash
pip install -r requirements.txt
python scripts/preparar_dados.py     # só se tiver os dados brutos (ver abaixo)
python modelo/modelo_frota.py        # resultado no terminal
python scripts/gerar_notebook.py     # regenera e executa o notebook
```

O notebook pronto, com gráficos, é `modelo/modelo_frota.ipynb`.

Os dados brutos (`dados/brutos/`, o MCO tem 78 MB) não vão para o GitHub. As tabelas pequenas, `dados/frota_por_regiao.csv` e `dados/demanda_por_regiao.csv`, já estão prontas e bastam para rodar o modelo.

## Estrutura

```
Modelagem Matemática e Computacional/
├── README.md
├── requirements.txt
├── dados/
│   ├── frota_por_regiao.csv       frota cadastrada e em operação, por região
│   ├── demanda_por_regiao.csv     passageiros, viagens e km por dia útil, por região
│   ├── FONTES.md                  de onde vieram os dados e limitações
│   └── brutos/                    arquivos originais baixados (fora do GitHub)
├── scripts/
│   ├── preparar_dados.py          dados brutos -> tabelas por região
│   └── gerar_notebook.py          monta e executa o notebook
├── modelo/
│   ├── MODELO_MATEMATICO.md       variáveis, função objetivo e restrições
│   ├── modelo_frota.py            o modelo em código (programação linear inteira)
│   └── modelo_frota.ipynb         análise completa, com gráficos
├── resultados/
│   ├── comparativo_antes_depois.png
│   ├── sensibilidade.png / sensibilidade.csv
│   └── tabela_resultados.csv
└── docs/
    └── ANALISE_E_CONCLUSAO.md     interpretação, impacto e limitações
```
