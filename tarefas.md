# Tarefas de Melhoria do Laboratório

Este documento mapeia todas as permutações de experimentos a serem realizados, combinando as três melhorias identificadas no Capítulo 5 do TCC: uso do LycoS-IDS2017, redução de dimensionalidade (MDI) e abordagem não supervisionada.

---

## Experimentos Supervisionados (RF + DNN)

Os cenários de treino são: **Completo** (todas as classes), **Sem XSS** e **Sem PortScan**.

### Baseline — CICIDS2017, sem redução de dimensionalidade
- [x] Completo
- [x] Sem XSS no treino
- [x] Sem PortScan no treino

### Melhoria A — LycoS-IDS2017, sem redução de dimensionalidade
- [x] Completo (RF + DNN)
- [x] Sem XSS no treino (RF + DNN)
- [x] Sem PortScan no treino (RF + DNN)

### Melhoria B — CICIDS2017, com redução de dimensionalidade (MDI via RF)
- [x] Completo (DNN com features reduzidas)
- [x] Sem XSS no treino
- [x] Sem PortScan no treino

### Melhoria C — LycoS-IDS2017, com redução de dimensionalidade (MDI via RF)
- [x] Completo (DNN com features reduzidas)
- [x] Sem XSS no treino
- [x] Sem PortScan no treino

---

## Experimentos Não Supervisionados (Autoencoder)

> O treino é realizado **exclusivamente com tráfego BENIGN** — não há distinção de "sem XSS/PortScan no treino". Os cenários referem-se ao **conjunto de teste** utilizado para avaliação.

### Pré-requisitos (implementação única)
- [x] Definir e implementar a arquitetura do Autoencoder (78→64→32→16→32→64→78, MSE). *(em `Não Supervisionado/Autoencoder - cicids2017.ipynb`)*
- [x] Definir a estratégia de limiar de anomalia (95º percentil do erro de reconstrução no treino BENIGN).

### Melhoria D — CICIDS2017, sem redução de dimensionalidade
- [x] Avaliado no conjunto de teste completo

### Melhoria E — LycoS-IDS2017, sem redução de dimensionalidade
- [x] Avaliado no conjunto de teste completo

### Melhoria F — CICIDS2017, com redução de dimensionalidade (MDI)
- [x] Avaliado no conjunto de teste completo

### Melhoria G — LycoS-IDS2017, com redução de dimensionalidade (MDI)
- [x] Avaliado no conjunto de teste completo

---

## Adendo: Inventário de Scripts

### Legenda
- ✅ Existe e foi executado
- 🟡 Script criado, ainda não executado
- ❌ Não existe

### Supervisionados — CICIDS2017

| Script | Status |
|---|---|
| DNN - Completo | ✅ |
| RF - Completo | ✅ |
| DNN - Sem XSS no treino | ✅ |
| RF - Sem XSS no treino | ✅ |
| DNN - Sem PortScan no treino | ✅ |
| RF - Sem PortScan no treino | ✅ |

### Supervisionados — LycoS-IDS2017

| Script | Status |
|---|---|
| DNN - Completo | ✅ |
| RF - Completo | ✅ |
| DNN - Sem XSS no treino | ✅ |
| RF - Sem XSS no treino | ✅ |
| DNN - Sem PortScan no treino | ✅ |
| RF - Sem PortScan no treino | ✅ |

### Redução de Dimensionalidade (scripts MDI via RF)

> Um único notebook por dataset gera todos os cenários (Completo, Sem XSS, Sem PortScan, Balanced).

| Script | Status |
|---|---|
| CICIDS2017 - Completo | ✅ |
| CICIDS2017 - Sem XSS no treino | ✅ |
| CICIDS2017 - Sem PortScan no treino | ✅ |
| CICIDS2017 - Balanced | ✅ |
| LycoS - Completo | ✅ |
| LycoS - Sem XSS no treino | ✅ |
| LycoS - Sem PortScan no treino | ✅ |
| LycoS - Balanced | ✅ |

### Treinamento DNN — Com Redução de Dimensionalidade

| Script | Status |
|---|---|
| CICIDS2017 - Completo | ✅ |
| CICIDS2017 - Sem XSS no treino | ✅ |
| CICIDS2017 - Sem PortScan no treino | ✅ |
| CICIDS2017 - Balanced | ✅ |
| LycoS - Completo | ✅ |
| LycoS - Sem XSS no treino | ✅ |
| LycoS - Sem PortScan no treino | ✅ |
| LycoS - Balanced | ✅ |

### Não Supervisionados (Autoencoder)

| Script | Status |
|---|---|
| CICIDS2017 - Teste completo | ✅ |
| LycoS - Teste completo | ✅ |
| CICIDS2017 + MDI - Teste completo | ✅ |
| LycoS + MDI - Teste completo | ✅ |
