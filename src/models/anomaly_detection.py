# Cálculo de Anomalias

from sklearn.ensemble import IsolationForest

def detect_anomalies_isolationforest(_df, features, contamination=0.01):
    df = _df.copy()
    iso = IsolationForest(contamination=contamination, random_state=42)
    X = df[features].fillna(0).values
    if len(X) == 0:
        return df, None
    iso.fit(X)
    df['anomaly_score'] = iso.decision_function(X)
    df['is_anomaly'] = (iso.predict(X) == -1).astype(int)
    return df, iso