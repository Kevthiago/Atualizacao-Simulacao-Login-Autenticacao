def compute_kpis(df):
    kpis = {
        'total_logins': len(df),
        'success_rate': df['login_success'].mean() if 'login_success' in df.columns else None,
        'fail_rate': 1 - df['login_success'].mean() if 'login_success' in df.columns else None,
        'unique_users': df['user_id'].nunique() if 'user_id' in df.columns else None,
        'unique_ips': df['ip_address'].nunique() if 'ip_address' in df.columns else None,
        'avg_login_duration_s': df['login_duration_sec'].mean() if 'login_duration_sec' in df.columns else None
    }
    return kpis