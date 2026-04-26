import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# evita warning do sklearn
os.environ["LOKY_MAX_CPU_COUNT"] = "4"

# DATA
from data.loader import load_data
from config.config import DATA_PROCESSED

# MÉTRICAS
from metrics.kpis import compute_kpis

# MODELOS
from models.anomaly_detection import detect_anomalies_isolationforest
from models.clustering import cluster_logins
from models.predictive_model import train_predictive_model

# ANÁLISE
from analytics.failure_analysis import (
    find_users_with_many_failures,
    get_anomalous_user_details
)

# FILAS
from queue_simulation.mmc_queue import MMCQueue
from queue_simulation.simulation import (
    estimate_arrival_rate,
    estimate_service_time,
    generate_bursts,
    run_sim
)

# VISUAL
from visualization.plots import plot_bar_with_labels

# =========================================
# CONFIG
# =========================================
st.set_page_config(layout="wide")
st.title("🔐 Dashboard de Login com Autenticação 2FA")

# =========================================
# SIDEBAR
# =========================================
with st.sidebar:
    st.header("⚙️ Configurações")

    st.subheader("Anomalias")
    contamination = st.slider("Taxa de contaminação", 0.001, 0.1, 0.01)

    st.subheader("Clusterização")
    n_clusters = st.slider("Número de clusters", 2, 8, 3)

    st.subheader("Segurança")
    min_failures = st.number_input("Mínimo de falhas por usuário", 1, 50, 5)

    st.subheader("Filas")
    servers_m = st.slider("Servidores (teoria)", 1, 10, 3)

    servers_test = st.multiselect("Servidores (simulação)", [1,2,3,4,5], default=[1,2,3])
    runtime = st.number_input("Tempo da simulação (s)", value=3600, min_value=100)

# =========================================
# LOAD DATA
# =========================================
# try:
#     df = load_data(DATA_PROCESSED)
# except Exception as e:
#     st.error(f"Erro ao carregar dados: {e}")
#     st.stop()

df = None

st.markdown("## 📂 Carregue seu dataset")

uploaded_file = st.file_uploader(
    "Envie um arquivo (.csv ou .xlsx)",
    type=["csv", "xlsx"]
)

use_default = st.button("Usar dataset de exemplo")

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        REQUIRED_COLUMNS = ["login_success", "latency_ms", "login_duration_sec"]
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]

        if missing_cols:
            st.error(f"Colunas obrigatórias ausentes: {missing_cols}")
            st.stop()

        df = df.drop_duplicates()
        df = df.dropna(subset=["login_success"])
        df["login_success"] = df["login_success"].astype(int)

        st.success("Arquivo carregado com sucesso!")

    except Exception as e:
        st.error("Erro ao processar arquivo.")
        st.exception(e)
        st.stop()

elif use_default:
    try:
        df = load_data(DATA_PROCESSED)
        st.info("Usando dataset de exemplo")
    except Exception as e:
        st.error(f"Erro ao carregar dataset padrão: {e}")
        st.stop()

# 🚨 BLOQUEIO (sem sidebar agora)
if df is None:
    st.markdown("### ⬆️ Envie um arquivo para começar")
    st.stop()

# =========================================
# KPIs
# =========================================
st.header("📊 Indicadores Gerais")

kpis = compute_kpis(df)

col1, col2, col3 = st.columns(3)
col1.metric("Total de Logins", kpis.get("total_logins", 0))
col2.metric("Taxa de Sucesso", f"{kpis.get('success_rate', 0):.2%}")
col3.metric("Usuários Únicos", kpis.get("unique_users", 0))

st.divider()

# =========================================
# GRÁFICOS
# =========================================
st.header("📈 Análise de Comportamento")

if {"device_type", "login_success"}.issubset(df.columns):
    st.caption("Distribuição da taxa de sucesso por tipo de dispositivo")
    stats = df.groupby("device_type")["login_success"].mean().reset_index()
    plot_bar_with_labels(stats, "device_type", "login_success", "Sucesso por dispositivo")
else:
    st.info("Dados insuficientes para análise por dispositivo")

