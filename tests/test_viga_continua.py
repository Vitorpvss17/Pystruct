import numpy as np
import pytest

from pystruct.calculo import viga_continua

E, I = 30e6, 26785


def test_um_vao_biapoiado():
    res = viga_continua.analisar([10], [4], E, I)
    assert res.momentos_apoio == [0.0, 0.0]
    assert res.reacoes == pytest.approx([20, 20])
    assert res.momentos_positivos[0] == pytest.approx(10 * 4 ** 2 / 8)
    assert res.posicoes_maximo[0] == pytest.approx(2)


def test_dois_vaos_iguais():
    q, L = 10, 4
    res = viga_continua.analisar([q, q], [L, L], E, I)
    assert res.momentos_apoio[1] == pytest.approx(-q * L ** 2 / 8)
    assert res.reacoes == pytest.approx([3 * q * L / 8, 10 * q * L / 8, 3 * q * L / 8])
    assert res.momentos_positivos == pytest.approx([9 * q * L ** 2 / 128] * 2)


def test_dois_vaos_diferentes_equacao_dos_tres_momentos():
    # 2·M·(L1 + L2) = −(q1·L1³ + q2·L2³) / 4
    res = viga_continua.analisar([10, 20], [4, 6], E, I)
    assert res.momentos_apoio[1] == pytest.approx(-62)
    assert res.reacoes[0] == pytest.approx(4.5)


def test_tres_vaos_igual_ao_programa_original():
    # valores do bloco_notas.txt gerado pela versão original
    res = viga_continua.analisar([1, 2, 3], [4, 5, 6], E, I)
    assert res.momentos_apoio[1:3] == pytest.approx([-1.62938, -9.83423], rel=1e-5)
    assert res.reacoes == pytest.approx([1.59265, 5.76637, 17.28001, 7.36096], rel=1e-5)


def test_quatro_vaos_iguais_coeficientes_de_tabela():
    q, L = 10, 4
    res = viga_continua.analisar([q] * 4, [L] * 4, E, I)
    ql2 = q * L ** 2
    assert res.momentos_apoio[1:4] == pytest.approx([-0.10714 * ql2, -0.07143 * ql2, -0.10714 * ql2], rel=1e-3)
    # simetria
    assert res.momentos_positivos[0] == pytest.approx(res.momentos_positivos[3])
    assert res.momentos_positivos[1] == pytest.approx(res.momentos_positivos[2])
    assert res.momentos_positivos[0] == pytest.approx(0.0772 * ql2, rel=1e-3)
    assert res.momentos_positivos[1] == pytest.approx(0.0364 * ql2, rel=1e-2)


@pytest.mark.parametrize("q, L", [
    ([10, 10, 10, 10], [4, 5, 6, 7]),
    ([5, 12, 8, 3, 9], [3, 6, 4.5, 5, 2]),
])
def test_equilibrio_e_continuidade(q, L):
    res = viga_continua.analisar(q, L, E, I)
    assert sum(res.reacoes) == pytest.approx(sum(qi * Li for qi, Li in zip(q, L)))
    # o diagrama é contínuo nos apoios
    for k in range(len(L) - 1):
        assert res.momento_em(k, L[k]) == pytest.approx(res.momentos_apoio[k + 1])


def test_entradas_invalidas():
    with pytest.raises(ValueError):
        viga_continua.analisar([], [], E, I)
    with pytest.raises(ValueError):
        viga_continua.analisar([10], [0], E, I)
    with pytest.raises(ValueError):
        viga_continua.analisar([10, 10], [4], E, I)


def tres_momentos(q, L, m0, mn):
    """Momentos nos apoios internos pela equação dos três momentos, com extremos conhecidos."""
    n = len(L)
    A = np.zeros((n - 1, n - 1))
    b = np.zeros(n - 1)
    for i in range(1, n):
        A[i - 1, i - 1] = 2 * (L[i - 1] + L[i])
        if i > 1:
            A[i - 1, i - 2] = L[i - 1]
        if i < n - 1:
            A[i - 1, i] = L[i]
        b[i - 1] = -(q[i - 1] * L[i - 1] ** 3 + q[i] * L[i] ** 3) / 4
    b[0] -= m0 * L[0]
    b[-1] -= mn * L[-1]
    return [m0, *np.linalg.solve(A, b), mn]


def test_um_vao_com_balanco_esquerdo():
    res = viga_continua.analisar([10], [6], E, I, balanco_esq=viga_continua.Balanco(10, 2))
    assert res.momentos_apoio == pytest.approx([-20, 0])
    # momentos em relação ao apoio direito: R0·6 = 20·7 + 60·3
    assert res.reacoes == pytest.approx([320 / 6, 80 - 320 / 6])


def test_um_vao_com_dois_balancos_iguais():
    q, L, a = 10, 6, 1.5
    bal = viga_continua.Balanco(q, a)
    res = viga_continua.analisar([q], [L], E, I, balanco_esq=bal, balanco_dir=bal)
    assert res.momentos_apoio == pytest.approx([-q * a ** 2 / 2] * 2)
    assert res.momentos_positivos[0] == pytest.approx(q * L ** 2 / 8 - q * a ** 2 / 2)
    assert res.reacoes == pytest.approx([q * (L / 2 + a)] * 2)


@pytest.mark.parametrize("q, L, esq, dir_", [
    ([10, 20], [4, 6], (10, 2), None),
    ([10, 20], [4, 6], None, (15, 1.5)),
    ([5, 12, 8, 3], [3, 6, 4.5, 5], (8, 1.2), (6, 2)),
])
def test_balancos_conferem_com_tres_momentos(q, L, esq, dir_):
    bal_esq = viga_continua.Balanco(*esq) if esq else None
    bal_dir = viga_continua.Balanco(*dir_) if dir_ else None
    res = viga_continua.analisar(q, L, E, I, balanco_esq=bal_esq, balanco_dir=bal_dir)

    m0 = bal_esq.momento_apoio if bal_esq else 0.0
    mn = bal_dir.momento_apoio if bal_dir else 0.0
    assert res.momentos_apoio == pytest.approx(tres_momentos(q, L, m0, mn))

    carga_total = sum(qi * Li for qi, Li in zip(q, L))
    carga_total += sum(b.q * b.L for b in (bal_esq, bal_dir) if b)
    assert sum(res.reacoes) == pytest.approx(carga_total)

    # o diagrama é contínuo, inclusive na junção com os balanços
    xs, ms = res.diagrama()
    for x_apoio, m_apoio in zip(res.posicoes_apoios, res.momentos_apoio):
        assert ms[np.isclose(xs, x_apoio)] == pytest.approx(m_apoio)


def test_balanco_sem_comprimento():
    with pytest.raises(ValueError):
        viga_continua.analisar([10], [4], E, I, balanco_esq=viga_continua.Balanco(10, 0))
