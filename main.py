# main.py
import pandas as pd
import os
from pathlib import Path

# Configuração dos caminhos dos dados
from src.config import DATA_RAW, DATA_PROCESSED, DATA_MODEL_READY

# Pré-processamento dos dados
from src.preprocessing.clean_data import clean_dataset
from src.preprocessing.feature_engineering import create_features, preprocess_for_model

# (Imports das outras etapas estão comentados, pois ainda não existem)
# from src.metrics.success_rate import success_rate
# ...e assim por diante


def main_data_pipeline():
    """
    Executa o pipeline de preparação de dados:
    1. Carrega dados brutos.
    2. Limpa os dados e salva em DATA_PROCESSED.
    3. Aplica engenharia de features.
    4. Aplica pré-processamento final e salva em DATA_MODEL_READY.
    """
    print("Iniciando o pipeline de preparação de dados...")

    # Garantir que os diretórios de saída existam
    os.makedirs(Path(DATA_PROCESSED).parent, exist_ok=True)
    os.makedirs(Path(DATA_MODEL_READY).parent, exist_ok=True)

    # Passo 1: Limpeza dos dados
    print("Etapa 1: Carregando e limpando dados brutos...")
    try:
        df_raw = pd.read_excel(DATA_RAW)
    except FileNotFoundError:
        print(f"Erro: Arquivo bruto não encontrado em {DATA_RAW}")
        return
        
    df_clean = clean_dataset(df_raw)
    
    # Salvar o arquivo limpo intermediário
    df_clean.to_csv(DATA_PROCESSED, index=False)
    print(f"Dados limpos salvos em: {DATA_PROCESSED}")


    # Passo 2: Engenharia de características
    print("Etapa 2: Engenharia de características...")
    # (Note que `create_features` espera o df limpo, que vem de DATA_PROCESSED)
    df_featured = create_features(df_clean) 

    # Passo 3: Pré-processamento final para o modelo
    print("Etapa 3: Pré-processamento final para o modelo...")
    df_model_ready = preprocess_for_model(df_featured)

    # Passo 4: Salvar os dados prontos para o modelo
    print("Etapa 4: Salvando os dados prontos para o modelo...")
    df_model_ready.to_csv(DATA_MODEL_READY, index=False)
    print(f"Dados prontos para o modelo salvos em: {DATA_MODEL_READY}")
    
    print("\n--- Pipeline de Dados Concluído com Sucesso! ---")
    print(f"Dataset final: {df_model_ready.shape}")
    print(df_model_ready.head())


if __name__ == "__main__":
    main_data_pipeline()