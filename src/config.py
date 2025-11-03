# Configurações do aplicativo src/config.py
import os
from pathlib import Path

# Caminhos principais
BASE_DIR = Path(__file__).resolve().parent.parent # Caminho raiz do projeto
DATA_RAW = BASE_DIR / 'data' / 'raw' / 'simulacao_login_dataset1.xlsx' # Caminho do arquivo de dados brutos
DATA_PROCESSED = BASE_DIR / "data" / "processed" / "simulacao_login_dataset1_processed.csv" # Caminho do arquivo de dados processados
DATA_MODEL_READY = BASE_DIR / "data" / "processed" / "simulacao_login_features_pronto.csv" # Caminho do dataset pronto para modelo

# Parametros Gerais
RANDOM_SEED = 42 # Semente para reprodutibilidade