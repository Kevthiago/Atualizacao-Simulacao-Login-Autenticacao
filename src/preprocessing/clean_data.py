# Limpeza dos dados
import pandas as pd
from src.config import DATA_RAW, DATA_PROCESSED

def clean_data():
    # Carregar os dados brutos
    df = pd.read_excel(DATA_RAW)

    # Realizar a limpeza dos dados
    df = df.drop_duplicates() # Remover duplicatas
    df = df.dropna(subset=["user_id", "timestamp"]) # Remover linhas com valores ausentes em colunas críticas
    df["timestamp"] = pd.to_datetime(df["timestamp"]) # Converter timestamps para datetime
    df = df.sort_values(by="timestamp") # Ordenar por timestamp
    df = df.reset_index(drop=True) # Resetar o índice

    # Salvar os dados limpos
    df.to_csv(DATA_PROCESSED, index=False) 

    print(f"Dados limpos salvos em: {DATA_PROCESSED}")
    print(df.info())
    print("Primeiras linhas dos dados limpos:")
    print(df.head())
