# =======================================================
# SEÇÃO 1 - TEORIA DE FILAS (M/M/c)
# =======================================================

import math


class MMCQueue:
    def __init__(self, arrival_rate, service_rate, servers):
        self.lambda_ = arrival_rate
        self.mu = service_rate
        self.c = servers

    def utilization(self):
        if self.c == 0 or self.mu == 0:
            return float('inf') if self.lambda_ > 0 else 0.0
        return self.lambda_ / (self.c * self.mu)

    def _p0(self):
        rho = self.utilization()
        c = self.c
        if rho >= 1:
            return 0.0
        try:
            sum_terms = sum((c * rho) ** n / math.factorial(n) for n in range(c))
            last_term = ((c * rho) ** c) / (math.factorial(c) * (1 - rho))
            return 1 / (sum_terms + last_term)
        except (OverflowError, ValueError):
            return 0.0

    def avg_waiting_time_in_queue(self):
        rho = self.utilization()
        c = self.c
        if rho >= 1:
            return float('inf')
        p0 = self._p0()
        if p0 == 0.0:
             return float('inf')
        try:
            numerator = ((c * rho) ** c) * p0
            denominator = math.factorial(c) * (1 - rho) ** 2
            Lq = numerator / denominator
            return (Lq / self.lambda_) if self.lambda_ > 0 else 0.0
        except (OverflowError, ValueError):
            return float('inf')

    def avg_time_in_system(self):
        wq = self.avg_waiting_time_in_queue()
        if wq == float('inf') or self.mu == 0:
            return float('inf')
        return wq + (1 / self.mu)