import pandas as pd

def find_users_with_many_failures(_df, quantile_threshold=0.95, min_failures_threshold=3):
    df = _df.copy()
    if 'login_success' not in df.columns or 'user_id' not in df.columns:
        return pd.DataFrame(columns=['user_id', 'failure_count']), 0, "Colunas 'user_id' ou 'login_success' em falta."

    failures = df[df['login_success'] == 0]
    if failures.empty:
        return pd.DataFrame(columns=['user_id', 'failure_count']), 0, "Não foram registadas falhas no dataset."

    user_failures = failures.groupby('user_id').size().to_frame(name='failure_count')

    quantile_val = user_failures['failure_count'].quantile(quantile_threshold)
    final_threshold = max(quantile_val, min_failures_threshold)

    anomalous_users = user_failures[user_failures['failure_count'] >= final_threshold].sort_values(by='failure_count', ascending=False)
    return anomalous_users, final_threshold, None

def get_anomalous_user_details(_df, anomalous_user_ids_list): # O argumento agora espera uma lista
    """
    Filtra o dataframe principal para obter os detalhes de atividade
    dos utilizadores anómalos.
    """
    if 'ip_address' not in _df.columns or 'device_type' not in _df.columns:
        return pd.DataFrame(), pd.DataFrame(), "Faltam 'ip_address' ou 'device_type' no dataset."

    # Filtra toda a atividade (sucessos e falhas) dos utilizadores suspeitos
    user_activity = _df[_df['user_id'].isin(anomalous_user_ids_list)]
    if user_activity.empty:
        return pd.DataFrame(), pd.DataFrame(), "Nenhuma atividade encontrada para estes utilizadores."

    # 1. IPs mais usados por este grupo (Top 10)
    top_ips = user_activity['ip_address'].value_counts().head(10).to_frame(name='Nº de Logins (Total)')

    # 2. Dispositivos mais usados por este grupo (Top 10)
    top_devices = user_activity['device_type'].value_counts().head(10).to_frame(name='Nº de Logins (Total)')

    return top_ips, top_devices, None # None para "sem erro"