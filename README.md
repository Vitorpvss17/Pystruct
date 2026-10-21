# Pystruct

Programa de dimensionamento de estruturas de concreto armado desenvolvido como TCC:

- **Rampa** e **Escada**: lajes inclinadas armadas em uma direção
- **Viga**: análise de viga contínua (com ou sem balanços) pelo método dos deslocamentos, dimensionamento à flexão de qualquer momento da análise e geração do desenho da seção no AutoCAD (`.scr`)

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python -m pystruct
```

## Testes

```bash
pytest
```

## Organização

```
pystruct/
├── calculo/     # back-end: fórmulas puras, sem interface (testáveis)
├── export/      # geração de arquivos (script do AutoCAD, memória de cálculo)
└── ui/          # front-end Tkinter: lê os campos, chama o back-end e mostra resultados
tests/           # testes automatizados do back-end e da interface
```

A interface nunca faz contas: cada janela monta um objeto `Dados...`, chama
`dimensionar()`/`analisar()` do módulo correspondente em `calculo/` e exibe o `Resultado...`.
