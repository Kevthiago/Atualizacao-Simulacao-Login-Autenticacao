from pathlib import Path

# Raiz do projeto (2 níveis acima de src/config)
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "src/data"

DATA_RAW = DATA_DIR / "raw" / "simulacao_login_dataset1.xlsx"
DATA_PROCESSED = DATA_DIR / "processed" / "simulacao_login_dataset1_processed.csv"
DATA_MODEL_READY = DATA_DIR / "processed" / "simulacao_login_features_pronto.csv"

RANDOM_SEED = 42