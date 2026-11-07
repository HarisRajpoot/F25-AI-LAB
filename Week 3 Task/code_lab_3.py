from collections import deque
import heapq
graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["G"], "F": [], "G": []}
wgraph = {"A": [("B", 1), ("C", 2)], "B": [("D", 4), ("E", 1)], "C": [("F", 5), ("G", 10)], "D": [], "E": [("G", 1)], "F": [], "G": []}
def bfs(start, goal, g, show=False):
    queue = deque([(start, [start])])
    seen = {start}
    order = []
    step = 0
    while queue:
        node, path = queue.popleft()
        step += 1
        order.append(node)
        if node != goal:
            for nxt in g[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, path + [nxt]))
        if show:
            print(step, "|", node, "|", path, "|", [x[0] for x in queue])
        if node == goal:
            return path, order
    return None, order
def dfs(start, goal, g, show=False):
    stack = [(start, [start])]
    seen = set()
    order = []
    step = 0
    while stack:
        node, path = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        step += 1
        order.append(node)
        if node != goal:
            for nxt in reversed(g[node]):
                stack.append((nxt, path + [nxt]))
        if show:
            print(step, "|", node, "|", path, "|", [x[0] for x in stack])
        if node == goal:
            return path, order
    return None, order
def dls(node, goal, limit, path, g):
    if node == goal:
        return "FOUND", path
    if limit == 0:
        for child in g[node]:
            if child not in path:
                return "CUTOFF", None
        return "FAILURE", None
    cutoff = False
    for child in g[node]:
        if child in path:
            continue
        status, result = dls(child, goal, limit - 1, path + [child], g)
        if status == "FOUND":
            return status, result
        if status == "CUTOFF":
            cutoff = True
    if cutoff:
        return "CUTOFF", None
    return "FAILURE", None
def iddfs(start, goal, max_depth, g):
    tried = []
    for limit in range(max_depth + 1):
        status, path = dls(start, goal, limit, [start], g)
        tried.append(limit)
        print("  limit", limit, status, path)
        if status == "FOUND":
            return path, tried
    return None, tried
def ucs(start, goal, g):
    pq = [(0, start, [start])]
    best = {start: 0}
    order = []
    while pq:
        cost, node, path = heapq.heappop(pq)
        if cost > best[node]:
            continue
        order.append(node)
        if node == goal:
            return path, cost, order
        for nxt, w in g[node]:
            new_cost = cost + w
            if nxt not in best or new_cost < best[nxt]:
                best[nxt] = new_cost
                heapq.heappush(pq, (new_cost, nxt, path + [nxt]))
    return None, None, order
def path_cost(path, g):
    total = 0
    for i in range(len(path) - 1):
        for nxt, w in g[path[i]]:
            if nxt == path[i + 1]:
                total += w
    return total
print("TASK 1")
print("BFS trace: step | processed | path | queue after")
bfs_path, bfs_order = bfs("A", "G", graph, True)
print("BFS path:", bfs_path)
print("BFS visit order:", bfs_order)
print("DFS trace: step | processed | path | stack after")
dfs_path, dfs_order = dfs("A", "G", graph, True)
print("DFS path:", dfs_path)
print("DFS visit order:", dfs_order)
print()
print("TASK 2")
for limit in [1, 2, 3, 4]:
    print("DLS limit", limit, dls("A", "G", limit, ["A"], graph))
for m in [1, 2, 3, 4]:
    print("IDDFS max depth", m)
    path, tried = iddfs("A", "G", m, graph)
    print("  result:", path, "limits tried:", tried)
print()
print("TASK 3")
names = {k: [n for n, w in v] for k, v in wgraph.items()}
u_path, u_cost, u_order = ucs("A", "G", wgraph)
print("UCS path:", u_path)
print("UCS cost:", u_cost)
print("UCS processing order:", u_order)
print("UCS cost checked again:", path_cost(u_path, wgraph))
b_path, b_order = bfs("A", "G", names)
print("BFS path:", b_path)
print("BFS cost:", path_cost(b_path, wgraph))
print("BFS processing order:", b_order)
print("UCS hops:", len(u_path) - 1, "BFS hops:", len(b_path) - 1)
print()
print("EDGE CASES")
print("Start equals goal BFS:", bfs("A", "A", graph))
print("Start equals goal UCS:", ucs("A", "A", wgraph))
print("Unreachable goal BFS:", bfs("F", "G", graph))
print("Unreachable goal DFS:", dfs("F", "G", graph))
print("Unreachable goal UCS:", ucs("F", "G", wgraph))
cycle = {"A": ["B"], "B": ["C"], "C": ["A", "D"], "D": []}
print("Cycle graph BFS:", bfs("A", "D", cycle))
print("Cycle graph DFS:", dfs("A", "D", cycle))
print("Cycle graph DLS limit 2:", dls("A", "D", 2, ["A"], cycle))
print("Cycle graph DLS limit 3:", dls("A", "D", 3, ["A"], cycle))
