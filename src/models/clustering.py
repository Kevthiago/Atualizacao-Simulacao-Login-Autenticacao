# Cálculo de Agrupamento
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def cluster_logins(_df, n_clusters=3):
    df = _df.copy()
    features = [c for c in ['login_duration_sec', 'latency_ms'] if c in df.columns]
    if not features:
        return df, None, "Sem features (duração/latência) para clusterizar."

    data_to_cluster = df[features].fillna(df[features].median())
    if len(data_to_cluster) < n_clusters:
        return df, None, "Menos amostras do que clusters."

    X = data_to_cluster.values
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(Xs)
    df['cluster'] = labels
    return df, kmeans, f"Clusterizado com base em: {', '.join(features)}"