def solve(csv_text: str):
    rows = csv_text.strip().splitlines()
    edges = []
    for row in rows:
        a, b = row.split(',')
        edges.append((int(a), int(b)))

    n = 0
    for u, v in edges:
        if u > n:
            n = u
        if v > n:
            n = v

    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        matrix[u - 1][v - 1] = 1

    return tuple(tuple(row) for row in matrix)

def main(v: str):
    return solve(v)
