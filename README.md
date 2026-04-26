# 🔐 Dashboard de Simulação de Login com 2FA

Projeto para análise e simulação de sistemas de autenticação com dois fatores (2FA), combinando **engenharia de dados, machine learning e teoria das filas**.

---

## 🎯 Objetivo

Simular e analisar o comportamento de um sistema de login real, permitindo:

* Avaliar desempenho (latência, throughput)
* Medir taxa de sucesso e falhas
* Detectar comportamentos anômalos
* Agrupar padrões de usuários
* Simular filas de autenticação (M/M/c)

---

## 🚀 Funcionalidades

* 📊 KPIs de autenticação
* ⚠️ Detecção de anomalias (Isolation Forest)
* 🔎 Clusterização de logins (K-Means)
* 🤖 Modelo preditivo de sucesso de login
* 🛡️ Análise de falhas por usuário
* 📐 Teoria das filas (M/M/1 e M/M/c)
* 🔬 Simulação de carga (burst de requisições)
* 📂 Upload de datasets (.csv / .xlsx)

---

## 🐳 Executando com Docker

```bash
docker build -t login-dashboard .
docker run -p 8501:8501 login-dashboard
```

Acesse no navegador:

```
http://localhost:8501
```

---

## 📂 Uso do Sistema

Ao iniciar o app, você pode:

* Enviar um dataset próprio (`.csv` ou `.xlsx`)
* Ou usar o dataset de exemplo

### Colunas mínimas esperadas:

* `login_success`
* `latency_ms`
* `login_duration_sec`

---

## ⚙️ Pipeline de Dados

1. Limpeza e tratamento de dados
2. Engenharia de features
3. Pré-processamento para modelagem
4. Cálculo de métricas
5. Aplicação de modelos
6. Simulação de filas

---

## 📊 Métricas Analisadas

| Métrica            | Descrição                            |
| ------------------ | ------------------------------------ |
| Taxa de sucesso    | % de logins bem-sucedidos            |
| Latência           | Tempo médio de autenticação          |
| Falhas por usuário | Comportamento suspeito               |
| Anomalias          | Eventos fora do padrão               |
| Tempo de fila      | Espera no sistema (teoria das filas) |

---

## 🧠 Técnicas Utilizadas

* **Teoria das Filas**: M/M/1, M/M/c
* **Anomalias**: Isolation Forest
* **Clusterização**: K-Means
* **Predição**: Random Forest
* **Simulação**: Monte Carlo

---

## 📁 Estrutura do Projeto

```
src/
├── app.py
├── data/
├── preprocessing/
├── metrics/
├── models/
├── analytics/
├── queue_simulation/
└── visualization/

Dockerfile
requirements.txt
main.py
```

---

## 📌 Observações

* O dataset original não é versionado no Git (boas práticas)
* O sistema aceita dados externos via upload
* Projeto modular e escalável

---

## 👨‍💻 Autor

Projeto desenvolvido para fins acadêmicos com foco em simulação e análise de sistemas reais de autenticação.
