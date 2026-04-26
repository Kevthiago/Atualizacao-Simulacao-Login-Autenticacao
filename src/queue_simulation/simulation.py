import simpy
import random
import numpy as np 

# =======================================================
# SEÇÃO 2 - SIMULAÇÃO SIMPY (COM BURSTS)
# =======================================================

def estimate_arrival_rate(df):
    df = df.dropna(subset=['timestamp'])
    if len(df) < 2: return 0.0001
    ts_min, ts_max = df['timestamp'].min(), df['timestamp'].max()
    sec = (ts_max - ts_min).total_seconds()
    return len(df) / sec if sec > 0 else 0.0001

def estimate_service_time(df, mode='exp'):
    values = df['login_duration_sec'].dropna().values
    if len(values) == 0: return 1.0
    return float(np.median(values)) if mode=='exp' else values

def generate_bursts(run_time, n_bursts=2, duration=60, mult=3, seed=42):
    random.seed(seed)
    bursts = []
    if run_time <= duration:
        return []
    for _ in range(n_bursts):
        start = random.uniform(0, run_time - duration)
        bursts.append((start, start+duration, mult))
    return bursts

class AuthSystemSim:
    def __init__(self, env, servers, service_src, mode):
        self.env = env
        self.server = simpy.Resource(env, capacity=servers)
        self.service_src = service_src
        self.mode = mode
        self.wait_times = []
        self.total = 0

    def service_time(self):
        if self.mode == 'exp':
            m = float(self.service_src)
            return random.expovariate(1/m) if m > 0 else 0
        return float(np.random.choice(self.service_src))

    def process(self, _):
        arrival = self.env.now
        with self.server.request() as req:
            yield req
            self.wait_times.append(self.env.now - arrival)
            yield self.env.timeout(self.service_time())
            self.total += 1

def arrival_process(env, system, λ, runtime, bursts):
    λ_max = λ * max([m for _,_,m in bursts] + [1])
    if λ_max <= 0:
        return
    while env.now < runtime:
        interarrival = random.expovariate(λ_max)
        yield env.timeout(interarrival)
        if env.now >= runtime:
            break
        mult = 1
        for start,end,m in bursts:
            if start <= env.now <= end:
                mult = m
                break
        if random.random() <= (λ*mult)/λ_max:
            env.process(system.process(None))

def run_sim(servers, runtime, bursts_tuple, λ, m_service):
    bursts = list(bursts_tuple)
    env = simpy.Environment()
    s = AuthSystemSim(env, servers, m_service, 'exp')
    env.process(arrival_process(env, s, λ, runtime, bursts))
    env.run(until=runtime)
    return np.mean(s.wait_times or [0]), s.total