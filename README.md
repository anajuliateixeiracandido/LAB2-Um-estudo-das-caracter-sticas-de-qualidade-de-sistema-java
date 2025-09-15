
Este projeto realiza um estudo das características de qualidade de sistemas Java, analisando métricas de acoplamento, herança e coesão em repositórios populares do GitHub. A coleta e análise dos dados são feitas com a ferramenta CK, relacionando qualidade com popularidade, maturidade, atividade e tamanho dos repositórios.

### Questões de Pesquisa
Este laboratório tem o objetivo de responder às seguintes questões de pesquisa:

- RQ 01. Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
- RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade?
- RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
- RQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?


# 📝 Laboratório 02 - Um estudo das características de qualidade de sistema java

## 1. Informações do grupo
- **🎓 Curso:** Engenharia de Software
- **📘 Disciplina:** Laboratório de Experimentação de Software
- **🗓 Período:** 6° Período
- **👨‍🏫 Professor(a):** Prof. Wesley Dias Maciel
- **👥 Membros do Grupo:** [[Ana Julia Teixeira Candido](https://github.com/anajuliateixeiracandido) e [Marcella Ferreira Chaves Costa](https://github.com/marcellafccosta)]

---

## 2. Introdução
Descreva o contexto do laboratório, o objetivo do estudo e a relevância da análise.  
Inclua hipóteses informais sobre os resultados esperados.

**💡 Exemplos de Hipóteses Informais - Informal Hypotheses (IH):**

- **IH01:** Sistemas populares recebem mais contribuições externas e lançam releases com maior frequência, refletindo um processo de desenvolvimento ativo.
- **IH02:** Mais de 50% dos repositórios populares são mantidos há mais de 5 anos, indicando maturidade do projeto.
- **IH03:** Espera-se que mais de 50% dos repositórios populares tenham pelo menos 70% das issues fechadas, demonstrando boa gestão de problemas.
- **IH04:** Repositórios populares tendem a ser escritos nas linguagens mais utilizadas (ex.: JavaScript, Python, Java), representando a adoção de linguagens consolidadas.
- **IH05:** Mais de 50% dos repositórios populares recebem atualizações nos últimos 3 meses, refletindo atividade contínua da comunidade.
- **IH06:** Projetos populares com maior número de forks tendem a ter mais pull requests aceitas, indicando engajamento externo significativo.
- **IH07:** Repositórios populares com grande número de stars podem apresentar Big Numbers em métricas como número de commits, branches e releases, destacando sua relevância na comunidade open-source.

---

## 3. Tecnologias e ferramentas utilizadas
- **💻 Linguagem de Programação:** [Ex.: Python, Java]
- **🛠 Frameworks/Bibliotecas:** [Ex.: Pandas, Matplotlib, Seaborn, CK]
- **🌐 APIs utilizadas:** [Ex.: GitHub GraphQL API, GitHub REST API]
- **📦 Dependências:** [Ex.: requests, numpy]

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

**🔍 Questões de Pesquisa - Research Questions (RQs):**

| RQ   | Pergunta | Métrica utilizada | Código da Métrica |
|------|----------|-----------------|-----------------|
| RQ01 | Sistemas populares são maduros/antigos? | 🕰 Idade do repositório (calculado a partir da data de criação) | LM01 |
| RQ02 | Sistemas populares recebem muita contribuição externa? | ✅ Total de Pull Requests Aceitas | LM02 |
| RQ03 | Sistemas populares lançam releases com frequência? | 📦 Total de Releases | LM03 |
| RQ04 | Sistemas populares são atualizados com frequência? | ⏳ Tempo desde a última atualização (dias) | LM04 |
| RQ05 | Sistemas populares são escritos nas linguagens mais populares? | 💻 Linguagem primária de cada repositório | AM01 |
| RQ06 | Sistemas populares possuem um alto percentual de issues fechadas? | 📋 Razão entre número de issues fechadas pelo total de issues | LM05 |
| RQ07 | Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência? | ✅ Pull Requests Aceitas, 📦 Número de Releases, ⏳ Tempo desde a Última Atualização, 💻 Linguagem primária | LM02, LM03, LM04, AM01 |

---

## 6. Resultados

Apresente os resultados obtidos, com tabelas e gráficos sempre que possível.

---

### 6.1 Métricas

Inclua métricas relevantes de repositórios do GitHub, separando **métricas do laboratório** e **métricas adicionais trazidas pelo grupo**:

#### 📊 Métricas de Laboratório - Lab Metrics (LM)
| Código | Métrica | Descrição |
|--------|--------|-----------|
| LM01 | 🕰 Idade do Repositório (anos) | Tempo desde a criação do repositório até o momento atual, medido em anos. |
| LM02 | ✅ Pull Requests Aceitas | Quantidade de pull requests que foram aceitas e incorporadas ao repositório. |
| LM03 | 📦 Número de Releases | Total de versões ou releases oficiais publicadas no repositório. |
| LM04 | ⏳ Tempo desde a Última Atualização (dias) | Número de dias desde a última modificação ou commit no repositório. |
| LM05 | 📋 Percentual de Issues Fechadas (%) | Proporção de issues fechadas em relação ao total de issues criadas, em percentual. |
| LM06 | ⭐ Número de Estrelas | Quantidade de estrelas recebidas no GitHub, representando interesse ou popularidade. |
| LM07 | 🍴 Número de Forks | Número de forks, indicando quantas vezes o repositório foi copiado por outros usuários. |
| LM08 | 📏 Tamanho do Repositório (LOC) | Total de linhas de código (Lines of Code) contidas no repositório. |

#### 💡 Métricas adicionais trazidas pelo grupo - Additional Metrics (AM)
| Código | Métrica | Descrição |
|------|--------|------------|
| AM01 | 💻 Linguagem Primária | Linguagem de programação principal do repositório (ex.: Python, JavaScript, Java) |
| AM02 | 🔗 Forks vs Pull Requests Aceitas | Relação entre número de forks e pull requests aceitas |
| AM03 | 📈 Evolução Temporal | Evolução temporal de releases e pull requests aceitas |
| AM04 | 🌟 Big Numbers | Métricas com valores expressivos (commits, branches, stars, releases) |

> Obs.: Adapte ou acrescente métricas conforme o seu dataset.

---

### 6.2 Distribuição por categoria

Para métricas categóricas, como linguagem de programação, faça contagens e tabelas de frequência:

| Linguagem | Quantidade de Repositórios |
|---------------|------------------------|
| 🐍 Python     | 350                    |
| 💻 JavaScript | 300                    |
| ☕ Java        | 200                    |
| 📦 Outros     | 150                    |

---

### 6.3 Relação das RQs com as Métricas

| RQ   | Pergunta | Métrica utilizada | Código |
|------|----------|-----------------|--------|
| RQ01 | Sistemas populares são maduros/antigos? | 🕰 Idade do Repositório (calculado a partir da data de criação) | LM01 |
| RQ02 | Sistemas populares recebem muita contribuição externa? | ✅ Total de Pull Requests Aceitas | LM02 |
| RQ03 | Sistemas populares lançam releases com frequência? | 📦 Total de Releases | LM03 |
| RQ04 | Sistemas populares são atualizados com frequência? | ⏳ Tempo desde a Última Atualização (dias) | LM04 |
| RQ05 | Sistemas populares são escritos nas linguagens mais populares? | 💻 Linguagem primária de cada repositório | AM01 |
| RQ06 | Sistemas populares possuem alto percentual de issues fechadas? | 📋 Razão entre número de issues fechadas pelo total de issues | LM05 |
| RQ07 | Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência? | ✅ Pull Requests Aceitas, 📦 Número de Releases, ⏳ Tempo desde a Última Atualização, 💻 Linguagem primária | LM02, LM03, LM04, AM01 |

---

### 6.4 Sugestões de gráficos

Para criar visualizações das métricas, recomenda-se utilizar como referência o projeto **Seaborn Samples**:  
- 🔗 Repositório: [Projeto Seaborn Samples](https://github.com/joaopauloaramuni/laboratorio-de-experimentacao-de-software/tree/main/PROJETOS/Projeto%20Seaborn%20Samples)

- **📊 Histograma**: `grafico_histograma.png` → distribuição de idade, PRs aceitas ou estrelas.  
- **📈 Boxplot**: `grafico_boxplot.png` → dispersão de métricas como forks, issues fechadas ou LOC.  
- **📊 Gráfico de Barras**: `grafico_barras.png` → comparação de métricas entre linguagens.  
- **🥧 Gráfico de Pizza**: `grafico_pizza.png` → percentual de repositórios por linguagem.  
- **📈 Gráfico de Linha**: `grafico_linha.png` → evolução de releases ou PRs ao longo do tempo.  
- **🔹 Scatterplot / Dispersão**: `grafico_dispersao.png` → relação entre estrelas e forks.  
- **🌡 Heatmap**: `grafico_heatmap.png` → correlação entre métricas (idade, PRs, stars, forks, issues).  
- **🔗 Pairplot**: `grafico_pairplot.png` → análise de múltiplas métricas simultaneamente.  
- **🎻 Violin Plot**: `grafico_violin.png` → distribuição detalhada de métricas por subgrupo.  
- **📊 Barras Empilhadas**: `grafico_barras_empilhadas.png` → comparação de categorias dentro de métricas.

> 💡 Dica: combine tabelas e gráficos para facilitar a interpretação e evidenciar padrões nos dados.

### 6.5 Estatísticas Descritivas

Apresente as estatísticas descritivas das métricas analisadas, permitindo uma compreensão mais detalhada da distribuição dos dados.

| Métrica | Código | Média | Mediana | Moda | Desvio Padrão | Mínimo | Máximo |
|---------|--------|------|--------|-----|---------------|--------|--------|
| 🕰 Idade do Repositório (anos) | LM01 | X | Y | Z | A | B | C |
| ✅ Pull Requests Aceitas | LM02 | X | Y | Z | A | B | C |
| 📦 Número de Releases | LM03 | X | Y | Z | A | B | C |
| ⏳ Tempo desde a Última Atualização (dias) | LM04 | X | Y | Z | A | B | C |
| 📋 Percentual de Issues Fechadas (%) | LM05 | X | Y | Z | A | B | C |
| ⭐ Número de Estrelas (Stars) | LM06 | X | Y | Z | A | B | C |
| 🍴 Número de Forks | LM07 | X | Y | Z | A | B | C |
| 📏 Tamanho do Repositório (LOC) | LM08 | X | Y | Z | A | B | C |

> 💡 Dica: Inclua gráficos como histogramas ou boxplots junto com essas estatísticas para facilitar a interpretação.

---

## 7. Discussão

Nesta seção, compare os resultados obtidos com as hipóteses informais levantadas pelo grupo no início do experimento.

- **✅ Confirmação ou refutação das hipóteses**: identifique quais hipóteses foram confirmadas pelos dados e quais foram refutadas.  
- **❌ Explicações para resultados divergentes**: caso algum resultado seja diferente do esperado, tente levantar possíveis causas ou fatores que possam ter influenciado.  
- **🔍 Padrões e insights interessantes**: destaque tendências ou comportamentos relevantes observados nos dados que não haviam sido previstos nas hipóteses.  
- **📊 Comparação por subgrupos (opcional)**: se houver segmentação dos dados (ex.: por linguagem de programação, tamanho do repositório), discuta como os resultados se comportam em cada grupo.  

> Relacione sempre os pontos observados com as hipóteses informais definidas na introdução, fortalecendo a análise crítica do experimento.

---

## 8. Conclusão

Resumo das principais descobertas do laboratório.

- **🏆 Principais insights:**  
  - Big numbers encontrados nos repositórios, popularidade e métricas destacadas.  
  - Descobertas relevantes sobre padrões de contribuição, releases, issues fechadas ou linguagens mais utilizadas.  
  - Confirmações ou refutações das hipóteses informais levantadas pelo grupo.

- **⚠️ Problemas e dificuldades enfrentadas:**  
  - Limitações da API do GitHub e paginação de grandes volumes de dados.  
  - Normalização e tratamento de dados inconsistentes ou ausentes.  
  - Desafios com cálculos de métricas ou integração de múltiplos arquivos CSV.  

- **🚀 Sugestões para trabalhos futuros:**  
  - Analisar métricas adicionais ou aprofundar correlações entre métricas de qualidade e métricas de processo.  
  - Testar outras linguagens de programação ou frameworks.  
  - Implementar dashboards interativos para visualização de grandes volumes de dados.  
  - Explorar métricas de tendências temporais ou evolução de repositórios ao longo do tempo.

---

## 9. Referências
Liste as referências bibliográficas ou links utilizados.
- [📌 GitHub API Documentation](https://docs.github.com/en/graphql)
- [📌 CK Metrics Tool](https://ckjm.github.io/)
- [📌 Biblioteca Pandas](https://pandas.pydata.org/)
- [📌 Power BI](https://docs.microsoft.com/en-us/power-bi/fundamentals/service-get-started)

---

## 10. Apêndices
- 💾 Scripts utilizados para coleta e análise de dados.
- 🔗 Consultas GraphQL ou endpoints REST.
- 📊 Planilhas e arquivos CSV gerados.

---
