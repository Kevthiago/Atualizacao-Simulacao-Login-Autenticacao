# src/preprocessing/feature_engineering.py
import pandas as pd
import numpy as np

# =============================================================================
# FUNÇÃO 1: CRIAR FEATURES
# =============================================================================

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

# =============================================================================
# FUNÇÃO 2: PRÉ-PROCESSAMENTO FINAL (PASSO 1 e 2)
# =============================================================================

def preprocess_for_model(df_featured: pd.DataFrame) -> pd.DataFrame:
    """
    Executa o pré-processamento final: trata NaNs da engenharia de features,
    faz o encoding final e remove colunas desnecessárias.
    """
    print("Executando pré-processamento final (Tratando NaNs, Encoding, Drop)...")
    
    # --- PASSO 1: TRATAMENTO DE NaNs ---
    # (Trata os NaNs criados por .diff(), .shift() e .rolling())
    df_processed = df_featured.copy()
    
    # Preencher time_since_last_login com -1 (para diferenciar de 0 segundos)
    df_processed['time_since_last_login'] = df_processed['time_since_last_login'].fillna(-1)
    
    # Preencher login_frequency_24h com 1 (primeiro login na janela)
    df_processed['login_frequency_24h'] = df_processed['login_frequency_24h'].fillna(1)
    
    # Preencher colunas 'is_new' e desvios com 0 (primeiro login não é "novo" e não tem "desvio")
    cols_to_fill_zero = ['is_new_country', 'is_new_device', 'auth_method_changed', 
                         'desvio_duracao_login', 'desvio_latencia']
    df_processed[cols_to_fill_zero] = df_processed[cols_to_fill_zero].fillna(0)

    # --- PASSO 2: ENCODING E LIMPEZA DE COLUNAS ---
    
    # Colunas a serem removidas (identificadores, dados brutos, leaks)
    cols_to_drop = ['login_id', 'user_id', 'username', 'timestamp', 
                    'ip_address', 'session_duration_min']
    
    # Checar se as colunas existem antes de dropar (para evitar erros)
    cols_existentes_para_dropar = [col for col in cols_to_drop if col in df_processed.columns]
    df_processed = df_processed.drop(columns=cols_existentes_para_dropar)

    # Colunas categóricas que ainda precisam de encoding
    categorical_cols = ['device_type', 'browser', 'os', 'country', 
                        'time_of_day', 'ip_subnet']
    
    # Checar se as colunas existem antes de fazer o encoding
    cols_existentes_para_encode = [col for col in categorical_cols if col in df_processed.columns]
    
    df_model_ready = pd.get_dummies(df_processed, columns=cols_existentes_para_encode, drop_first=True)

    # Garantir que TUDO seja numérico (converter colunas bool de get_dummies para 1/0)
    for col in df_model_ready.columns:
        if df_model_ready[col].dtype == 'bool':
            df_model_ready[col] = df_model_ready[col].astype(int)
            
    return df_model_ready