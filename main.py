# Ponto de Entrada do Programa

import os
import pandas as pd

# Configuração dos caminhos dos dados
from src.config import DATA_PROCESSED

# Pré-processamento dos dados
from src.preprocessing.clean_data import clean_dataset
from src.preprocessing.feature_engineering import create_features

# Métricas
from src.metrics.success_rate import success_rate
from src.metrics.latency_metrics import latency_stats

# Simulação das Filas
from src.queue_simulation import mm1_queue
from src.queue_simulation import mm2_queue

# Modelos e detecção
from src.models.anomaly_detection import detect_anomalies
from src.models.clustering import run_clustering
from src.models.predictive_model import train_predictive_model

# Visualização
# (você pode deixar vazio por enquanto, mas já prepara o import)
# from src.visualization.plot_kpis import plot_metrics

def main():
    print("Iniciando o pipeline de simulação de login com 2FA...")

    # Passo 1: Limpeza dos dados
    print("Etapa 1: Limpeza dos dados...")
    df = clean_dataset()

    # Passo 2: Engenharia de características
    print("Etapa 2: Engenharia de características...")
    df = create_features(df)

    # Passo 3: Cálculo das métricas
    print("Etapa 3: Cálculo de métricas...")
    print(f"Taxa de sucesso: {success_rate(df):.2f}%")
    print("Estatísticas de latência:")
    print(latency_stats(df))

    # Passo 4: Simulação das filas
    print("Etapa 4: Simulação das filas (MM1 e MM2)...")
    results_mm1 = mm1_queue(lambd=2.5, mu=4.0)
    results_mm2 = mm2_queue(lambd=2.5, mu=4.0, c=2)
    print("Resultados da simulação MM1:")
    print(results_mm1)
    print("Resultados da simulação MM2:")
    print(results_mm2)

    # Passo 5: Modelos e detecção
    print("Etapa 5: Detecção de anomalias e padrões...")
    anomalies = detect_anomalies(df)
    clusters = run_clustering(df)
    model = train_predictive_model(df)

    # Passo 6: Salvar os resultados processados
    print("Etapa 6: Salvando os dados processados...")
    os.makedirs(os.path.dirname(DATA_PROCESSED), exist_ok=True)
    df.to_csv(DATA_PROCESSED, index=False)
    print(f"Dados processados salvos em: {DATA_PROCESSED}")

    # Visualização (se implementada)
    # print("Etapa 7: Visualização dos KPIs...")
    # plot_metrics(df)

    print("Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()