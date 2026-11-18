"""Modelagem Matemática e Computacional - GS 2026.2 (CitizenTech).

Mobilidade urbana: recupera a frota por região com um sistema linear (Etapa 1) e
propõe uma redistribuição por transformação linear (Etapa 2).

Execução: python modelo_frota.py   (gera a pasta resultados/)
"""
import json
from fractions import Fraction
from math import ceil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = Path(__file__).resolve().parent
SAIDA = RAIZ / "resultados"

REGIOES = ["Norte", "Sul", "Leste", "Oeste"]
FROTA_TOTAL = 72
CAPACIDADE = 40
PASSAGEIROS = [560, 760, 720, 840]

# Relatório I. Variáveis na ordem (N, S, L, O); uma linha por registro operacional.
EQUACOES = [
    ("N + S + L + O = 72", [1, 1, 1, 1], 72),
    ("N + 2S + O = 76", [1, 2, 0, 1], 76),
    ("S + 2L = 52", [0, 1, 2, 0], 52),
    ("N + L + 2O = 76", [1, 0, 1, 2], 76),
]


def fmt(v) -> str:
    v = Fraction(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def matriz_str(m) -> list[list[str]]:
    return [[fmt(v) for v in linha] for linha in m]


def eliminar_gauss_jordan(aumentada):
    """Gauss-Jordan com frações exatas. Devolve (matriz final, passos, determinante de A)."""
    m = [[Fraction(v) for v in linha] for linha in aumentada]
    n = len(m)
    det = Fraction(1)
    passos = [{"descricao": "Matriz aumentada [A | b]", "matriz": matriz_str(m)}]
    for c in range(n):
        piv = next((r for r in range(c, n) if m[r][c] != 0), None)
        if piv is None:
            det = Fraction(0)
            continue
        ops = []
        if piv != c:
            m[c], m[piv] = m[piv], m[c]
            det *= -1
            ops.append(f"L{c + 1} <-> L{piv + 1}")
        p = m[c][c]
        det *= p
        if p != 1:
            m[c] = [v / p for v in m[c]]
            ops.append(f"L{c + 1} <- L{c + 1} / {fmt(p)}")
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[c])]
                ops.append(f"L{r + 1} <- L{r + 1} - ({fmt(f)})·L{c + 1}")
        passos.append({"descricao": f"Coluna {c + 1}: " + "; ".join(ops) if ops else f"Coluna {c + 1}: pivô já é 1", "matriz": matriz_str(m)})
    return m, passos, det


def etapa1() -> dict:
    A = [e[1] for e in EQUACOES]
    b = [e[2] for e in EQUACOES]
    aumentada = [linha + [bi] for linha, bi in zip(A, b)]
    final, passos, det = eliminar_gauss_jordan(aumentada)

    posto_A = sum(1 for linha in final if any(v != 0 for v in linha[:4]))
    posto_aug = sum(1 for linha in final if any(v != 0 for v in linha))
    unica = posto_A == posto_aug == len(REGIOES)

    solucao = [final[i][4] for i in range(4)] if unica else None
    x = [int(v) for v in solucao] if unica and all(v.denominator == 1 for v in solucao) else None

    np_A, np_b = np.array(A, float), np.array(b, float)
    conferencia_numpy = np.linalg.solve(np_A, np_b).tolist() if unica else None

    verificacao = []
    if x:
        for texto, coef, rhs in EQUACOES:
            esq = sum(c * xi for c, xi in zip(coef, x))
            verificacao.append({"equacao": texto, "esquerda": esq, "direita": rhs, "ok": esq == rhs})

    return {
        "variaveis": dict(zip(["N", "S", "L", "O"], REGIOES)),
        "equacoes": [{"texto": t, "coeficientes": c, "termo_independente": r} for t, c, r in EQUACOES],
        "A": A,
        "b": b,
        "passos": passos,
        "determinante": fmt(det),
        "determinante_numpy": float(np.linalg.det(np_A)),
        "posto_A": posto_A,
        "posto_aumentada": posto_aug,
        "numero_de_condicao": float(np.linalg.cond(np_A)),
        "solucao_unica": unica,
        "distribuicao_atual": dict(zip(REGIOES, x)) if x else None,
        "x": x,
        "conferencia_numpy": conferencia_numpy,
        "verificacao": verificacao,
        "todas_equacoes_ok": bool(verificacao) and all(v["ok"] for v in verificacao),
    }


