import pandas as pd

def load_data(path):
    df = pd.read_csv(path)

    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['weekday'] = df['timestamp'].dt.day_name()

    return df