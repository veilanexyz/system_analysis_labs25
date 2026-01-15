from typing import List, Tuple, Dict, Set

def _get_all_descendants(start_node: str, adj: Dict[str, List[str]]) -> Set[str]:
    descendants = set()
    stack = list(adj.get(start_node, []))
    visited = {start_node}
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            descendants.add(node)
            for child in adj.get(node, []):
                if child not in visited:
                    stack.append(child)
    return descendants

def _parse_graph_data(s: str) -> Tuple[Dict[str, List[str]], List[str], Dict[str, int], int]:
    edges = []
    nodes = set()
    lines = s.strip().split('\n')
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) == 2:
            u, v = parts[0].strip(), parts[1].strip()
            edges.append((u, v))
            nodes.add(u)
            nodes.add(v)
    sorted_nodes = sorted(list(nodes))
    n = len(sorted_nodes)
    node_to_index = {node: i for i, node in enumerate(sorted_nodes)}
    adj = {node: [] for node in sorted_nodes}
    for u, v in edges:
        if u in adj:
            adj[u].append(v)
            
    return adj, sorted_nodes, node_to_index, n

def main(s: str, e: str) -> Tuple[	List[List[bool]],
                                	List[List[bool]],
                                	List[List[bool]],
                                	List[List[bool]],
                                	List[List[bool]]]:
    adj, sorted_nodes, node_to_index, n = _parse_graph_data(s)
    if n == 0:
        return ([], [], [], [], [])
    r1 = [[False] * n for _ in range(n)]
    r2 = [[False] * n for _ in range(n)]
    r3 = [[False] * n for _ in range(n)]
    r4 = [[False] * n for _ in range(n)]
    r5 = [[False] * n for _ in range(n)]

    for parent, children in adj.items():
        if not children:
            continue
            
        idx_p = node_to_index[parent]
        
        for child in children:
            idx_c = node_to_index[child]
            r1[idx_p][idx_c] = True
            r2[idx_c][idx_p] = True
 
        for i in range(len(children)):
            for j in range(i + 1, len(children)):
                child1 = children[i]
                child2 = children[j]
                idx_c1 = node_to_index[child1]
                idx_c2 = node_to_index[child2]
                r5[idx_c1][idx_c2] = True
                r5[idx_c2][idx_c1] = True

    for node in sorted_nodes:
        idx_node = node_to_index[node]
        all_descendants = _get_all_descendants(node, adj)
        direct_children = set(adj.get(node, []))
        mediated_descendants = all_descendants - direct_children
        for descendant in mediated_descendants:
            idx_desc = node_to_index[descendant]
            r3[idx_node][idx_desc] = True
            r4[idx_desc][idx_node] = True
            
    return (r1, r2, r3, r4, r5)