def indicadores(x, passageiros=PASSAGEIROS):
    ocupacao = [p / (CAPACIDADE * xi) for p, xi in zip(passageiros, x)]
    nao_atendidos = [max(0, p - CAPACIDADE * xi) for p, xi in zip(passageiros, x)]
    return {
        "onibus": list(x),
        "ocupacao": ocupacao,
        "passageiros_por_onibus": [p / xi for p, xi in zip(passageiros, x)],
        "nao_atendidos": nao_atendidos,
        "total_nao_atendidos": sum(nao_atendidos),
        "ocupacao_maxima": max(ocupacao),
    }


def construir_transformacao(x, necessario, passageiros=PASSAGEIROS):
    """Fluxos guloso: quem mais sobra doa primeiro; quem está mais lotado recebe primeiro."""
    idx = range(len(x))
    saldo = [x[i] - necessario[i] for i in idx]
    doadores = sorted((i for i in idx if saldo[i] > 0), key=lambda i: -saldo[i])
    receptores = sorted((i for i in idx if saldo[i] < 0), key=lambda i: -passageiros[i] / (CAPACIDADE * x[i]))
    sobra = {d: saldo[d] for d in doadores}
    fluxos = []
    for r in receptores:
        falta = -saldo[r]
        for d in doadores:
            q = min(falta, sobra[d])
            if q > 0:
                fluxos.append((d, r, q))
                sobra[d] -= q
                falta -= q
    T = [[Fraction(0)] * len(x) for _ in idx]
    saiu = [0] * len(x)
    for d, r, q in fluxos:
        T[r][d] += Fraction(q, x[d])
        saiu[d] += q
    for j in idx:
        T[j][j] = Fraction(x[j] - saiu[j], x[j])
    return T, fluxos, saldo


def aplicar(T, x):
    return [sum(T[i][j] * x[j] for j in range(len(x))) for i in range(len(x))]


def det_fracao(m):
    _, _, d = eliminar_gauss_jordan([[*linha, 0] for linha in m])
    return d


def etapa2(x) -> dict:
    necessario = [ceil(p / CAPACIDADE) for p in PASSAGEIROS]
    antes = indicadores(x)
    T, fluxos, saldo = construir_transformacao(x, necessario)
    novo_frac = aplicar(T, x)
    novo = [int(v) for v in novo_frac]

    soma_colunas = [sum(T[i][j] for i in range(4)) for j in range(4)]
    menor_coef = min(v for linha in T for v in linha)
    depois = indicadores(novo)

    # Linearidade: T(a·u + b·v) = a·T(u) + b·T(v), testada com vetores quaisquer.
    u, v, a, b = [3, 0, 7, 5], [10, 2, 1, 4], Fraction(2), Fraction(3)
    lhs = aplicar(T, [a * ui + b * vi for ui, vi in zip(u, v)])
    rhs = [a * p + b * q for p, q in zip(aplicar(T, u), aplicar(T, v))]

    return {
        "demanda": [
            {
                "regiao": REGIOES[i],
                "passageiros": PASSAGEIROS[i],
                "capacidade": CAPACIDADE,
                "necessario": necessario[i],
                "atual": x[i],
                "saldo": saldo[i],
            }
            for i in range(4)
        ],
        "total_necessario": sum(necessario),
        "frota_suficiente": sum(necessario) <= FROTA_TOTAL,
        "antes": antes,
        "depois": depois,
        "fluxos": [{"origem": REGIOES[d], "destino": REGIOES[r], "onibus": q} for d, r, q in fluxos],
        "onibus_movidos": sum(q for _, _, q in fluxos),
        "T": matriz_str(T),
        "T_float": [[float(v) for v in linha] for linha in T],
        "novo_vetor": novo,
        "novo_vetor_exato": [fmt(v) for v in novo_frac],
        "soma_das_colunas": [fmt(s) for s in soma_colunas],
        "menor_coeficiente": fmt(menor_coef),
        "total_antes": sum(x),
        "total_depois": sum(novo),
        "total_preservado": sum(novo) == sum(x) and all(s == 1 for s in soma_colunas),
        "sem_alocacao_negativa": menor_coef >= 0 and all(n >= 0 for n in novo),
        "atinge_necessidade": novo == necessario,
        "determinante_T": fmt(det_fracao(T)),
        "linearidade_ok": lhs == rhs,
    }


