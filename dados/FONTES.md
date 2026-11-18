# Fontes dos dados

Todos os dados são abertos e vêm do portal de dados abertos da Prefeitura de Belo Horizonte (CKAN: ckan.pbh.gov.br). Acessados em 16/11/2026.

| Arquivo | Conjunto de dados | Tamanho | Uso |
|---|---|---|---|
| `brutos/bhtrans_frota/cadastro_frota_agosto_2026.csv` | Cadastro de Frota do Sistema Convencional (frota cadastrada no 1º dia do mês, convencional e MOVE) | 336 KB | Contar ônibus cadastrados por consórcio |
| `brutos/bhtrans_mco_agosto_2026/mco_agosto_2026.csv` | Mapa de Controle Operacional (MCO) Consolidado, agosto de 2026 | 78 MB | Passageiros, viagens, km e ônibus em operação por dia útil |
| `brutos/bhtrans_frota/dicionario_dados_frota.pdf` | Dicionário de dados da frota | 149 KB | Significado dos campos |
| `brutos/bhtrans_mco_agosto_2026/dicionario_mco.pdf` | Dicionário de dados do MCO | 179 KB | Significado dos campos, tipos de dia e códigos de consórcio |

## Definições usadas

- **Regiões:** os 4 consórcios do sistema convencional, como definem os dicionários: 801 Pampulha, 802 BH Leste, 803 Dez, 804 Dom Pedro II.
- **Dia útil:** `TIPO DIA = 8` (Anexo 01 do dicionário do MCO). Agosto de 2026 tem 21 dias úteis.
- **Viagem realizada:** qualquer linha do MCO cuja ocorrência não seja `VN` (viagem não realizada).
- **Viagem normal:** ponto de controle 1 ou 2 (0 = ociosa, 3 = transferência). Usada para contar viagens e km.
- **Passageiros:** coluna `TOTAL USUARIOS`, vinda da bilhetagem eletrônica, somada por dia e depois média dos dias úteis.
- **Ônibus em operação:** nº de veículos distintos que fizeram ao menos uma viagem no dia, por consórcio, média dos dias úteis.

## Limitações conhecidas dos dados

1. **O MCO não traz todos os passageiros.** O próprio dicionário avisa que passageiros das linhas de bloqueio das estações BHBUS e das estações de transferência do MOVE não são informados.
2. **O cadastro de frota e a operação não batem.** Cerca de 32% das viagens do MCO foram feitas por veículos cadastrados em outro consórcio. Por isso a "frota atual" do modelo é a que de fato operou (MCO), a mesma fonte da demanda. A frota cadastrada fica como referência na tabela.
3. **Colunas deslocadas no cadastro.** Neste arquivo, os dados das colunas de portas, assentos e área útil não correspondem aos cabeçalhos (por exemplo, a "área útil" tem valores como 39). Por isso essas colunas **não foram usadas**.
4. **Ônibus em mais de um consórcio no mesmo dia** são contados em cada um, então a soma (2.866) pode ser levemente maior que o número de veículos distintos.
5. Um único mês. Os resultados valem para agosto de 2026, em dia útil.

## Como baixar de novo

Os links dos arquivos estão no catálogo do portal: procurar por "Mapa de Controle Operacional (MCO) Consolidado" e "Cadastro de Frota do Sistema Convencional" em ckan.pbh.gov.br.
