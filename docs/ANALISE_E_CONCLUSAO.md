# Análise e conclusão

## O que os dados mostram (situação atual)

Em um dia útil de agosto de 2026, o sistema convencional de BH transporta em média cerca de 755 mil passageiros (registrados no MCO) com 2.866 ônibus em operação nas 4 áreas.

| Região | Ônibus hoje | Passageiros/dia útil | Passageiros por ônibus |
|---|---:|---:|---:|
| Pampulha | 836 | 195.173 | 233,5 |
| BH Leste | 778 | 206.961 | 266,0 |
| Dez | 752 | 222.391 | 295,7 |
| Dom Pedro II | 500 | 130.084 | 260,2 |

**A distribuição é desequilibrada:** cada ônibus de Dez atende 27% mais passageiros que cada ônibus de Pampulha (razão máx/mín de 1,27, coeficiente de variação de 0,084). Pampulha tem a maior frota e a menor carga; Dez tem a maior demanda e uma frota menor que a de Pampulha e BH Leste.

## A proposta (folga de 15%)

| Região | Hoje | Proposta | Variação | Passageiros/ônibus depois |
|---|---:|---:|---:|---:|
| Pampulha | 836 | 741 | −95 | 263,4 |
| BH Leste | 778 | 786 | +8 | 263,3 |
| Dez | 752 | 845 | +93 | 263,2 |
| Dom Pedro II | 500 | 494 | −6 | 263,3 |

- A carga por ônibus fica praticamente igual nas 4 regiões (263 passageiros/dia): razão máx/mín de 1,001 e coeficiente de variação de 0,0003.
- O ônibus mais carregado passa de 296 para 263 passageiros/dia, uma redução de 11% na pior carga.
- Foram remanejados **101 ônibus**, 3,5% da frota. Quase tudo é uma transferência de Pampulha para Dez.

## Sensibilidade: quanto vale remanejar

| Folga | Ônibus remanejados | Coef. de variação | Carga máxima |
|---:|---:|---:|---:|
| 0% | 0 | 0,0839 | 295,7 |
| 5% | 47 | 0,0480 | 281,5 |
| 10% | 85 | 0,0140 | 268,6 |
| 15% | 101 | 0,0003 | 263,4 |

O ganho é muito rápido no começo: com apenas 47 ônibus movidos (1,6% da frota) a desigualdade cai 43%. Remanejar mais que 101 ônibus não melhora nada, porque o equilíbrio já foi atingido. Uma gestão cautelosa pode começar pela folga de 5% ou 10% e ir ajustando.

## Impacto na gestão do transporte público

- **Equidade:** passageiros de Dez, que hoje viajam em ônibus mais cheios, passam a ter a mesma disponibilidade média que os das outras áreas.
- **Uso da frota:** a mesma quantidade de ônibus atende melhor, sem comprar veículos.
- **Custo operacional (ponto de atenção):** como o serviço em km por dia não muda, tirar ônibus de Pampulha faz cada ônibus de lá rodar mais (158 para 179 km/dia, +13%), enquanto em Dez cada ônibus roda menos (167 para 148 km/dia, −11%). Isso pode aumentar o desgaste e o custo por veículo em Pampulha. A gestão deve considerar esse efeito, por exemplo remanejando só parte dos 101 ônibus.
- **Ligação com o Citizen Assist AI:** equilibrar a oferta de ônibus melhora o acesso das pessoas aos postos de atendimento e serviços que o assistente orienta.

## Limitações

1. O modelo trata os ônibus como equivalentes e ignora horários de pico, tamanho das viagens, tipo de linha (BRT, convencional) e distância.
2. Usa um único mês e só dias úteis; fins de semana e feriados podem exigir outra distribuição.
3. O MCO não inclui passageiros das linhas de bloqueio das estações BHBUS e MOVE, então a demanda pode estar subestimada em algumas áreas.
4. O cadastro de frota e a operação divergem em cerca de 32% das viagens, e por isso o modelo usa a frota que de fato operou.
5. Mover ônibus entre consórcios depende de contratos e garagens. A folga representa isso, mas não substitui uma análise operacional.
6. Com 4 regiões, o resultado quase proporcional é esperado. Um modelo com mais regiões (por exemplo, por linha ou por regional administrativa) seria uma evolução natural.

## Conclusão

A frota de ônibus de BH é desigual entre as áreas de operação: o ônibus de Dez carrega 27% mais passageiros que o de Pampulha. Um remanejamento de 101 ônibus (3,5% da frota), principalmente de Pampulha para Dez, equilibraria a carga em todas as áreas sem aumentar a frota. A decisão exige cuidado com a quilometragem por ônibus e com a viabilidade contratual, e pode ser feita em etapas, já que os primeiros 47 ônibus movidos entregam quase metade do ganho.
