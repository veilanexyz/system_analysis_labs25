import math
from typing import List, Tuple, Dict, Set
from task1 import main as _calculate_relations

def _calculate_binary_entropy(p: float) -> float:
    if p == 0.0 or p == 1.0:
        return 0.0
    return - (p * math.log2(p) + (1 - p) * math.log2(1 - p))

def main(s: str, e: str) -> Tuple[float, float]:
    matrices = _calculate_relations(s, e)
    if not matrices or not matrices[0]:
        return (0.0, 0.0)
    n = len(matrices[0])
    if n == 0:
        return (0.0, 0.0) 
    n_squared = n * n
    total_entropy = 0.0
    for matrix in matrices:
        k = 0
        for row in matrix:
            k += sum(row) 
        if n_squared > 0:
            p = k / n_squared
        else:
            p = 0.0
        total_entropy += _calculate_binary_entropy(p)
    h_max = 5.0
    if h_max > 0:
        h_norm = total_entropy / h_max
    else:
        h_norm = 0.0
    return (round(total_entropy, 1), round(h_norm, 1))