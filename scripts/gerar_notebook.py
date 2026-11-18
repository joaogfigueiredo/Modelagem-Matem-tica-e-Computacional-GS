"""Gera e executa modelo_frota.ipynb (mesmo modelo de modelo_frota.py, em formato de notebook)."""
from pathlib import Path

import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

RAIZ = Path(__file__).resolve().parent.parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

celulas = [
    md("# Mobilidade Urbana Inteligente: modelagem matemática da frota\n\n"
       "**Modelagem Matemática e Computacional · Global Solution 2026.2 (CitizenTech)**  \n"
       "João Guilherme Figueiredo (RM 572697) · Ryan Luther Roque (RM 572993)\n\n"
       "Os dados do enunciado são hipotéticos. Variáveis: N, S, L e O são os ônibus nos centros Norte, Sul, Leste e Oeste."),
    code("import pandas as pd\n"
         "from IPython.display import Image, display\n"
         "import modelo_frota as mf\n\n"
         "res = mf.executar()\n"
         "e1, e2 = res['etapa1'], res['etapa2']"),
    md("## Etapa 1: diagnóstico da situação atual\n\n### b) e c) Modelo e sistema matricial A·x = b"),
    code("for eq in e1['equacoes']:\n    print(eq['texto'])\n"
         "print()\n"
         "print('A =')\n"
         "display(pd.DataFrame(e1['A'], columns=['N', 'S', 'L', 'O']))\n"
         "print('b =', e1['b'])"),
    md("### d) Unicidade da solução: Gauss-Jordan com frações exatas, posto e determinante"),
    code("for passo in e1['passos']:\n"
         "    print(passo['descricao'])\n"
         "    for linha in passo['matriz']:\n"
         "        print('   ', linha)\n"
         "    print()"),
    code("print('posto(A)        =', e1['posto_A'])\n"
         "print('posto([A | b])  =', e1['posto_aumentada'])\n"
         "print('det(A)          =', e1['determinante'], '(numpy:', round(e1['determinante_numpy'], 4), ')')\n"
         "print('solução única   =', e1['solucao_unica'])"),
    md("### e) e f) Distribuição encontrada e verificação dos registros"),
    code("print('Distribuição atual:', e1['distribuicao_atual'])\n"
         "display(pd.DataFrame(e1['verificacao']))"),
    md("## Etapa 2: política de redistribuição\n\n### a) e b) Necessidade e desequilíbrios\n\n"
       "Necessidade da região i: n_i = teto(passageiros_i / 40)."),
    code("display(pd.DataFrame(e2['demanda']))\n"
         "print('Total necessário:', e2['total_necessario'], '| frota suficiente:', e2['frota_suficiente'])\n"
         "print('Ocupação antes:', [round(o, 3) for o in e2['antes']['ocupacao']])\n"
         "print('Passageiros sem vaga antes:', e2['antes']['nao_atendidos'])"),
    md("### c) Política: fluxos entre regiões\n\n"
       "Quem tem mais sobra doa primeiro; quem está mais lotado recebe primeiro; só doam as regiões com sobra e só recebem as com falta."),
    code("display(pd.DataFrame(e2['fluxos']))\nprint('Ônibus movidos:', e2['onibus_movidos'])"),
    md("### d) e e) Transformação linear T(x) = M·x e a matriz M\n\n"
       "m_ij (i ≠ j) é a fração da frota da região j enviada à região i; m_jj é a fração que permanece."),
    code("regs = ['Norte', 'Sul', 'Leste', 'Oeste']\n"
         "M = pd.DataFrame(e2['T'], index=['destino ' + r for r in regs], columns=['origem ' + r for r in regs])\n"
         "display(M)"),
    md("### f) Demonstrações: total preservado e nenhuma alocação negativa\n\n"
       "Cada coluna de M soma 1 (toda a frota de uma região fica ou é enviada) e todos os coeficientes são não negativos. "
       "Logo Σ(Mx)_i = Σ x_j e (Mx)_i ≥ 0 para qualquer x ≥ 0."),
    code("print('Soma de cada coluna de M :', e2['soma_das_colunas'])\n"
         "print('Menor coeficiente de M  :', e2['menor_coeficiente'])\n"
         "print('M·x                     :', e2['novo_vetor'], '(necessidade:', [d['necessario'] for d in e2['demanda']], ')')\n"
         "print('Total antes -> depois   :', e2['total_antes'], '->', e2['total_depois'])\n"
         "print('Total preservado        :', e2['total_preservado'])\n"
         "print('Sem alocação negativa   :', e2['sem_alocacao_negativa'])\n"
         "print('Atinge a necessidade    :', e2['atinge_necessidade'])\n"
         "print('det(M)                  :', e2['determinante_T'])\n"
         "print('Linearidade verificada  :', e2['linearidade_ok'])"),
    md("## Resultado da intervenção"),
    code("print('Passageiros sem vaga:', e2['antes']['total_nao_atendidos'], '->', e2['depois']['total_nao_atendidos'])\n"
         "print('Ocupação máxima:', round(e2['antes']['ocupacao_maxima'], 3), '->', round(e2['depois']['ocupacao_maxima'], 3))\n"
         "display(Image('resultados/frota_antes_depois.png'))\n"
         "display(Image('resultados/ocupacao_antes_depois.png'))"),
    md("**Conclusão.** A frota (72) é suficiente para a demanda do pico (72), mas está mal distribuída. "
       "Mover 4 ônibus elimina a superlotação de Norte e Leste e a transformação proposta preserva o total e não gera valores negativos. "
       "Limitações: dados hipotéticos, um único horário e M calibrada para a distribuição atual."),
]

nb = nbf.v4.new_notebook(cells=celulas)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
ExecutePreprocessor(timeout=300, kernel_name="python3").preprocess(nb, {"metadata": {"path": str(RAIZ)}})
nbf.write(nb, RAIZ / "modelo_frota.ipynb")
print("Notebook executado e salvo em", RAIZ / "modelo_frota.ipynb")
