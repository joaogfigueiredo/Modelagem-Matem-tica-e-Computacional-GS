# Modelo matemático

## Problema

Belo Horizonte tem 4 áreas de operação de ônibus. Cada área recebe uma quantidade diferente de passageiros e opera com uma quantidade diferente de ônibus. Queremos saber se a carga por ônibus é equilibrada e, se não for, como redistribuir a frota.

## Conjuntos, dados e variáveis

| Símbolo | Significado | Origem |
|---|---|---|
| $i \in \{1,2,3,4\}$ | região (Pampulha, BH Leste, Dez, Dom Pedro II) | dicionários da BHTRANS |
| $d_i$ | passageiros por dia útil na região $i$ | MCO, agosto de 2026 |
| $x^0_i$ | ônibus que operam hoje na região $i$ | MCO |
| $N = \sum_i x^0_i$ | frota total (não muda) | calculado |
| $f$ | folga: fração máxima que cada região pode ganhar ou perder | parâmetro (padrão 15%) |
| $x_i$ | **variável:** ônibus na região $i$ depois da redistribuição | inteiro |
| $a_i = N\, d_i / \sum_j d_j$ | frota "ideal" proporcional à demanda | calculado |
| $t_i$ | variável auxiliar para o valor absoluto | contínua |

## Indicador de equilíbrio

Carga da região $i$: $c_i = d_i / x_i$ (passageiros por ônibus por dia). A distribuição é equilibrada quando as $c_i$ são parecidas. Medimos isso pelo **coeficiente de variação** das $c_i$ (desvio padrão dividido pela média) e pela **razão máx/mín**.

## Formulação

$$\min \sum_{i} t_i$$

sujeito a

$$t_i \ge x_i - a_i \qquad t_i \ge a_i - x_i \qquad (i=1..4)$$
$$\sum_i x_i = N$$
$$\lfloor (1-f)\,x^0_i \rfloor \le x_i \le \lceil (1+f)\,x^0_i \rceil$$
$$x_i \in \mathbb{Z}_{\ge 0}, \quad t_i \ge 0$$

As duas primeiras restrições forçam $t_i \ge |x_i - a_i|$, então minimizar $\sum t_i$ minimiza o desvio total em relação à frota ideal. É um problema de **programação linear inteira** (MILP).

## Por que essa formulação

- **Frota proporcional à demanda** é o critério mais simples e justo de equilíbrio: cada ônibus atende o mesmo número de passageiros.
- **A folga $f$** representa a realidade: garagens, contratos e operação limitam o quanto um consórcio pode crescer ou encolher.
- **Inteiros:** não existe meio ônibus.
- A frota total é constante: a proposta redistribui, não compra ônibus.

## Resolução computacional

Código em `modelo/modelo_frota.py`, usando `scipy.optimize.milp`. A função `redistribuir(demanda, atuais, folga)` monta as matrizes e resolve; `sensibilidade()` repete para várias folgas.

## Avaliação da proposta

1. Carga por ônibus por região, antes e depois.
2. Coeficiente de variação e razão máx/mín.
3. Ônibus remanejados (custo da mudança).
4. Quilômetros por ônibus antes e depois (checagem do custo operacional: o mesmo serviço rodado por menos ônibus exige mais km de cada um).
5. Sensibilidade à folga.

## Hipóteses e limites

- Todos os ônibus são equivalentes (mesma capacidade).
- A demanda é a de um dia útil médio de agosto de 2026 e não muda com a redistribuição.
- Mover um ônibus entre consórcios é possível dentro da folga (na prática depende de contratos).
- Com apenas 4 regiões, a solução ótima fica muito próxima da proporcionalidade exata assim que a folga é suficiente (≥ 15%).
