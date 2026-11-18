# Modelagem Matemática e Computacional: Mobilidade Urbana Inteligente

Global Solution 2026.2 (FIAP, CitizenTech). Modelagem da frota de ônibus de um município com **sistemas lineares, matrizes e transformações lineares**, implementada em Python.

**Integrantes:** João Guilherme Figueiredo (RM 572697) e Ryan Luther Roque (RM 572993)

## O que o enunciado pede e onde está

| Pedido | Onde |
|---|---|
| Etapa 1: variáveis, modelo, sistema matricial, unicidade (Álgebra Linear), solução em Python, verificação | Relatório, seção 2; `modelo_frota.py`, função `etapa1` |
| Etapa 2: necessidade por região, desequilíbrios, política, transformação linear, matriz e coeficientes, demonstrações | Relatório, seção 3; `modelo_frota.py`, função `etapa2` |
| Código em Python | `modelo_frota.py` (e o notebook `modelo_frota.ipynb`) |
| Relatório | `Relatorio_Modelagem_Matematica_e_Computacional.pdf` |

## Resultados

- Sistema 4×4: det(A) = 3, posto(A) = posto([A | b]) = 4, **solução única**: Norte 12, Sul 20, Leste 16, Oeste 24 (total 72). Os 4 registros são satisfeitos.
- Necessidade pela demanda (passageiros / 40, arredondada para cima): 14, 19, 18 e 21 ônibus (total 72, igual à frota).
- Hoje 160 passageiros ficam sem vaga no pico (Norte 80 e Leste 80).
- Política: mover 4 ônibus (Oeste → Norte 2, Oeste → Leste 1, Sul → Leste 1), representada pela matriz M com colunas somando 1 e coeficientes não negativos. Isso demonstra que o total é preservado e que não há alocação negativa. Depois da política, 0 passageiros sem vaga.

## Como executar

```bash
pip install -r requirements.txt
python modelo_frota.py              # imprime as duas etapas e gera resultados/
python scripts/gerar_relatorio.py   # gera o PDF a partir de resultados/resultados.json
python scripts/gerar_notebook.py    # gera e executa modelo_frota.ipynb
python -m unittest discover -s tests
```

## Estrutura

```
├── modelo_frota.py                 o modelo (Etapas 1 e 2) e os gráficos
├── modelo_frota.ipynb              o mesmo modelo, passo a passo, já executado
├── Relatorio_Modelagem_Matematica_e_Computacional.pdf
├── resultados/                     resultados.json e os dois gráficos
├── scripts/                        geradores do relatório e do notebook
├── tests/test_modelo.py            testes automatizados
└── extensao_bhtrans_dados_reais/   extensão opcional com dados reais de BH (fora do enunciado)
```

## Limitações

Os dados do enunciado são hipotéticos e de um único horário de pico. A matriz M foi calibrada para a distribuição atual; se a frota ou a demanda mudarem, deve ser recalculada com `construir_transformacao` (as propriedades de preservar o total e não gerar valores negativos continuam valendo).

## Entrega

O PDF do enunciado não informa o formato de entrega no portal. Confirmar com o professor; o conjunto natural é `modelo_frota.py`, o notebook e o relatório em PDF.
