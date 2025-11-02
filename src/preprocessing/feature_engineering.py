# Engenharia de Recursos
import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria novas características a partir do DataFrame fornecido.

    Parâmetros:
    df (pd.DataFrame): DataFrame original com os dados brutos.

    Retorna:
    pd.DataFrame: DataFrame com novas características adicionadas.
    """
    # É uma boa prática não modificar o DataFrame original
    df_copy = df.copy()

    # ==============================
    # 1. PRÉ-PROCESSAMENTO
    # ==============================

    # Converter 'timestamp' para datetime
    df_copy['timestamp'] = pd.to_datetime(df_copy['timestamp'])

    # Ordenar valores (crítico para diff e shift)
    df_copy = df_copy.sort_values(by=['user_id', 'timestamp'])

    # ==============================
    # 2. Features baseadas em tempo
    # ==============================

    # Hora do dia
    df_copy['hour_of_day'] = df_copy['timestamp'].dt.hour

    # Dia da semana
    df_copy['day_of_week'] = df_copy['timestamp'].dt.dayofweek

    # Sábado ou domingo (convertido para 0 ou 1)
    df_copy['is_weekend'] = df_copy['day_of_week'].isin([5, 6]).astype(int)

    # Parte do dia - (Usando bins mais robustos)
    df_copy['time_of_day'] = pd.cut(
        df_copy['hour_of_day'],
        bins=[-1, 5, 11, 17, 23], # (0-5), (6-11), (12-17), (18-23)
        labels=['Madrugada', 'Manhã', 'Tarde', 'Noite'],
        right=True
    )

    # ===============================
    # 3. Features comportamentais
    # ==============================

    # Tempo desde o último login
    df_copy['time_since_last_login'] = df_copy.groupby('user_id')['timestamp'].diff().dt.total_seconds()
    
    # Frequência de login - Número de logins nas últimas 24 horas
    # (CORREÇÃO: Requer indexação de tempo para a janela '24h')
    df_indexed = df_copy.set_index('timestamp')
    rolling_count = df_indexed.groupby('user_id')['login_id'].transform(
        lambda x: x.rolling('24h').count()
    )
    df_copy['login_frequency_24h'] = rolling_count.values

    # País novo - Indica se o país do login é diferente do último país registrado

    df_copy['is_new_country'] = df_copy.groupby('user_id')['country'].transform(
        lambda x: (x != x.shift(1)).astype(int)
    )

    # Dispositivo novo - Indica se o dispositivo do login é diferente do último dispositivo registrado
    df_copy['is_new_device'] = df_copy.groupby('user_id')['device_type'].transform(
        lambda x: (x != x.shift(1)).astype(int)
    )

    # Mudança de metodo de autenticação - Indica se o método de autenticação mudou em relação ao último login
    df_copy['auth_method_changed'] = df_copy.groupby('user_id')['auth_method'].transform(
        lambda x: (x != x.shift(1)).astype(int)
    )

    # Metodo de autenticação - Codifica o método de autenticação utilizado
    df_copy = pd.get_dummies(df_copy, columns=['auth_method'], prefix='auth_method')

    # ==============================
    # 4. Features de risco e contexto
    # ==============================

    # Ip subnet - Extrai a sub-rede do endereço IP
    df_copy['ip_subnet'] = df_copy['ip_address'].apply(lambda x: '.'.join(x.split('.')[:3]))
    
    # Contagem de usuários por IP - Número de usuários únicos que usaram o mesmo IP
    df_copy['user_count_per_ip'] = df_copy.groupby('ip_address')['user_id'].transform('nunique')
    
    # Desvio da duração do login - Mede a variação da duração do login em relação à média
    df_copy['desvio_duracao_login'] = df_copy.groupby('user_id')['login_duration_sec'].transform(
        lambda x: (x - x.mean()).abs()
    )

    # Desvio da latência - Mede a variação da latência em relação à média
    df_copy['desvio_latencia'] = df_copy.groupby('user_id')['latency_ms'].transform(
        lambda x: (x - x.mean()).abs()
    )

    return df_copy