# src/preprocessing/clean_data.py
import pandas as pd

# Remova os imports do config.py daqui

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza a limpeza básica nos dados brutos.
    Recebe um DataFrame e retorna um DataFrame limpo.
    """
    print("Executando limpeza (duplicatas, NaNs críticos)...")
    
    # Realizar a limpeza dos dados
    df_clean = df.drop_duplicates() # Remover duplicatas
    df_clean = df_clean.dropna(subset=["user_id", "timestamp"]) # Remover linhas com valores ausentes
    
    # (Estas duas linhas são opcionais aqui, pois o feature_engineering fará isso,
    # mas é uma boa prática garantir o tipo certo)
    df_clean["timestamp"] = pd.to_datetime(df_clean["timestamp"]) 
    df_clean = df_clean.reset_index(drop=True) # Resetar o índice

    return df_clean