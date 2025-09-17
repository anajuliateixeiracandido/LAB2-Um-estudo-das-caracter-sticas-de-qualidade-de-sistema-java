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

- **IH01:** 

- **IH02:** Repositórios mais maduros (ou seja, com maior idade) tendem a apresentar uma qualidade de código superior, como menor acoplamento entre objetos (CBO) e menor profundidade de herança (DIT), devido ao tempo de desenvolvimento e refinamento constante do código.

- **IH03:** 
- **IH04:** Repositórios maiores, com mais linhas de código (LOC) e mais linhas de comentários, tendem a apresentar piores características de qualidade de código, como maior acoplamento entre objetos (CBO), maior profundidade de herança (DIT) e menor coesão de métodos (LCOM), devido à maior complexidade e dificuldade de manutenção associada a sistemas maiores.

**Hipóteses Formais - Formal Hypotheses (FH):**
#### **RQ01 - Popularidade vs Qualidade:**
- **H0₁:** 
- **H1₁:** 

#### **RQ02 - Maturidade vs Qualidade:**
- **H0₂:** Não existe correlação significativa entre a maturidade dos repositórios (idade em anos) e suas métricas de qualidade de código (CBO, DIT, WMC, LCOM).
- **H1₂:** Existe correlação significativa entre a maturidade dos repositórios e suas métricas de qualidade de código.

#### **RQ03 - Atividade vs Qualidade:**
- **H0₃:** 
- **H1₃:** 

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
Descreva detalhadamente as etapas do experimento ou estudo, incluindo coleta de dados, filtragem, normalização, análise e visualização.

### 4.1 Coleta de dados
- Foram coletados dados de [X] repositórios utilizando a [GitHub API].
- Critérios de seleção: [Ex.: top-1000 por número de estrelas, linguagem específica, etc.]

### 4.2 Filtragem e paginação
- Foi utilizada paginação da API devido ao grande volume de dados.
- ⏱ Tempo médio de coleta: [XX minutos].

### 4.3 Normalização e pré-processamento
- Os dados foram normalizados utilizando [ex.: min-max scaling] para garantir consistência.

### 4.4 Cálculo de métricas
- Métricas de interesse: idade do repositório, número de pull requests aceitas, número de releases, tempo desde a última atualização, linguagem primária, percentual de issues fechadas.
- Métricas compostas calculadas por meio de combinação linear ponderada de fatores relevantes.

### 4.5 Ordenação e análise inicial
- Repositórios ordenados por pontuação composta ou por número de estrelas.
- Análise inicial baseada em valores medianos e contagem de categorias.

---

## 5. Questões de pesquisa

Liste as questões de pesquisa que guiaram o estudo, com suas métricas associadas:

**Questões de Pesquisa - Research Questions (RQs):**

| RQ   | Pergunta | Métrica utilizada | Código da Métrica |
|------|----------|-----------------|-----------------|
| RQ01 | Qual a relação entre a popularidade dos repositórios e as suas características de qualidade? | Número de estrelas | LM01 |
| RQ02 | Qual a relação entre a maturidade do repositórios e as suas características de qualidade? | Idade (em anos) de cada repositório coletado, CBO e DIT | LM02 |
| RQ03 | Qual a relação entre a atividade dos repositórios e as suas características de qualidade? | Número de releases | LM03 |
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

### 6.2 Estatísticas Descritivas

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



### 6.3 Análises

#### 6.3.1 RQ01 (Popularidade x Qualidade)

#### 6.3.2 RQ02 (Maturidade x Qualidade)

#### 6.3.3 RQ03 (Atividade x Qualidade)

#### 6.3.4 RQ04 (Tamanho x Qualidade)

---

## 7. Discussão

Nesta seção, compare os resultados obtidos com as hipóteses informais levantadas pelo grupo no início do experimento.

- Confirmação ou refutação das hipóteses: identifique quais hipóteses foram confirmadas pelos dados e quais foram refutadas.  
- Explicações para resultados divergentes: caso algum resultado seja diferente do esperado, tente levantar possíveis causas ou fatores que possam ter influenciado.  
- Padrões e insights interessantes: destaque tendências ou comportamentos relevantes observados nos dados que não haviam sido previstos nas hipóteses.  
- Comparação por subgrupos (opcional): se houver segmentação dos dados (ex.: por linguagem de programação, tamanho do repositório), discuta como os resultados se comportam em cada grupo.  

> Relacione sempre os pontos observados com as hipóteses informais definidas na introdução, fortalecendo a análise crítica do experimento.

---

## 8. Conclusão

Resumo das principais descobertas do laboratório.

- Principais insights:  
  - Big numbers encontrados nos repositórios, popularidade e métricas destacadas.  
  - Descobertas relevantes sobre padrões de contribuição, releases, issues fechadas ou linguagens mais utilizadas.  
  - Confirmações ou refutações das hipóteses informais levantadas pelo grupo.

- Problemas e dificuldades enfrentadas:  
  - Limitações da API do GitHub e paginação de grandes volumes de dados.  
  - Normalização e tratamento de dados inconsistentes ou ausentes.  
  - Desafios com cálculos de métricas ou integração de múltiplos arquivos CSV.  

- Sugestões para trabalhos futuros:  
  - Analisar métricas adicionais ou aprofundar correlações entre métricas de qualidade e métricas de processo.  
  - Testar outras linguagens de programação ou frameworks.  
  - Implementar dashboards interativos para visualização de grandes volumes de dados.  
  - Explorar métricas de tendências temporais ou evolução de repositórios ao longo do tempo.

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
