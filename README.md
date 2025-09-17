# Laboratório 02 - Um estudo das características de qualidade de sistema java

## 1. Informações do grupo
- **Curso:** Engenharia de Software
- **Disciplina:** Laboratório de Experimentação de Software
- **Período:** 6° Período
- **Professor(a):** Prof. Wesley Dias Maciel
- **Membros do Grupo:** [[Ana Julia Teixeira Candido](https://github.com/anajuliateixeiracandido) e [Marcella Ferreira Chaves Costa](https://github.com/marcellafccosta)]

---

## 2. Introdução
O desenvolvimento de sistemas de software open-source envolve a colaboração de múltiplos desenvolvedores, que contribuem com diferentes partes do código ao longo do tempo. Essa abordagem colaborativa, apesar de trazer benefícios como inovação rápida e acessibilidade, também apresenta desafios em relação à manutenção de atributos de qualidade do software, como **modularidade, legibilidade e manutenibilidade**.

Este laboratório tem como objetivo realizar uma análise detalhada das características de qualidade de repositórios de código open-source escritos na linguagem Java. A partir da coleta e análise de métricas de produto obtidas por meio da ferramenta CK, busca-se correlacionar essas métricas com características do processo de desenvolvimento dos repositórios, como popularidade, tamanho, atividade e maturidade. O estudo busca responder a quatro questões de pesquisa:

- RQ01. Qual a relação entre a popularidade dos repositórios e suas características de qualidade? 

- RQ02. Qual a relação entre a maturidade dos repositórios e suas características de qualidade? 

- RQ03. Qual a relação entre a atividade dos repositórios e suas características de qualidade? 

- RQ04. Qual a relação entre o tamanho dos repositórios e suas características de qualidade?

**Hipóteses Informais - Informal Hypotheses (IH):**

- **IH01:** Repositórios mais populares tendem a apresentar melhor qualidade de código, pois recebem mais contribuições, revisões e atenção da comunidade.

- **IH02:** Repositórios mais maduros (ou seja, com maior idade) tendem a apresentar uma qualidade de código superior, como menor acoplamento entre objetos (CBO) e menor profundidade de herança (DIT), devido ao tempo de desenvolvimento e refinamento constante do código.

- **IH03:** Repositórios mais ativos tendem a ter pior qualidade inicial, mas melhor organização ao longo do tempo devido ao desenvolvimento contínuo e refatorações.
  
- **IH04:** Repositórios maiores, com mais linhas de código (LOC) e mais linhas de comentários, tendem a apresentar piores características de qualidade de código, como maior acoplamento entre objetos (CBO), maior profundidade de herança (DIT) e menor coesão de métodos (LCOM), devido à maior complexidade e dificuldade de manutenção associada a sistemas maiores.

**Hipóteses Formais - Formal Hypotheses (FH):**
#### **RQ01 - Popularidade vs Qualidade:**
- **H0₁:** Não há diferença significativa nas métricas de qualidade entre repositórios de diferentes níveis de popularidade.
- **H1₁:** Há diferença significativa nas métricas de qualidade entre repositórios de diferentes níveis de popularidade.

#### **RQ02 - Maturidade vs Qualidade:**
- **H0₂:** Não existe correlação significativa entre a maturidade dos repositórios (idade em anos) e suas métricas de qualidade de código (CBO, DIT, WMC, LCOM).
- **H1₂:** Existe correlação significativa entre a maturidade dos repositórios e suas métricas de qualidade de código.

#### **RQ03 - Atividade vs Qualidade:**
- **H0₃:** Não há diferença significativa nas métricas de qualidade entre repositórios de diferentes níveis de atividade.
- **H1₃:** Há diferença significativa nas métricas de qualidade entre repositórios de diferentes níveis de atividade.

#### **RQ04 - Tamanho vs Qualidade:**
- **H0₄:** Não existe correlação significativa entre o tamanho dos repositórios (LOC, número de classes) e suas métricas de qualidade de código (CBO, DIT, WMC, LCOM).
- **H1₄:** Existe correlação significativa entre o tamanho dos repositórios e suas métricas de qualidade de código.


---

## 3. Tecnologias e ferramentas utilizadas
- **Linguagem de Programação:** Python
- **Frameworks/Bibliotecas:** [Ex.: Pandas, Matplotlib, Seaborn, CK]
- **APIs utilizadas:** GitHub REST API
- **Dependências:** requests, csv, time, os, subprocess, shutil, math, threading, json, platform, datetime, pathlib, concurrent.futures, re

---

## 4. Metodologia

### 4.1 Coleta de Dados

Para responder às questões de pesquisa propostas, desenvolvemos um **script em Python** para coletar dados de repositórios de código open-source escritos na linguagem Java. O objetivo foi obter os **1.000 repositórios Java mais populares** do GitHub, utilizando a API REST do GitHub para extração de metadados dos projetos.

### 4.2 Métricas de Processo

Para cada repositório coletado, extraímos as seguintes métricas de processo de desenvolvimento:

- **Popularidade:** Número de estrelas do repositório
- **Maturidade:** Idade do repositório (em anos) 
- **Atividade:** Número de releases publicados
- **Tamanho:** Linhas de código (LOC) e linhas de comentários

### 4.3 Métricas de Qualidade

As métricas de qualidade interna foram calculadas utilizando a ferramenta **CK (Chidamber and Kemerer)**, que realiza análise estática do código Java. As métricas analisadas foram:

- **CBO:** Coupling Between Objects
- **DIT:** Depth Inheritance Tree  
- **LCOM:** Lack of Cohesion of Methods

### 4.4 Análise dos Dados

Desenvolvemos **scripts Python adicionais** utilizando as bibliotecas **pandas** e **numpy** para análise estatística dos dados coletados. A análise seguiu as seguintes etapas:

1. **Agrupamento dos repositórios:** Dividimos os repositórios em faixas baseadas nas métricas de processo:
- **RQ1:** Optamos por faixas logarítmicas em vez de tercis devido à **distribuição exponencial**. Esta abordagem evita agrupar repositórios de 40.000 estrelas com outros de 150.000 estrelas, que representam diferentes níveis de impacto na comunidade. Os limites foram definidos baseados em estudos prévios sobre popularidade em repositórios open-source e na distribuição natural dos nossos dados.
- **RQ3:** Separamos explicitamente repositórios **inativos** (0 releases). As demais faixas foram definidas considerando práticas comuns de versionamento em projetos Java, onde releases frequentes (>50) indicam alta atividade de desenvolvimento, enquanto 1-10 releases sugerem projetos em estágio inicial ou com baixa cadência de atualizações.

2. **Análise estatística:** Para cada grupo, calculamos média, mediana e desvio padrão das métricas de qualidade (CBO, DIT, LCOM).

3. **Teste de hipóteses:** Comparamos os valores obtidos entre os diferentes grupos para identificar padrões e responder às questões de pesquisa.

### 4.5 Limitações Metodológicas

É importante destacar que todos os repositórios analisados possuem mais de 3.400 estrelas, representando apenas os projetos mais populares do GitHub. Esta limitação da amostra deve ser considerada na interpretação dos resultados, pois não representa o ecossistema completo de repositórios Java.

---

## 5. Questões de pesquisa

Liste as questões de pesquisa que guiaram o estudo, com suas métricas associadas:

**Questões de Pesquisa - Research Questions (RQs):**

| RQ   | Pergunta | Métrica utilizada | Código da Métrica |
|------|----------|-----------------|-----------------|
| RQ01 | Qual a relação entre a popularidade dos repositórios e as suas características de qualidade? | Estrelas (agrupadas em: Populares, Muito populares, Extremamente populares), CBO, DIT, LCOM | LM01 |
| RQ02 | Qual a relação entre a maturidade do repositórios e as suas características de qualidade? | Idade (em anos) de cada repositório coletado, CBO e DIT | LM02 |
| RQ03 | Qual a relação entre a atividade dos repositórios e as suas características de qualidade? | Número de releases (agrupados em: Inativos, Baixa atividade, Média atividade, Alta atividade), CBO, DIT, LCOM | LM03 |
| RQ04 | Qual a relação entre o tamanho dos repositórios e as suas características de qualidade? | Linhas de código (LOC) e linhas de comentários, CBO, DIT e LCOM | LM04 |

---

## 6. Resultados

Apresente os resultados obtidos, com tabelas e gráficos sempre que possível.

---

### 6.1 Métricas

Inclua métricas relevantes de repositórios do GitHub, separando **métricas do laboratório** e **métricas adicionais trazidas pelo grupo**:

#### Métricas de Laboratório - Lab Metrics (LM)
| Código | Métrica | Descrição |
|--------|--------|-----------|
| LM01 | Número de estrelas	 | Total de estrelas atribuídas ao repositório, indicando sua popularidade entre os usuários |
| LM02 | Idade (em anos) de cada repositório coletado | Número de anos desde a criação do repositório, refletindo sua maturidade no tempo. |
| LM03 | Número de Releases | Total de versões ou releases oficiais publicadas no repositório. |
| LM04 | Linhas de código (LOC) e linhas de comentários | Total de linhas de código e linhas de comentários no repositório, indicando o tamanho e a qualidade da documentação do código. |
| LM05 | Linhas de comentários | Total de linhas de comentários no repositório, indicando o tamanho e a qualidade da documentação do código. |
| LM06 | CBO: Coupling between objects	 | Total de dependências que uma classe possui com outras classes, indicando o grau de acoplamento entre objetos |
| LM07 | DIT: Depth Inheritance Tree	 |Profundidade de uma classe na hierarquia de herança, refletindo a complexidade da reutilização de código|
| LM08 | LCOM: Lack of Cohesion of Methods	 | Grau de coesão entre os métodos de uma classe, indicando se a classe realiza funções relacionadas ou múltiplas responsabilidades |
---

### 6.2 Sugestões de gráficos

Para criar visualizações das métricas, recomenda-se utilizar como referência o projeto **Seaborn Samples**:  
- Repositório: [Projeto Seaborn Samples](https://github.com/joaopauloaramuni/laboratorio-de-experimentacao-de-software/tree/main/PROJETOS/Projeto%20Seaborn%20Samples)

- Histograma: `grafico_histograma.png` → distribuição de idade, PRs aceitas ou estrelas.  
- Boxplot: `grafico_boxplot.png` → dispersão de métricas como forks, issues fechadas ou LOC.  
- Gráfico de Barras: `grafico_barras.png` → comparação de métricas entre linguagens.  
- Gráfico de Pizza: `grafico_pizza.png` → percentual de repositórios por linguagem.  
- Gráfico de Linha: `grafico_linha.png` → evolução de releases ou PRs ao longo do tempo.  
- Scatterplot / Dispersão: `grafico_dispersao.png` → relação entre estrelas e forks.  
- Heatmap: `grafico_heatmap.png` → correlação entre métricas (idade, PRs, stars, forks, issues).  
- Pairplot: `grafico_pairplot.png` → análise de múltiplas métricas simultaneamente.  
- Violin Plot: `grafico_violin.png` → distribuição detalhada de métricas por subgrupo.  
- Barras Empilhadas: `grafico_barras_empilhadas.png` → comparação de categorias dentro de métricas.

> Dica: combine tabelas e gráficos para facilitar a interpretação e evidenciar padrões nos dados.

### 6.3 Estatísticas Descritivas

Apresente as estatísticas descritivas das métricas analisadas, permitindo uma compreensão mais detalhada da distribuição dos dados.

| Métrica | Código | Média | Mediana | Moda | Desvio Padrão | Mínimo | Máximo | 
|---------|--------|------|--------|-----|---------------|--------|--------|
| Idade do Repositório (anos) | LM01 | 9,652557673 | 9,7 | 8,76 | 3,056436355 | 0,17 | 16,92 |
| Número de estrelas	 | LM02 | 9620,285858 | 5773 | 3813 | 3,056436355| 3414 | 151757 |
| Número de Releases | LM03 | 41,30391174 | 10 | 0 | 3,056436355 | 0 | 2215 |
| Linhas de código (LOC) | LM04 | 79452,63892 | 13368| 0 | 3,056436355 | 0 | 2006814 |
| Linhas de comentários | LM05 | 52011,68706|4743 | 0 | 3,056436355 | 0 | 12462921|
| CBO: Coupling between objects	| LM06 | 5,352302905|5,315 |  0|1,873299378| 0 |21,93 |
| DIT: Depth Inheritance Tree	 | LM07 | 1,460259336| 1,39| 1 |0,3690244713| 1 | 5,71|
| LCOM: Lack of Cohesion of Methods	 | LM08 |118,7377801 | 23,75| 0 | 1785,655144 |0  | 55203,28|

> Dica: Inclua gráficos como histogramas ou boxplots junto com essas estatísticas para facilitar a interpretação.

### 6.4 Análises
### 6.4.1 RQ01 — Popularidade x Qualidade

| Popularidade            | CBO (mean) | CBO (median) | CBO (std) | DIT (mean) | DIT (median) | DIT (std) | LCOM (mean) | LCOM (median) | LCOM (std) |
|-------------------------|------------|--------------|-----------|------------|--------------|-----------|-------------|---------------|------------|
| Populares               | 5.40       | 5.29         | 1.80      | 1.47       | 1.40         | 0.35      | 54.52       | 23.33         | 138.43     |
| Muito populares         | 5.33       | 5.44         | 2.01      | 1.45       | 1.38         | 0.44      | 343.80      | 26.95         | 3796.68    |
| Extremamente populares  | 3.03       | 2.72         | 2.44      | 1.19       | 1.12         | 0.25      | 102.71      | 6.34          | 317.80     |

**Análise**  
- **CBO:** diminui significativamente nos repositórios extremamente populares (5.40 → 3.03), indicando menor acoplamento.  
- **DIT:** também reduz nos mais populares (1.47 → 1.19), sugerindo hierarquias mais simples.  
- **LCOM:** comportamento não-linear, com pico nos “muito populares”, mas queda nos “extremamente populares”.  

**Conclusão**  
- Rejeita-se **H₀** para **CBO** e **DIT**.  
- Repositórios extremamente populares apresentam **melhor qualidade estrutural** (menor acoplamento e hierarquias menos profundas).  
- **Hipótese parcialmente confirmada:** popularidade extrema está associada a melhor qualidade.  
- **Insight:** há um “ponto ótimo” de popularidade em que a qualidade estrutural é maximizada.  

#### 6.4.2 RQ02 (Maturidade x Qualidade)

### 6.4.3 RQ03 — Atividade x Qualidade

| Atividade        | CBO (mean) | CBO (median) | CBO (std) | DIT (mean) | DIT (median) | DIT (std) | LCOM (mean) | LCOM (median) | LCOM (std) |
|------------------|------------|--------------|-----------|------------|--------------|-----------|-------------|---------------|------------|
| Inativos         | 4.52       | 4.62         | 1.81      | 1.38       | 1.31         | 0.36      | 218.96      | 12.06         | 3134.82    |
| Baixa atividade  | 5.15       | 5.02         | 1.82      | 1.47       | 1.38         | 0.36      | 66.95       | 22.66         | 209.92     |
| Média atividade  | 5.63       | 5.57         | 1.41      | 1.50       | 1.42         | 0.41      | 69.10       | 29.32         | 234.53     |
| Alta atividade   | 6.41       | 6.33         | 1.95      | 1.52       | 1.48         | 0.31      | 77.69       | 36.11         | 182.08     |

**Análise**  
- **CBO:** aumenta consistentemente com a atividade (4.52 → 6.41), indicando maior acoplamento em projetos mais ativos.  
- **DIT:** crescimento moderado (1.38 → 1.52), sugerindo hierarquias ligeiramente mais complexas.  
- **LCOM:** comportamento interessante — alto em projetos inativos (218.96), reduz nos com atividade moderada, e cresce de forma gradual nos mais ativos.  

**Conclusão**  
- Rejeita-se **H₀** para todas as métricas.  
- Repositórios mais ativos apresentam **maior complexidade estrutural**, mas **melhor coesão** em comparação com os abandonados.  
- **Hipótese confirmada:** atividade contínua aumenta a complexidade, mas evita degradação da coesão.  
- **Insight:** projetos abandonados tendem a deteriorar em coesão, enquanto a manutenção contínua, mesmo com maior acoplamento, preserva a qualidade estrutural.  


#### 6.4.4 RQ04 (Tamanho x Qualidade)

---

## 7. Discussão

### 7.1 RQ01 - Popularidade vs Qualidade

#### 7.1.1 Confirmação ou refutação das hipóteses
Nossa hipótese informal de que "repositórios mais populares tendem a apresentar melhor qualidade devido a mais contribuições e revisões" foi **parcialmente confirmada**, mas com nuances importantes. Os repositórios extremamente populares (>50.000 estrelas) apresentaram significativa melhoria na qualidade estrutural, com CBO reduzindo de 5.40 para 3.03 e DIT de 1.47 para 1.19. Isso confirma que projetos de grande visibilidade tendem a ter arquiteturas mais desacopladas e hierarquias mais simples.

#### 7.1.2 Explicações para resultados divergentes
**Comportamento não-linear do LCOM na análise de popularidade:**
O resultado inesperado foi que repositórios muito populares apresentaram valores extremamente altos de LCOM (343.80), enquanto os extremamente populares voltaram a níveis moderados (102.71). Possíveis explicações:
- **Efeito threshold:** Projetos que atingem popularidade extrema passam por processos rigorosos de refatoração e reestruturação
- **Seleção natural:** Apenas projetos com arquitetura sustentável conseguem manter popularidade extrema a longo prazo
- **Recursos disponíveis:** Projetos extremamente populares têm mais recursos para investir em qualidade de código

#### 7.1.3 Padrões e insights interessantes
**Insight - "Sweet Spot" de Popularidade:**
Existe um padrão em U invertido na qualidade por popularidade. Repositórios populares (3.000-10.000 estrelas) e extremamente populares (>50.000) apresentam melhor qualidade que os muito populares (10.000-50.000). Isso sugere uma "zona crítica" onde projetos crescem rapidamente, mas ainda não desenvolveram processos maduros de governança.

### 7.2 RQ02 - Maturidade vs Qualidade

*[Espaço reservado para análise da RQ02]*

### 7.3 RQ03 - Atividade vs Qualidade

#### 7.3.1 Confirmação ou refutação das hipóteses
Nossa hipótese de que "repositórios mais ativos teriam pior qualidade inicial, mas melhor organização ao longo do tempo" foi **parcialmente refutada**. Os dados mostram que repositórios mais ativos apresentam consistentemente maior acoplamento (CBO crescendo de 4.52 para 6.41) e maior complexidade estrutural. Contudo, a hipótese foi confirmada no aspecto da coesão: projetos inativos apresentaram LCOM extremamente alto (218.96), indicando que o abandono deteriora significativamente a coesão do código.

#### 7.3.2 Explicações para resultados divergentes
**Aumento do acoplamento com atividade:**
O crescimento consistente do CBO com atividade contraria a expectativa de melhor qualidade. Possíveis causas:
- **Crescimento funcional:** Projetos mais ativos naturalmente adicionam mais funcionalidades, aumentando dependências
- **Pressão de entrega:** Releases frequentes podem priorizar funcionalidade sobre arquitetura ideal
- **Complexidade evolutiva:** Projetos maduros acumulam dependências históricas difíceis de refatorar

#### 7.3.3 Padrões e insights interessantes
**Insight - Abandono vs Atividade Excessiva:**
Ambos os extremos (projetos inativos e altamente ativos) apresentam problemas de qualidade, mas de naturezas diferentes:
- **Projetos inativos:** Deterioração da coesão (LCOM alto = 218.96)
- **Projetos hiperativos:** Aumento do acoplamento (CBO alto = 6.41)

**Insight - Estabilidade da Herança:**
A métrica DIT mostrou-se mais estável (variação de 1.38 a 1.52), sugerindo que decisões arquiteturais sobre hierarquia de herança são mais resistentes a mudanças relacionadas à atividade.

### 7.4 RQ04 - Tamanho vs Qualidade

*[Espaço reservado para análise da RQ04]*

### 7.5 Limitações Gerais

A análise revelou que **todos os repositórios estudados já são altamente populares** (>3.400 estrelas), limitando a generalização dos resultados para o ecossistema completo do GitHub. Isso pode ter enviesado os resultados em favor de projetos já estabelecidos e com certo nível de maturidade arquitetural.

---

## 8. Conclusão

### 8.1 Principais insights por questão de pesquisa

#### 8.1.1 RQ01 - Popularidade vs Qualidade
**Descobertas relevantes:**
- **Efeito não-linear da popularidade:** Repositórios extremamente populares (>50.000 estrelas) apresentam arquiteturas significativamente mais desacopladas (CBO = 3.03) comparados aos muito populares (CBO = 5.33)
- **Zona crítica de popularidade:** Projetos na faixa de 10.000-50.000 estrelas apresentam pior qualidade estrutural, sugerindo uma fase de crescimento descontrolado

**Confirmação das hipóteses:**
- **Confirmada:** Projetos extremamente populares têm melhor qualidade estrutural (CBO e DIT menores)

#### 8.1.2 RQ02 - Maturidade vs Qualidade

*[Espaço reservado para conclusões da RQ02]*

#### 8.1.3 RQ03 - Atividade vs Qualidade
**Descobertas relevantes:**
- **Trade-off atividade-acoplamento:** Maior atividade correlaciona fortemente com maior acoplamento, sugerindo que desenvolvimento intenso compromete a arquitetura
- **Deterioração por abandono:** Repositórios inativos apresentam os piores valores de coesão (LCOM = 218.96), confirmando que manutenção contínua é crucial

**Confirmação das hipóteses:**
- **Parcialmente confirmada:** Atividade melhora coesão comparado ao abandono, mas aumenta acoplamento
- **Refutada:** Projetos mais ativos não necessariamente têm melhor qualidade geral

#### 8.1.4 RQ04 - Tamanho vs Qualidade

*[Espaço reservado para conclusões da RQ04]*

### 8.2 Big numbers encontrados

**Popularidade extrema:** Analisamos repositórios de 3.414 a 151.757 estrelas, representando o top 1% dos projetos Java no GitHub
**Atividade intensa:** Encontramos projetos com até 2.215 releases, demonstrando desenvolvimento contínuo por anos
**Variabilidade de qualidade:** LCOM variou de 6.34 a 55.203, mostrando enorme diversidade na coesão de métodos
**Projetos maduros:** Idade média de 9,65 anos, indicando projetos estabelecidos e consolidados

### 8.3 Problemas e dificuldades enfrentadas

**Limitações metodológicas:**
- **Viés de seleção:** Amostra limitada aos repositórios mais populares (>3.400 estrelas), impedindo análise do ecossistema completo
- **Heterogeneidade temporal:** Repositórios de diferentes idades podem ter sido desenvolvidos com práticas e ferramentas distintas
- **Distribuição assimétrica:** Necessidade de abandonar tercis tradicionais em favor de faixas baseadas no domínio

**Desafios técnicos:**
- **Processamento de dados:** Normalização de 997 repositórios com métricas em diferentes escalas (0 a 55.203 para LCOM)
- **Valores extremos:** LCOM apresentou outliers significativos que requereram análise cuidadosa
- **Interpretação de métricas:** Diferenciação entre padrões estruturais intencionais e deterioração de código

### 8.4 Sugestões para trabalhos futuros

#### 8.4.1 Para RQ01 - Popularidade vs Qualidade
- **Análise de pontos de inflexão:** Identificar exatamente em que faixa de popularidade ocorre a melhoria da qualidade estrutural
- **Estudo longitudinal:** Acompanhar a evolução da qualidade conforme repositórios ganham popularidade ao longo do tempo

#### 8.4.2 Para RQ02 - Maturidade vs Qualidade

*[Espaço reservado para sugestões da RQ02]*

#### 8.4.3 Para RQ03 - Atividade vs Qualidade
- **Análise de padrões de release:** Investigar se o tipo de release (major, minor, patch) influencia diferentemente as métricas de qualidade
- **Correlação com práticas DevOps:** Relacionar frequência de releases com adoção de práticas de integração contínua

#### 8.4.4 Para RQ04 - Tamanho vs Qualidade

*[Espaço reservado para sugestões da RQ04]*

#### 8.4.5 Sugestões gerais
**Aprofundamento metodológico:**
- **Análise temporal:** Estudar evolução das métricas CK ao longo do ciclo de vida dos repositórios
- **Métricas complementares:** Incluir métricas de testabilidade, documentação e complexidade ciclomática
- **Análise multivariada:** Aplicar PCA para identificar padrões latentes entre múltiplas métricas

**Expansão do escopo:**
- **Diversidade linguística:** Comparar padrões entre Java, Python, JavaScript e outras linguagens populares
- **Segmentação por domínio:** Analisar frameworks, bibliotecas e aplicações separadamente
- **Inclusão de repositórios médios:** Expandir análise para repositórios com 100-3.000 estrelas

**Ferramentas e automação:**
- **Dashboard interativo:** Desenvolver interface web para exploração dinâmica das correlações
- **Predição de qualidade:** Implementar modelos ML para prever degradação de qualidade
- **Guidelines baseadas em evidências:** Desenvolver recomendações específicas por faixa de popularidade/atividade
- 
---

## 9. Referências
Liste as referências bibliográficas ou links utilizados.
- [GitHub API Documentation](https://docs.github.com/en/graphql)
- [CK Metrics Tool](https://ckjm.github.io/)
- [Biblioteca Pandas](https://pandas.pydata.org/)
- [Power BI](https://docs.microsoft.com/en-us/power-bi/fundamentals/service-get-started)

---

## 10. Apêndices
- Scripts utilizados para coleta e análise de dados.
- Consultas GraphQL ou endpoints REST.
- Planilhas e arquivos CSV gerados.

---
