# Pystruct

Programa de dimensionamento de estruturas de concreto armado desenvolvido como TCC:

- **Rampa** e **Escada**: lajes inclinadas armadas em uma direção
- **Viga**: análise de viga contínua (com ou sem balanços) pelo método dos deslocamentos, dimensionamento à flexão de qualquer momento da análise e geração do desenho da seção no AutoCAD (`.scr`)

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

python -m pystruct.app        # app novo (Flet): rampa e escada
python -m pystruct            # versão desktop antiga (tkinter): todas as estruturas
```

O app novo é feito em [Flet](https://flet.dev) e roda no Windows, macOS, Linux, web,
Android e iOS. A viga ainda está sendo migrada; até lá ela só existe na versão tkinter.

## Testes

```bash
pytest
```

## Organização

```
pystruct/
├── calculo/     # back-end: fórmulas puras, sem interface (testáveis)
├── export/      # geração de arquivos (script do AutoCAD, memória de cálculo)
├── app/         # front-end Flet (multiplataforma), substituindo aos poucos o ui/
└── ui/          # front-end Tkinter antigo
tests/           # testes automatizados do back-end e das duas interfaces
```

A interface nunca faz contas: cada janela monta um objeto `Dados...`, chama
`dimensionar()`/`analisar()` do módulo correspondente em `calculo/` e exibe o `Resultado...`.
