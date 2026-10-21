# Plano de melhorias do Pystruct

Acompanhamento da reorganização do projeto. Marque `[x]` quando concluir e anote a data.

Legenda: ✅ concluído · 🔄 em andamento · ⬜ pendente · ❓ precisa de decisão de engenharia

---

## 1. Arquitetura e organização

| Status | Item | Observações |
|---|---|---|
| ✅ | Separar cálculo (back) da interface (front) | `pystruct/calculo` sem nenhum tkinter (2026-10-20) |
| ✅ | Estrutura de pastas `calculo/`, `export/`, `ui/`, `tests/` | 2026-10-20 |
| ✅ | Eliminar as 97 variáveis `global` | Estado vive em objetos `Dados...`/`Resultado...` |
| ✅ | Janelas como classes (`JanelaEstrutura` como base) | |
| ✅ | Componentes reutilizáveis (`Campo`, `Saida`, `Escolha`, `AreaRolavel`) | Substituíram os blocos Label + Text + botão "ok!" |
| ✅ | Um botão "Calcular" por tela no lugar dos vários "ok!" | Aceita vírgula decimal e mostra erro amigável |
| ✅ | Desenho da viga parametrizado (sem coordenadas repetidas) | `ui/desenho_viga.py` |
| ✅ | Viga contínua generalizada para N vãos | `calculo/viga_continua.py` |
| 🔄 | Remover a pasta antiga `TccProjeto/TccProjeto/` (`Tcc.py`, `build/`, `.idea/`, `venv/`) | Fora do git; código original preservado na tag `tcc-original`. Falta apagar do disco |
| ✅ | Primeiro commit limpo no git | Sobre o histórico do GitHub (`Vitorpvss17/Pystruct`), sem force push (2026-10-21) |
| ✅ | Usar o resultado da análise da viga no dimensionamento | Lista de momentos + botão "Dimensionar este momento" preenche Mk (2026-10-21) |
| ✅ | Cálculo de vigas com balanço | Momento do balanço entra como momento conhecido no apoio extremo; conferido com a equação dos três momentos (2026-10-21) |
| ✅ | Unificar Rampa e Escada (ambas são laje inclinada) | `calculo/laje_inclinada.py` e `ui/janela_laje_inclinada.py`; diferenças da seção 5 preservadas (2026-10-21) |
| ⬜ | Trocar a interface tkinter por Flet | Multiplataforma (desktop, web, Android/iOS) reaproveitando `calculo/` em Python |
| ⬜ | Gerar executável/instaladores | Com Flet: `flet build windows/apk/web` |

## 2. Testes e qualidade

| Status | Item | Observações |
|---|---|---|
| ✅ | Testes com pytest para o back-end | Flexão, armadura, rampa, escada, viga (com balanços), AutoCAD |
| ✅ | Validar a viga contínua com casos de tabela e a equação dos três momentos | |
| ✅ | Teste de regressão do script do AutoCAD contra o `Viga.scr` antigo | |
| ⬜ | Validar com exemplos resolvidos do TCC/apostila (rampa, escada, viga) | Comparar números finais |
| ✅ | Testes para os casos de erro da interface | `tests/test_interface.py`: campos inválidos, divisões por zero, fluxo análise → dimensionamento. Total: 45 testes (2026-10-21) |

## 3. Higiene do repositório

| Status | Item | Observações |
|---|---|---|
| ✅ | `.gitignore` (venv, build, .idea, arquivos gerados) | |
| ✅ | `requirements.txt` corrigido | Removidos `future`/`PyAutoGUI`; incluídos `numpy`/`matplotlib` |
| ✅ | `pyproject.toml` e `README.md` | Python mínimo passou para 3.10 (`dataclass(kw_only=True)`) |
| ✅ | Ambiente virtual `.venv` na raiz | O Python global tem conflito numpy 2 × matplotlib antigo |

## 4. Bugs corrigidos (mudam resultados)

| Status | Bug | Onde estava |
|---|---|---|
| ✅ | `cos(α)` recebia graus em vez de radianos | Rampa e escada, altura útil |
| ✅ | Bitola secundária digitada era ignorada (lia a principal) | Rampa e escada |
| ✅ | Espaçamento máximo `2h` comparava com o vão em metros | Rampa e escada |
| ✅ | Campo φl era ignorado (`fil = 1` fixo) | Viga, cálculo de `d` |
| ✅ | Momentos positivos errados com 3 ou mais vãos | Viga contínua |
| ✅ | Reações erradas com 2 vãos diferentes | Viga contínua |
| ✅ | Tudo errado com 4 ou mais vãos diferentes | Viga contínua (matriz de rigidez montada à mão) |
| ✅ | Listas acumulavam ao clicar em "calcular" duas vezes | Viga |
| ✅ | `CIRCLE` sem `_` em parte do script | AutoCAD |
| ✅ | Erro se as duas raízes da linha neutra fossem iguais | Todas |
| ✅ | "-1" destruía o rótulo e o "+1" seguinte dava erro | Viga |

## 5. Pontos para revisão de engenharia ❓

Mantidos como no código original até você decidir:

| Status | Ponto | Arquivo |
|---|---|---|
| ❓ | Parcela extra no Md da rampa: `100·1,4·(H/2)²/H` (= 35·H kN·m/m) | `calculo/rampa.py` |
| ❓ | Peso próprio da escada usa `h1` e não `hm` | `calculo/escada.py` |
| ❓ | Número de barras usa o As calculado mesmo quando As,mín governa | `rampa.py`, `escada.py`, `viga.py` |
| ❓ | As,mín da viga = 0,15·d (fórmula de laje); para viga seria 0,15% de bw·h | `calculo/flexao.py` |
| ❓ | Quando As < As,mín: a rampa diz "não permitida", a escada adota As,mín | `rampa.py` × `escada.py` |
| ❓ | Diâmetro estimado fixo de 1 cm no `d` de rampa e escada | `DIAMETRO_ESTIMADO` |
| ❓ | Unidade de E e I na viga (não altera esforços com seção constante) | `ui/janela_viga.py` |

---

## Histórico

- **2026-10-20**: Separação front/back, nova estrutura de pastas, solver de viga contínua generalizado, testes, correção dos bugs da seção 4.
- **2026-10-21**: Primeiro commit da reorganização no GitHub; decisão de migrar a interface para Flet.
- **2026-10-21**: Rampa e escada unificadas como laje inclinada, viga com balanços, momento da análise enviado ao dimensionamento, testes da interface.
