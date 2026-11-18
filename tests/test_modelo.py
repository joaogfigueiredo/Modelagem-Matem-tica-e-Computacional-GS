import random
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import modelo_frota as mf


class TestEtapa1(unittest.TestCase):
    def setUp(self):
        self.e1 = mf.etapa1()

    def test_solucao_unica_e_valores(self):
        self.assertTrue(self.e1["solucao_unica"])
        self.assertEqual(self.e1["x"], [12, 20, 16, 24])

    def test_determinante_e_postos(self):
        self.assertEqual(self.e1["determinante"], "3")
        self.assertEqual((self.e1["posto_A"], self.e1["posto_aumentada"]), (4, 4))

    def test_todos_os_registros_satisfeitos(self):
        self.assertTrue(self.e1["todas_equacoes_ok"])


class TestEtapa2(unittest.TestCase):
    def setUp(self):
        self.x = [12, 20, 16, 24]
        self.e2 = mf.etapa2(self.x)

    def test_necessidade_e_resultado(self):
        self.assertEqual([d["necessario"] for d in self.e2["demanda"]], [14, 19, 18, 21])
        self.assertEqual(self.e2["novo_vetor"], [14, 19, 18, 21])
        self.assertTrue(self.e2["atinge_necessidade"])

    def test_total_e_negativos(self):
        self.assertTrue(self.e2["total_preservado"])
        self.assertTrue(self.e2["sem_alocacao_negativa"])
        self.assertEqual(self.e2["onibus_movidos"], 4)

    def test_nao_atendidos(self):
        self.assertEqual(self.e2["antes"]["total_nao_atendidos"], 160)
        self.assertEqual(self.e2["depois"]["total_nao_atendidos"], 0)

    def test_propriedades_valem_para_qualquer_distribuicao(self):
        T, _, _ = mf.construir_transformacao(self.x, [14, 19, 18, 21])
        rnd = random.Random(7)
        for _ in range(200):
            v = [rnd.randint(0, 60) for _ in range(4)]
            w = mf.aplicar(T, v)
            self.assertEqual(sum(w), sum(v))
            self.assertTrue(all(c >= 0 for c in w))

    def test_colunas_somam_um(self):
        T, _, _ = mf.construir_transformacao(self.x, [14, 19, 18, 21])
        for j in range(4):
            self.assertEqual(sum(T[i][j] for i in range(4)), Fraction(1))


if __name__ == "__main__":
    unittest.main()