def grafico_frota(e1, e2, destino: Path) -> None:
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(7.2, 4))
    larg = 0.27
    ax.bar(x - larg, e2["antes"]["onibus"], larg, label="Atual", color="#9aa5b1")
    ax.bar(x, e2["depois"]["onibus"], larg, label="Após redistribuição", color="#0b6e4f")
    ax.bar(x + larg, [d["necessario"] for d in e2["demanda"]], larg, label="Necessário (demanda/40)", color="#e0a100")
    ax.set_xticks(x, REGIOES)
    ax.set_ylabel("Ônibus")
    ax.set_title("Frota por região: atual, após a política e necessária")
    ax.set_ylim(0, 29)
    ax.legend(loc="upper center", ncol=3, fontsize=8)
    fig.tight_layout()
    fig.savefig(destino, dpi=160)
    plt.close(fig)


def grafico_ocupacao(e2, destino: Path) -> None:
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(7.2, 4))
    larg = 0.35
    ax.bar(x - larg / 2, [o * 100 for o in e2["antes"]["ocupacao"]], larg, label="Antes", color="#9aa5b1")
    ax.bar(x + larg / 2, [o * 100 for o in e2["depois"]["ocupacao"]], larg, label="Depois", color="#0b6e4f")
    ax.axhline(100, color="#b42318", linewidth=1, linestyle="--", label="Limite de capacidade (100%)")
    ax.set_xticks(x, REGIOES)
    ax.set_ylabel("Ocupação da capacidade (%)")
    ax.set_title("Ocupação da frota no horário de pico")
    ax.set_ylim(0, 140)
    ax.legend(loc="upper center", ncol=3, fontsize=8)
    fig.tight_layout()
    fig.savefig(destino, dpi=160)
    plt.close(fig)


def executar() -> dict:
    SAIDA.mkdir(exist_ok=True)
    e1 = etapa1()
    if not e1["solucao_unica"] or e1["x"] is None:
        raise SystemExit("O sistema não tem solução única inteira; não é possível recuperar a frota.")
    e2 = etapa2(e1["x"])
    grafico_frota(e1, e2, SAIDA / "frota_antes_depois.png")
    grafico_ocupacao(e2, SAIDA / "ocupacao_antes_depois.png")
    resultado = {"etapa1": e1, "etapa2": e2}
    (SAIDA / "resultados.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def imprimir(res: dict) -> None:
    e1, e2 = res["etapa1"], res["etapa2"]
    print("=== ETAPA 1: distribuição atual ===")
    print("Variáveis: N=Norte, S=Sul, L=Leste, O=Oeste")
    for eq in e1["equacoes"]:
        print("  ", eq["texto"])
    print("det(A) =", e1["determinante"], "| posto(A) =", e1["posto_A"], "| posto([A|b]) =", e1["posto_aumentada"])
    print("Solução única:", e1["solucao_unica"], "->", e1["distribuicao_atual"])
    print("Conferência numpy.linalg.solve:", [round(v, 6) for v in e1["conferencia_numpy"]])
    for v in e1["verificacao"]:
        print(f"  {v['equacao']:<20} {v['esquerda']} == {v['direita']}  {'OK' if v['ok'] else 'FALHOU'}")
    print("\n=== ETAPA 2: política de redistribuição ===")
    for d in e2["demanda"]:
        print(f"  {d['regiao']:<6} demanda {d['passageiros']:>3} -> necessário {d['necessario']:>2} | atual {d['atual']:>2} | saldo {d['saldo']:+d}")
    print("Total necessário:", e2["total_necessario"], "(frota", FROTA_TOTAL, ")")
    print("Fluxos:", [f"{f['origem']}->{f['destino']}: {f['onibus']}" for f in e2["fluxos"]])
    print("Matriz T (linhas: destino N,S,L,O; colunas: origem N,S,L,O):")
    for linha in e2["T"]:
        print("  ", linha)
    print("Soma das colunas:", e2["soma_das_colunas"], "| menor coeficiente:", e2["menor_coeficiente"])
    print("T·x =", e2["novo_vetor"], "| total", e2["total_antes"], "->", e2["total_depois"])
    print("Total preservado:", e2["total_preservado"], "| sem negativos:", e2["sem_alocacao_negativa"], "| atinge a necessidade:", e2["atinge_necessidade"])
    print("det(T) =", e2["determinante_T"], "| linearidade verificada:", e2["linearidade_ok"])
    print("Não atendidos no pico:", e2["antes"]["total_nao_atendidos"], "->", e2["depois"]["total_nao_atendidos"])
    print("Ônibus movidos:", e2["onibus_movidos"], "de", FROTA_TOTAL)


if __name__ == "__main__":
    imprimir(executar())
