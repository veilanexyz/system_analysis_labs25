import json

def main(r1_json: str, r2_json: str) -> str:
    r1 = json.loads(r1_json)
    r2 = json.loads(r2_json)
    
    items = set()
    for group in r1:
        for x in group:
            items.add(x)
    for group in r2:
        for x in group:
            items.add(x)
    
    unique_items = sorted(list(items))
    n = len(unique_items)
    item_to_idx = {item: i for i, item in enumerate(unique_items)}
    
    def get_matrix(ranking):
        mat = [[0] * n for _ in range(n)]
        ranks = {}
        for r_idx, group in enumerate(ranking):
            for item in group:
                ranks[item] = r_idx
        
        for i in range(n):
            for j in range(n):
                u = unique_items[i]
                v = unique_items[j]
                rank_u = ranks.get(u, -1)
                rank_v = ranks.get(v, -1)
                
                if rank_u < rank_v:
                    mat[i][j] = 1
                elif rank_u > rank_v:
                    mat[i][j] = -1
                else:
                    mat[i][j] = 0
        return mat

    m1 = get_matrix(r1)
    m2 = get_matrix(r2)
    
    scores = []
    for i in range(n):
        row_sum = 0
        for j in range(n):
            if i == j:
                continue
            val = m1[i][j] + m2[i][j]
            row_sum += val
        scores.append((row_sum, unique_items[i]))
        
    scores.sort(key=lambda x: x[0], reverse=True)
    
    result_ranking = []
    if not scores:
        return json.dumps([])
        
    current_group = []
    current_score = scores[0][0]
    
    for score, item in scores:
        if score == current_score:
            current_group.append(item)
        else:
            result_ranking.append(sorted(current_group))
            current_group = [item]
            current_score = score
            
    if current_group:
        result_ranking.append(sorted(current_group))
        
    return json.dumps(result_ranking)