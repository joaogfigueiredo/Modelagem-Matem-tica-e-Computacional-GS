"""Gera o relatório PDF a partir de resultados/resultados.json (nenhum número é digitado à mão)."""
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle

RAIZ = Path(__file__).resolve().parent.parent
RES = json.loads((RAIZ / "resultados" / "resultados.json").read_text(encoding="utf-8"))
E1, E2 = RES["etapa1"], RES["etapa2"]
SAIDA = RAIZ / "Relatorio_Modelagem_Matematica_e_Computacional.pdf"

FONTES = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
pdfmetrics.registerFont(TTFont("Arial", str(FONTES / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONTES / "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONTES / "ariali.ttf")))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", str(FONTES / "arialbi.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-BoldItalic")
MONO = "Courier"
if (FONTES / "consola.ttf").exists():
    pdfmetrics.registerFont(TTFont("Consolas", str(FONTES / "consola.ttf")))
    MONO = "Consolas"

AZUL = colors.HexColor("#14365d")
CINZA = colors.HexColor("#eef2f6")
VERDE = colors.HexColor("#0b6e4f")

corpo = ParagraphStyle("corpo", fontName="Arial", fontSize=10, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6)
h1 = ParagraphStyle("h1", fontName="Arial-Bold", fontSize=15, leading=19, textColor=AZUL, spaceBefore=14, spaceAfter=6, keepWithNext=1)
h2 = ParagraphStyle("h2", fontName="Arial-Bold", fontSize=11.5, leading=15, textColor=AZUL, spaceBefore=9, spaceAfter=4, keepWithNext=1)
celula = ParagraphStyle("celula", fontName="Arial", fontSize=9, leading=12)
celula_c = ParagraphStyle("celula_c", parent=celula, alignment=TA_CENTER)
cab = ParagraphStyle("cab", fontName="Arial-Bold", fontSize=9, leading=12, textColor=colors.white, alignment=TA_CENTER)
mono = ParagraphStyle("mono", fontName=MONO, fontSize=8.6, leading=11, backColor=CINZA, borderPadding=5, spaceBefore=4, spaceAfter=8)
legenda = ParagraphStyle("legenda", fontName="Arial-Italic", fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#444444"), spaceAfter=8)


def pct(v: float) -> str:
    return f"{v * 100:.1f}".replace(".", ",") + "%"


def p(texto: str, estilo=corpo) -> Paragraph:
    return Paragraph(texto, estilo)


def tabela(linhas, larguras, centralizar=True) -> Table:
    dados = [[Paragraph(str(c), cab) for c in linhas[0]]]
    for linha in linhas[1:]:
        dados.append([Paragraph(str(c), celula_c if centralizar else celula) for c in linha])
    t = Table(dados, colWidths=larguras, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CINZA]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c2cc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def matriz_texto(m, aumentada=False) -> str:
    larg = [max(len(m[i][j]) for i in range(len(m))) for j in range(len(m[0]))]
    linhas = []
    for linha in m:
        partes = [linha[j].rjust(larg[j]) for j in range(len(linha))]
        if aumentada:
            corpo_ = "  ".join(partes[:-1]) + "  |  " + partes[-1]
        else:
            corpo_ = "  ".join(partes)
        linhas.append("[ " + corpo_ + " ]")
    return "\n".join(linhas)


def pre(texto: str) -> Preformatted:
    return Preformatted(texto, mono)


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, "Modelagem Matemática e Computacional · Global Solution 2026.2 · CitizenTech")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def figura(nome: str, legenda_txt: str, largura=13.5 * cm):
    img = Image(str(RAIZ / "resultados" / nome))
    prop = img.imageHeight / img.imageWidth
    img.drawWidth, img.drawHeight = largura, largura * prop
    return KeepTogether([img, p(legenda_txt, legenda)])


REG = ["Norte", "Sul", "Leste", "Oeste"]
x = E1["x"]
D = E2["demanda"]
antes, depois = E2["antes"], E2["depois"]
S = []

# Capa
S += [
    Spacer(1, 2.2 * cm),
    Paragraph("Mobilidade Urbana Inteligente", ParagraphStyle("t", fontName="Arial-Bold", fontSize=24, leading=28, textColor=AZUL)),
    Paragraph("Modelagem matemática para a gestão do transporte público", ParagraphStyle("st", fontName="Arial", fontSize=14, leading=18, textColor=colors.HexColor("#333333"), spaceAfter=18)),
    Paragraph("Relatório técnico · Modelagem Matemática e Computacional · Global Solution 2026.2 (CitizenTech)", celula),
    Spacer(1, 0.6 * cm),
    Paragraph("<b>Equipe: Citizen Solutions Tech</b><br/><br/><b>Integrantes</b><br/>João Guilherme Figueiredo · RM 572697<br/>Ryan Luther Roque · RM 572993<br/><br/>"
              "<b>Divisão geral do trabalho:</b> João, códigos e partes complementares; Ryan, lógica e códigos complementares",
              ParagraphStyle("i", fontName="Arial", fontSize=11, leading=16)),
    Spacer(1, 0.8 * cm),
]
S += [
    p("<b>Resumo.</b> A frota de 72 ônibus foi recuperada a partir de quatro registros consolidados, modelados como um sistema linear "
      f"4×4 com determinante {E1['determinante']} (solução única): <b>Norte {x[0]}, Sul {x[1]}, Leste {x[2]}, Oeste {x[3]}</b>. "
      f"Comparada à necessidade estimada pela demanda do pico ({', '.join(str(d['necessario']) for d in D)} ônibus), a frota atual deixa "
      f"{antes['total_nao_atendidos']} passageiros sem vaga. Uma transformação linear de matriz estocástica por colunas redistribui "
      f"{E2['onibus_movidos']} ônibus ({pct(E2['onibus_movidos'] / 72)} da frota), preserva o total de {E2['total_antes']} e leva a "
      f"{depois['total_nao_atendidos']} passageiros não atendidos."),
    p("<b>Aviso.</b> Os dados do enunciado são hipotéticos e simplificam a operação real do transporte público. Os resultados valem para esse "
      "cenário e não representam a operação de nenhuma empresa."),
]

# 1. Premissas
S += [Paragraph("1. Premissas e dados do problema", h1)]
S += [
    p("Quatro centros operacionais atendem as regiões Norte, Sul, Leste e Oeste. Cada ônibus atende apenas a região onde está alocado, "
      "cada passageiro ocupa uma vaga, a capacidade é de 40 passageiros por ônibus, a frota total não pode ser ampliada e as quantidades "
      "são inteiras e não negativas."),
    tabela([["Região", "Passageiros estimados (pico)", "Capacidade por ônibus"]] + [[d["regiao"], d["passageiros"], d["capacidade"]] for d in D],
           [4 * cm, 6 * cm, 5 * cm]),
    Spacer(1, 6),
]

# 2. Etapa 1
S += [Paragraph("2. Etapa 1: diagnóstico e modelagem da situação atual", h1)]
S += [Paragraph("a) Variáveis", h2)]
S += [p("Sejam N, S, L e O o número de ônibus alocados nos centros Norte, Sul, Leste e Oeste, respectivamente. As quatro são "
        "variáveis inteiras e não negativas, e o vetor das incógnitas é x = (N, S, L, O).")]

S += [Paragraph("b) Modelo matemático", h2)]
S += [p("Cada registro consolidado do Relatório I vira uma equação linear:")]
traducao = [
    ("A frota disponível para a operação regular é de 72 ônibus", "N + S + L + O = 72"),
    ("Norte + Oeste + o dobro do Sul = 76", "N + 2S + O = 76"),
    ("Sul + o dobro do Leste = 52", "S + 2L = 52"),
    ("Norte + Leste + o dobro do Oeste = 76", "N + L + 2O = 76"),
]
S += [KeepTogether([tabela([["Registro operacional", "Equação"]] + [[a, b] for a, b in traducao], [11 * cm, 5 * cm], centralizar=False)])]
S += [Spacer(1, 6)]

S += [Paragraph("c) Sistema matricial", h2)]
S += [p("O sistema é escrito como A·x = b, com as colunas de A na ordem (N, S, L, O):")]
S += [pre(matriz_texto([[str(v) for v in l] + [str(bb)] for l, bb in zip(E1["A"], E1["b"])], aumentada=True) + "\n\n  Matriz aumentada [A | b]")]

S += [Paragraph("d) Existência e unicidade da solução (Álgebra Linear)", h2)]
S += [
    p("O sistema tem 4 equações e 4 incógnitas. Pelo teorema de Rouché-Capelli, ele é possível e determinado quando "
      "posto(A) = posto([A | b]) = número de incógnitas. Aplicou-se a eliminação de Gauss-Jordan com frações exatas "
      "(sem erro de arredondamento); os passos estão no Apêndice A."),
    tabela([["Grandeza", "Valor"],
            ["posto(A)", E1["posto_A"]],
            ["posto([A | b])", E1["posto_aumentada"]],
            ["número de incógnitas", 4],
            ["det(A) (produto dos pivôs, com o sinal das trocas)", E1["determinante"]],
            ["det(A) calculado por numpy (conferência)", f"{E1['determinante_numpy']:.4f}".replace(".", ",")],
            ["número de condição de A", f"{E1['numero_de_condicao']:.2f}".replace(".", ",")]],
           [10 * cm, 5 * cm]),
    Spacer(1, 6),
    p(f"Como det(A) = {E1['determinante']} ≠ 0, a matriz A é invertível e a solução é única: x = A<super>-1</super>·b. "
      "<b>Conclusão:</b> as informações disponíveis permitem determinar uma única distribuição de veículos. O número de condição baixo "
      "indica que a solução não é sensível a pequenas perturbações nos registros."),
]

S += [Paragraph("e) Resolução em Python", h2)]
S += [p("O arquivo <font name='Courier'>modelo_frota.py</font> implementa a eliminação de Gauss-Jordan e confere o resultado com "
        "<font name='Courier'>numpy.linalg.solve</font>. A distribuição encontrada é:")]
S += [tabela([["Região", "Ônibus (solução exata)", "numpy.linalg.solve"]] +
             [[REG[i], x[i], f"{E1['conferencia_numpy'][i]:.6f}".replace(".", ",")] for i in range(4)], [4 * cm, 6 * cm, 5 * cm]), Spacer(1, 6)]

S += [Paragraph("f) Verificação dos registros operacionais", h2)]
S += [tabela([["Equação", "Lado esquerdo", "Lado direito", "Resultado"]] +
             [[v["equacao"], v["esquerda"], v["direita"], "satisfeita" if v["ok"] else "violada"] for v in E1["verificacao"]],
             [6 * cm, 3.5 * cm, 3.5 * cm, 3 * cm]), Spacer(1, 6)]
S += [p("Todos os registros são satisfeitos e as quantidades são inteiras e não negativas, portanto a distribuição recuperada é válida.")]

# 3. Etapa 2
S += [Paragraph("3. Etapa 2: política de redistribuição", h1)]
S += [Paragraph("a) Necessidade de ônibus por região", h2)]
S += [p("Como cada ônibus comporta 40 passageiros e cada passageiro precisa de uma vaga, a necessidade da região i é "
        "n<sub>i</sub> = teto(passageiros<sub>i</sub> / 40), isto é, o arredondamento para cima, pois não existe fração de ônibus.")]
S += [tabela([["Região", "Passageiros", "Passageiros / 40", "Necessário"]] +
             [[d["regiao"], d["passageiros"], f"{d['passageiros'] / d['capacidade']:.1f}".replace(".", ","), d["necessario"]] for d in D] +
             [["Total", sum(d["passageiros"] for d in D), "", E2["total_necessario"]]], [4 * cm, 4 * cm, 4 * cm, 4 * cm]), Spacer(1, 6)]
S += [p(f"A necessidade total ({E2['total_necessario']}) é igual à frota de 72 ônibus. Logo a frota é suficiente: o problema é de "
        "<b>distribuição</b>, e não de falta de veículos.")]

S += [Paragraph("b) Desequilíbrios", h2)]
S += [tabela([["Região", "Atual", "Necessário", "Saldo", "Ocupação", "Passageiros sem vaga"]] +
             [[D[i]["regiao"], D[i]["atual"], D[i]["necessario"], f"{D[i]['saldo']:+d}", pct(antes["ocupacao"][i]), antes["nao_atendidos"][i]] for i in range(4)] +
             [["Total", sum(d["atual"] for d in D), E2["total_necessario"], "0", "", antes["total_nao_atendidos"]]],
             [3 * cm, 2.4 * cm, 2.8 * cm, 2.4 * cm, 2.8 * cm, 3.6 * cm]), Spacer(1, 6)]
falta = [d["regiao"] for d in D if d["saldo"] < 0]
sobra = [d["regiao"] for d in D if d["saldo"] > 0]
S += [p(f"Saldo = frota atual − necessidade. Faltam ônibus em {' e '.join(falta)} (ocupação acima de 100%) e sobram em {' e '.join(sobra)}. "
        f"No pico, {antes['total_nao_atendidos']} passageiros ficam sem vaga.")]

S += [Paragraph("c) Política proposta e critérios", h2)]
S += [p("A política é desenvolvida pela equipe e obedece às exigências da prefeitura (preservar o total e permitir o compartilhamento entre centros):")]
for item in [
    "<b>Preservar o total:</b> nenhum ônibus é criado ou retirado de operação.",
    "<b>Mover o mínimo:</b> só as regiões com sobra doam e só as regiões com falta recebem. O total movido é a soma das sobras, o menor valor que zera todos os déficits.",
    "<b>Atender primeiro quem está mais sobrecarregado:</b> a região com maior ocupação (Norte) é a primeira a receber.",
    "<b>Doar primeiro de quem tem mais folga:</b> a região com maior sobra (Oeste) doa antes, o que reduz o número de rotas de remanejamento.",
    "<b>Valores inteiros e não negativos</b>, como exige o enunciado.",
]:
    S += [p("• " + item)]
S += [p("Aplicando os critérios, os fluxos de ônibus são: " + "; ".join(f"{f['origem']} → {f['destino']}: {f['onibus']}" for f in E2["fluxos"]) +
        f". Total movimentado: {E2['onibus_movidos']} ônibus ({pct(E2['onibus_movidos'] / 72)} da frota).")]

S += [Paragraph("d) Representação por transformação linear", h2)]
S += [p("Seja T: R<super>4</super> → R<super>4</super> a transformação que leva a distribuição atual x à nova distribuição x': "
        "T(x) = M·x. A matriz M = (m<sub>ij</sub>) tem o seguinte significado: para i ≠ j, m<sub>ij</sub> é a <b>fração dos ônibus da região j "
        "enviada para a região i</b>; a diagonal m<sub>jj</sub> é a <b>fração dos ônibus da região j que permanece onde está</b>.")]
S += [p("T é linear porque é um produto de matriz por vetor: T(αu + βv) = αT(u) + βT(v). Isso foi também conferido numericamente no código "
        f"(resultado: {'verificada' if E2['linearidade_ok'] else 'falhou'}).")]

S += [Paragraph("e) Matriz associada e significado dos coeficientes", h2)]
cab_m = [""] + [f"origem {r}" for r in REG]
S += [tabela([cab_m] + [[f"destino {REG[i]}"] + E2["T"][i] for i in range(4)], [3.3 * cm, 3.1 * cm, 3.1 * cm, 3.1 * cm, 3.1 * cm]), Spacer(1, 6)]
S += [p("Leitura dos coeficientes:")]
idx = {r: i for i, r in enumerate(REG)}
for f in E2["fluxos"]:
    j, i = idx[f["origem"]], idx[f["destino"]]
    S += [p(f"• m<sub>{REG[i][0]}{REG[j][0]}</sub> = {E2['T'][i][j]}: {f['onibus']} de {x[j]} ônibus de {f['origem']} seguem para {f['destino']}.")]
for j in range(4):
    S += [p(f"• m<sub>{REG[j][0]}{REG[j][0]}</sub> = {E2['T'][j][j]}: fração da frota de {REG[j]} que permanece na região.")]

S += [Paragraph("f) Demonstrações", h2)]
S += [p("<b>1) A transformação preserva o total.</b> O total da frota após a política é "
        "Σ<sub>i</sub>(Mx)<sub>i</sub> = Σ<sub>i</sub>Σ<sub>j</sub> m<sub>ij</sub>x<sub>j</sub> = Σ<sub>j</sub> x<sub>j</sub>·(Σ<sub>i</sub> m<sub>ij</sub>). "
        "Cada coluna de M soma 1, pois toda a frota de uma região ou permanece ou é enviada a outra. Logo o total é Σ<sub>j</sub> x<sub>j</sub>, "
        f"o mesmo de antes. Soma das colunas obtida: {', '.join(E2['soma_das_colunas'])}. Total: {E2['total_antes']} → {E2['total_depois']}.")]
S += [p("<b>2) A transformação não produz alocações negativas.</b> Todos os coeficientes são não negativos (menor coeficiente = "
        f"{E2['menor_coeficiente']}) e x<sub>j</sub> ≥ 0. Portanto (Mx)<sub>i</sub> = Σ<sub>j</sub> m<sub>ij</sub>x<sub>j</sub> ≥ 0 para qualquer distribuição x ≥ 0. "
        "As duas propriedades valem para qualquer x e não apenas para a distribuição atual: M é uma matriz estocástica por colunas.")]
S += [p("<b>3) Resultado da política.</b>")]
S += [pre("M · x = M · " + str(tuple(x)) + " = " + str(tuple(E2["novo_vetor"])) + "     necessidade = " + str(tuple(d["necessario"] for d in D)))]
S += [p(f"A nova distribuição coincide com a necessidade em todas as regiões ({'sim' if E2['atinge_necessidade'] else 'não'}). "
        f"Além disso, det(M) = {E2['determinante_T']} ≠ 0, então a transformação é invertível: é possível reverter a política "
        "aplicando M<super>-1</super>.")]

# 4. Resultados
S += [Paragraph("4. Avaliação dos resultados da intervenção", h1)]
S += [tabela([["Região", "Frota antes", "Frota depois", "Ocupação antes", "Ocupação depois", "Sem vaga antes", "Sem vaga depois"]] +
             [[REG[i], antes["onibus"][i], depois["onibus"][i], pct(antes["ocupacao"][i]), pct(depois["ocupacao"][i]), antes["nao_atendidos"][i], depois["nao_atendidos"][i]] for i in range(4)] +
             [["Total", sum(antes["onibus"]), sum(depois["onibus"]), "", "", antes["total_nao_atendidos"], depois["total_nao_atendidos"]]],
             [2.4 * cm, 2.3 * cm, 2.4 * cm, 2.6 * cm, 2.7 * cm, 2.4 * cm, 2.4 * cm]), Spacer(1, 8)]
S += [p(f"A ocupação máxima caiu de {pct(antes['ocupacao_maxima'])} para {pct(depois['ocupacao_maxima'])}, e os {antes['total_nao_atendidos']} passageiros sem vaga "
        f"passaram a {depois['total_nao_atendidos']}, movendo {E2['onibus_movidos']} ônibus.")]
S += [figura("frota_antes_depois.png", "Figura 1. Frota atual, após a redistribuição e necessária por região.")]
S += [figura("ocupacao_antes_depois.png", "Figura 2. Ocupação da capacidade no horário de pico, antes e depois.")]

# 5. Limitações
S += [Paragraph("5. Limitações e conclusão", h1)]
for item in [
    "Os dados são hipotéticos e se referem a um único horário de pico; a demanda real varia por hora, dia e sentido.",
    "O modelo supõe que cada ônibus atende somente a região em que está alocado e ignora tempo e custo de deslocamento entre centros operacionais.",
    "A matriz M foi calibrada para a distribuição atual: os coeficientes dão exatamente a necessidade apenas para esse x. Se a frota ou a demanda mudarem, "
    "M deve ser recalculada (a função <font name='Courier'>construir_transformacao</font> faz isso); as propriedades de preservar o total e não gerar valores negativos continuam valendo.",
    "O arredondamento para cima das necessidades é conservador; uma análise com variação de demanda seria um passo seguinte.",
]:
    S += [p("• " + item)]
S += [p("<b>Conclusão.</b> A frota é suficiente, mas está mal distribuída. Uma redistribuição de apenas "
        f"{E2['onibus_movidos']} ônibus elimina a superlotação de Norte e Leste sem aumentar a frota, e a modelagem por sistema linear e por "
        "transformação linear permite demonstrar matematicamente que a política preserva o total e não gera alocações negativas.")]

S += [Paragraph("6. Como executar", h1)]
S += [pre("pip install -r requirements.txt\npython modelo_frota.py            # imprime as Etapas 1 e 2 e gera resultados/\npython scripts/gerar_relatorio.py  # gera este PDF")]

# Apêndice
S += [Paragraph("Apêndice A. Passos da eliminação de Gauss-Jordan", h1)]
S += [p("Operações sobre a matriz aumentada [A | b], com frações exatas. L<sub>k</sub> é a k-ésima linha.")]
for passo in E1["passos"]:
    m = passo["matriz"]
    S += [KeepTogether([p("<b>" + escape(passo["descricao"]) + "</b>"), pre(matriz_texto(m, aumentada=True))])]
S += [p(f"Ao final, a parte esquerda é a identidade e a coluna direita é a solução (N, S, L, O) = {tuple(x)}.")]

doc = SimpleDocTemplate(str(SAIDA), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
                        title="Modelagem Matemática e Computacional - GS 2026.2", author="João Guilherme Figueiredo e Ryan Luther Roque")
doc.build(S, onFirstPage=rodape, onLaterPages=rodape)
print("PDF gerado:", SAIDA)
