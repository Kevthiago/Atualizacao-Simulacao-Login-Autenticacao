# Cálculo Preditivo

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def train_predictive_model(_df):
    df = _df.copy()
    feats = [c for c in ['login_duration_sec', 'latency_ms'] if c in df.columns]

    if not feats or 'login_success' not in df.columns:
        return None, "Faltam 'login_success' ou features (duração/latência)."

    data = df.copy().dropna(subset=feats + ['login_success'])
    if len(data) < 10:
        return None, "Poucos dados (após dropna) para treinar."

    X = data[feats].values
    y = data['login_success'].astype(int).values

    if len(np.unique(y)) < 2:
        return None, "Modelo requer duas classes (sucesso/falha) nos dados."

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    return model, {'accuracy': acc, 'features': feats}