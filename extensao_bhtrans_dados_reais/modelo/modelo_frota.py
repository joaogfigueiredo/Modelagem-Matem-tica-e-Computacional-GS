"""Modelo matemático e computacional de redistribuição da frota de ônibus.

Regiões: as 4 áreas de operação (consórcios) de Belo Horizonte.
Veja modelo/MODELO_MATEMATICO.md para a formulação completa.

Resumo:
  - x[i]  = nº de ônibus na região i depois da redistribuição (inteiro)
  - d[i]  = passageiros por dia útil da região i (dado)
  - x0[i] = nº de ônibus que operam hoje na região i (dado)
  - N     = soma de x0 (a frota total não muda)
  - alvo[i] = N * d[i] / soma(d): frota "proporcional" à demanda
  - minimizar  soma |x[i] - alvo[i]|
    sujeito a  soma x[i] = N  e  (1-folga)*x0[i] <= x[i] <= (1+folga)*x0[i]
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"


def carregar_dados() -> pd.DataFrame:
    """Une frota e demanda em uma tabela, uma linha por região."""
    frota = pd.read_csv(DADOS / "frota_por_regiao.csv")
    demanda = pd.read_csv(DADOS / "demanda_por_regiao.csv").drop(columns="regiao")
    df = frota.merge(demanda, on="regiao_id")
    df["onibus_atuais"] = df["onibus_operando_dia_util"].round().astype(int)
    return df


def passageiros_por_onibus(demanda: np.ndarray, onibus: np.ndarray) -> np.ndarray:
    """Carga média: quantos passageiros por dia cada ônibus atende."""
    return demanda / onibus


def indicadores(demanda: np.ndarray, onibus: np.ndarray) -> dict[str, float]:
    """Métricas de equilíbrio da distribuição."""
    carga = passageiros_por_onibus(demanda, onibus)
    return {
        "carga_media": float(carga.mean()),
        "carga_maxima": float(carga.max()),
        "carga_minima": float(carga.min()),
        "razao_max_min": float(carga.max() / carga.min()),
        "coef_variacao": float(carga.std() / carga.mean()),
    }


def redistribuir(demanda: np.ndarray, atuais: np.ndarray, folga: float = 0.15) -> np.ndarray:
    """Resolve o modelo por programação linear inteira (scipy.optimize.milp).

    Variáveis: [x_1..x_n, t_1..t_n], onde t_i >= |x_i - alvo_i| (valor absoluto linearizado).
    """
    n = len(demanda)
    total = atuais.sum()
    alvo = total * demanda / demanda.sum()

    # Função objetivo: minimizar a soma dos t_i
    c = np.concatenate([np.zeros(n), np.ones(n)])

    eye = np.eye(n)
    zero = np.zeros((n, n))
    restricoes = [
        # t_i - x_i >= -alvo_i   (equivale a x_i - alvo_i <= t_i)
        LinearConstraint(np.hstack([-eye, eye]), lb=-alvo, ub=np.inf),
        # t_i + x_i >= alvo_i    (equivale a alvo_i - x_i <= t_i)
        LinearConstraint(np.hstack([eye, eye]), lb=alvo, ub=np.inf),
        # soma dos x_i = frota total
        LinearConstraint(np.concatenate([np.ones(n), np.zeros(n)]).reshape(1, -1), lb=total, ub=total),
    ]
    limites = Bounds(
        lb=np.concatenate([np.floor((1 - folga) * atuais), np.zeros(n)]),
        ub=np.concatenate([np.ceil((1 + folga) * atuais), np.full(n, np.inf)]),
    )
    integralidade = np.concatenate([np.ones(n), np.zeros(n)])  # x inteiro, t contínuo

    resultado = milp(c, constraints=restricoes, bounds=limites, integrality=integralidade)
    if not resultado.success:
        raise RuntimeError(f"Modelo sem solução: {resultado.message}")
    return np.rint(resultado.x[:n]).astype(int)


def comparar(df: pd.DataFrame, folga: float = 0.15) -> pd.DataFrame:
    """Tabela antes x depois para uma folga."""
    demanda = df["passageiros_dia_util"].to_numpy()
    atuais = df["onibus_atuais"].to_numpy()
    novos = redistribuir(demanda, atuais, folga)
    saida = df[["regiao", "passageiros_dia_util", "onibus_atuais"]].copy()
    saida["onibus_propostos"] = novos
    saida["variacao"] = novos - atuais
    saida["pass_por_onibus_antes"] = passageiros_por_onibus(demanda, atuais).round(1)
    saida["pass_por_onibus_depois"] = passageiros_por_onibus(demanda, novos).round(1)
    # Checagem de custo operacional: o mesmo serviço (km/dia) com outro nº de ônibus.
    km = df["km_dia_util"].to_numpy()
    saida["km_por_onibus_antes"] = (km / atuais).round(1)
    saida["km_por_onibus_depois"] = (km / novos).round(1)
    return saida


def sensibilidade(df: pd.DataFrame, folgas=(0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50)) -> pd.DataFrame:
    """Para cada folga: quanto o desequilíbrio cai e quantos ônibus mudam de região."""
    demanda = df["passageiros_dia_util"].to_numpy()
    atuais = df["onibus_atuais"].to_numpy()
    linhas = []
    for folga in folgas:
        novos = redistribuir(demanda, atuais, folga)
        ind = indicadores(demanda, novos)
        linhas.append({
            "folga": folga,
            "onibus_remanejados": int(np.clip(novos - atuais, 0, None).sum()),
            "coef_variacao": round(ind["coef_variacao"], 4),
            "razao_max_min": round(ind["razao_max_min"], 3),
            "carga_maxima": round(ind["carga_maxima"], 1),
        })
    return pd.DataFrame(linhas)


if __name__ == "__main__":
    dados = carregar_dados()
    print(comparar(dados).to_string(index=False))
    print(sensibilidade(dados).to_string(index=False))
