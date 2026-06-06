# Guia de publicacao no GitHub

Este guia mostra como publicar o projeto `football-market-value-growth-analysis` no GitHub.

## 1. Abrir a pasta no VS Code

Abra esta pasta no VS Code:

```text
football-market-value-growth-analysis
```

Confira se a estrutura esta assim:

```text
README.md
requirements.txt
.gitignore
data/
docs/
notebooks/
outputs/
src/
```

## 2. Baixar ou posicionar os dados

Baixe o dataset no Kaggle:

```text
https://www.kaggle.com/datasets/davidcariboo/player-scores
```

Coloque estes arquivos em `data/raw/`:

```text
player_valuations.csv
players.csv
```

Os CSVs brutos estao ignorados pelo Git por padrao, porque podem ser grandes e dependem da licenca do dataset.

## 3. Testar o projeto localmente

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
.venv\Scripts\activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute o script:

```bash
python src/market_value_analysis.py
```

Se tudo funcionar, o projeto deve gerar:

```text
outputs/figures/club_value_analysis.png
outputs/tables/club_value_analysis.csv
outputs/tables/top_10_clubs_value_created.csv
```

## 4. Criar o repositorio no GitHub

No GitHub:

1. Clique em `New repository`.
2. Use o nome `football-market-value-growth-analysis`.
3. Adicione uma descricao curta:

```text
Exploratory data analysis of football clubs' player market value creation between 2013 and 2023.
```

4. Deixe como publico, se for para portfolio.
5. Nao marque para criar README, `.gitignore` ou license, pois estes arquivos ja existem localmente.

## 5. Inicializar o Git localmente

No terminal, dentro da pasta do projeto:

```bash
git init
git status
git add .
git commit -m "Initial football market value analysis project"
git branch -M main
```

## 6. Conectar com o GitHub

Substitua `SEU-USUARIO` pelo seu usuario do GitHub:

```bash
git remote add origin https://github.com/SEU-USUARIO/football-market-value-growth-analysis.git
git push -u origin main
```

## 7. Ajustes finais no GitHub

No repositorio publicado:

- Adicione uma descricao curta.
- Adicione topicos:
  - `python`
  - `data-analysis`
  - `football`
  - `pandas`
  - `seaborn`
  - `matplotlib`
  - `kaggle`
  - `transfermarkt`
- Fixe o repositorio no seu perfil.

## 8. Texto curto para LinkedIn

Sugestao:

```text
Publiquei um projeto de analise exploratoria de dados sobre criacao de valor de mercado em clubes de futebol entre 2013 e 2023.

Utilizei Python, pandas, numpy, seaborn e matplotlib para analisar dados publicos do Kaggle/Transfermarkt, calculando quais clubes mais aumentaram o valor de mercado dos jogadores durante seus periodos associados aos clubes.

Entre os principais resultados, Ajax Amsterdam, Red Bull Salzburg, RB Leipzig, Sporting CP e SL Benfica aparecem entre os maiores criadores de valor no periodo analisado.

O projeto inclui limpeza de dados, criacao de metricas, agregacao por clube, visualizacao e uma discussao sobre limitacoes metodologicas.
```

