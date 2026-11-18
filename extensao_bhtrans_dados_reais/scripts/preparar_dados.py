"""Transforma os dados brutos da BHTRANS em duas tabelas pequenas por região.

Entradas (dados abertos da Prefeitura de Belo Horizonte, ver dados/FONTES.md):
  - dados/brutos/bhtrans_frota/cadastro_frota_agosto_2026.csv
  - dados/brutos/bhtrans_mco_agosto_2026/mco_agosto_2026.csv

Saídas:
  - dados/frota_por_regiao.csv
  - dados/demanda_por_regiao.csv

Rode com:  python scripts/preparar_dados.py
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "dados" / "brutos"
ARQ_MCO = BRUTOS / "bhtrans_mco_agosto_2026" / "mco_agosto_2026.csv"
ARQ_FROTA = BRUTOS / "bhtrans_frota" / "cadastro_frota_agosto_2026.csv"

# Código do consórcio -> nome. Fonte: dicionários de dados da BHTRANS/SUMOB.
REGIOES = {801: "Pampulha", 802: "BH Leste", 803: "Dez", 804: "Dom Pedro II"}
TIPO_DIA_UTIL = 8  # Anexo 01 do dicionário do MCO: 8 = dia útil


def preparar_frota() -> pd.DataFrame:
    """Frota cadastrada no 1º dia do mês, resumida por consórcio."""
    # Atenção: neste arquivo, os cabeçalhos das colunas de portas, assentos e área
    # útil não batem com os dados (ver dados/FONTES.md). Por isso só contamos veículos.
    frota = pd.read_csv(ARQ_FROTA, sep=";", encoding="latin-1", decimal=",")
    return frota.groupby("CONSORCIO").agg(onibus_cadastrados=("NUMERO_VEICULO", "nunique"))


def preparar_demanda() -> pd.DataFrame:
    """Passageiros, viagens e veículos em operação por dia útil, por consórcio."""
    colunas = ["VIAGEM", "PC", "CONCESSIONARIA", "VEICULO", "OCORRENCIA",
               "TIPO DIA", "EXTENSAO", "TOTAL USUARIOS"]
    mco = pd.read_csv(ARQ_MCO, sep=";", encoding="utf-8", low_memory=False)
    mco.columns = [c.strip() for c in mco.columns]
    mco = mco[colunas].copy()
    mco["OCORRENCIA"] = mco["OCORRENCIA"].astype(str).str.strip()

    # Só dias úteis e só viagens realizadas (VN = viagem não realizada).
    mco = mco[(mco["TIPO DIA"] == TIPO_DIA_UTIL) & (mco["OCORRENCIA"] != "VN")]

    # Viagens normais saem do ponto de controle 1 ou 2 (0 = ociosa, 3 = transferência).
    normais = mco["PC"].isin([1, 2])

    por_dia = mco.groupby(["CONCESSIONARIA", "VIAGEM"]).agg(
        passageiros=("TOTAL USUARIOS", "sum"),
        veiculos_operando=("VEICULO", "nunique"),
    )
    por_dia["viagens"] = mco[normais].groupby(["CONCESSIONARIA", "VIAGEM"]).size()
    por_dia["km"] = mco[normais].groupby(["CONCESSIONARIA", "VIAGEM"])["EXTENSAO"].sum() / 1000

    resumo = por_dia.groupby("CONCESSIONARIA").agg(
        passageiros_dia_util=("passageiros", "mean"),
        viagens_dia_util=("viagens", "mean"),
        km_dia_util=("km", "mean"),
        onibus_operando_dia_util=("veiculos_operando", "mean"),
        dias_uteis_considerados=("passageiros", "size"),
    )
    return resumo


def main() -> None:
    frota = preparar_frota()
    demanda = preparar_demanda()

    # Frota "atual" do modelo = veículos que de fato operaram em dia útil (do MCO),
    # a mesma fonte da demanda. A frota cadastrada fica como referência.
    frota["onibus_operando_dia_util"] = demanda.pop("onibus_operando_dia_util")

    for tabela in (frota, demanda):
        tabela.index.name = "regiao_id"
        tabela.insert(0, "regiao", [REGIOES[i] for i in tabela.index])

    saida = RAIZ / "dados"
    frota.round(2).to_csv(saida / "frota_por_regiao.csv", encoding="utf-8")
    demanda.round(1).to_csv(saida / "demanda_por_regiao.csv", encoding="utf-8")
    print(frota.round(2).to_string())
    print(demanda.round(1).to_string())


if __name__ == "__main__":
    main()
