import json

def get_membership(value, points):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        
        if x1 <= value <= x2:
            if x1 == x2:
                return y1
            return y1 + (y2 - y1) * (value - x1) / (x2 - x1)
            
    if value < points[0][0]:
        return points[0][1]
    if value > points[-1][0]:
        return points[-1][1]
    return 0.0

def main(temp_mf_json: str, heat_mf_json: str, rules_json: str, current_temp: float) -> float:
    temp_mfs = json.loads(temp_mf_json)
    heat_mfs = json.loads(heat_mf_json)
    rules = json.loads(rules_json)
    
    temp_degrees = {}
    for term, points in temp_mfs.items():
        temp_degrees[term] = get_membership(current_temp, points)
        
    rule_activations = {}
    for temp_term, heat_term in rules.items():
        degree = temp_degrees.get(temp_term, 0.0)
        if heat_term in rule_activations:
            rule_activations[heat_term] = max(rule_activations[heat_term], degree)
        else:
            rule_activations[heat_term] = degree
            
    min_heat = float('inf')
    max_heat = float('-inf')
    for points in heat_mfs.values():
        for x, y in points:
            if x < min_heat: min_heat = x
            if x > max_heat: max_heat = x
            
    step = 0.1
    numerator = 0.0
    denominator = 0.0
    
    x = min_heat
    while x <= max_heat:
        max_y = 0.0
        
        for heat_term, activation in rule_activations.items():
            if activation > 0:
                mf_val = get_membership(x, heat_mfs[heat_term])
                clipped_val = min(mf_val, activation)
                if clipped_val > max_y:
                    max_y = clipped_val
        
        numerator += x * max_y
        denominator += max_y
        x += step
        
    if denominator == 0:
        return 0.0
        
    return numerator / denominator