st.divider()

# =========================================
# ANOMALIAS
# =========================================
st.header("⚠️ Detecção de Anomalias")

features = [c for c in ["latency_ms", "login_duration_sec"] if c in df.columns]

if features:
    df_anom, _ = detect_anomalies_isolationforest(df, features, contamination)
    total_anom = int(df_anom["is_anomaly"].sum())

    st.metric("Eventos Anômalos Detectados", total_anom)

    if total_anom > 0:
        st.warning("Existem comportamentos fora do padrão — possível instabilidade ou ataque.")
else:
    st.warning("Não há dados suficientes para detectar anomalias")

st.divider()

# =========================================
# CLUSTER
# =========================================
st.header("🔎 Segmentação de Logins (Clustering)")

df_clustered, _, msg = cluster_logins(df, n_clusters)

if "cluster" in df_clustered.columns:
    st.write("Distribuição dos grupos identificados:")
    st.dataframe(df_clustered["cluster"].value_counts())
else:
    st.info(msg)

st.divider()

# =========================================
# MODELO
# =========================================
st.header("🤖 Modelo Preditivo")

model, info = train_predictive_model(df)

if model:
    st.metric("Acurácia do Modelo", f"{info['accuracy']:.2%}")
else:
    st.info(info)

st.divider()

# =========================================
# SEGURANÇA
# =========================================
st.header("🛡️ Análise de Segurança")

users_df, threshold, error = find_users_with_many_failures(
    df,
    quantile_threshold=0.95,
    min_failures_threshold=min_failures
)

if error:
    st.info(error)
elif users_df.empty:
    st.success("Nenhum comportamento suspeito identificado")
else:
    st.markdown(f"Usuários com comportamento suspeito (≥ **{int(threshold)} falhas**)")

    st.dataframe(users_df.head(10))
    st.bar_chart(users_df.head(10))

    anomalous_ids_list = list(users_df.index)

    top_ips, top_devices, err = get_anomalous_user_details(df, anomalous_ids_list)

    if not err:
        col1, col2 = st.columns(2)

        with col1:
            st.write("IPs mais utilizados")
            st.dataframe(top_ips)

        with col2:
            st.write("Dispositivos mais utilizados")
            st.dataframe(top_devices)

st.divider()

# =========================================
# FILAS
# =========================================
st.header("📐 Teoria de Filas (M/M/c)")

if "timestamp" in df.columns:
    try:
        λ = estimate_arrival_rate(df)
        service_time = estimate_service_time(df)
        μ = 1 / service_time if service_time > 0 else 0

        q = MMCQueue(λ, μ, servers_m)
        rho = q.utilization()

        st.metric("Utilização do Sistema (ρ)", f"{rho:.2%}")

        if rho < 0.7:
            st.success("Sistema com baixa carga")
        elif rho < 1:
            st.warning("Sistema próximo do limite")
        else:
            st.error("Sistema instável (sobrecarga)")

    except Exception as e:
        st.warning(f"Erro na análise de filas: {e}")
else:
    st.warning("Coluna 'timestamp' necessária para análise de filas")

st.divider()

# =========================================
# SIMULAÇÃO
# =========================================
st.header("🔬 Simulação de Estresse")

if st.button("Executar Simulação"):

    if "timestamp" not in df.columns:
        st.error("Simulação requer dados temporais (timestamp)")
    else:
        bursts = generate_bursts(runtime)
        bursts_tuple = tuple(bursts)

        results = []

        for s in servers_test:
            try:
                w, total = run_sim(s, runtime, bursts_tuple, λ, service_time)
                results.append((s, w))
            except Exception as e:
                st.warning(f"Erro com {s} servidores: {e}")

        if results:
            res_df = pd.DataFrame(results, columns=["Servidores", "Tempo Médio de Espera (s)"])

            st.subheader("Resultados da Simulação")
            st.dataframe(res_df)

            st.line_chart(res_df.set_index("Servidores"))

            st.caption("Mais servidores reduzem o tempo de espera sob picos de carga")
        else:
            st.warning("Simulação não gerou resultados")