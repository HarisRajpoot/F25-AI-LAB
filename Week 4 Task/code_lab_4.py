import heapq
roads = {
    "Gate": [("Lib", 2), ("Cafe", 3), ("Hall", 7), ("Gym", 4)],
    "Lib": [("Lab", 2)],
    "Lab": [("Hostel", 6)],
    "Cafe": [("Admin", 3)],
    "Admin": [("Hostel", 3)],
    "Hall": [("Hostel", 4)],
    "Gym": [("Pool", 2)],
    "Pool": [],
    "Hostel": []
}
guess = {"Gate": 7, "Lib": 5, "Lab": 5, "Cafe": 5, "Admin": 2, "Hall": 3, "Gym": 6, "Pool": 6, "Hostel": 0}
start = "Gate"
goal = "Hostel"
def find_route(graph, h, begin, end):
    queue = [(h[begin], 0, 0, begin, [begin])]
    counter = 1
    best = {begin: 0}
    log = []
    expanded = []
    stale = 0
    while queue:
        f, g, order, node, path = heapq.heappop(queue)
        if g > best[node]:
            stale += 1
            continue
        if node == end:
            log.append((node, g, h[node], f, "goal reached"))
            return {"path": path, "cost": g, "log": log, "expanded": expanded, "stale": stale}
        expanded.append(node)
        for nxt, w in graph[node]:
            new_g = g + w
            if new_g < best.get(nxt, 10000):
                best[nxt] = new_g
                heapq.heappush(queue, (new_g + h[nxt], new_g, counter, nxt, path + [nxt]))
                counter += 1
        waiting = []
        for item in sorted(queue):
            if item[1] == best[item[3]]:
                waiting.append(item[3] + "(g=" + str(item[1]) + ",f=" + str(item[0]) + ")")
        log.append((node, g, h[node], f, ", ".join(waiting)))
    return {"path": None, "cost": None, "log": log, "expanded": expanded, "stale": stale}
def add_edges(graph, path):
    total = 0
    for i in range(len(path) - 1):
        for nxt, w in graph[path[i]]:
            if nxt == path[i + 1]:
                total = total + w
    return total
def show(title, res):
    print("RUN:", title)
    print("No. | Node   | g | h | f  | Frontier after this step")
    for i, row in enumerate(res["log"], 1):
        print(f"{i:<3} | {row[0]:<6} | {row[1]} | {row[2]} | {row[3]:<2} | {row[4]}")
    if res["path"] is None:
        print("Result: no path found")
    else:
        print("Path:", " -> ".join(res["path"]))
        print("Returned cost:", res["cost"], "| Cost added by hand:", add_edges(roads, res["path"]))
    print("Processed nodes:", [row[0] for row in res["log"]])
    print("Expanded nodes:", res["expanded"])
    print("Expansion count:", len(res["expanded"]), "| Stale entries skipped:", res["stale"])
    print()
zero = {node: 0 for node in roads}
print("HEURISTIC AUDIT")
print("Node   | h | True remaining cost | Admissible")
for node in roads:
    r = find_route(roads, zero, node, goal)
    true_cost = r["cost"]
    if true_cost is None:
        print(f"{node:<6} | {guess[node]} | cannot reach goal  | yes")
    else:
        print(f"{node:<6} | {guess[node]} | {true_cost:<19} | {'yes' if guess[node] <= true_cost else 'NO'}")
print("Edge          | h(u) | cost + h(v) | Consistent")
for u in roads:
    for v, w in roads[u]:
        print(f"{u + '->' + v:<13} | {guess[u]:<4} | {w + guess[v]:<11} | {'yes' if guess[u] <= w + guess[v] else 'NO'}")
print()
astar = find_route(roads, guess, start, goal)
show("A* with given heuristic", astar)
ucs = find_route(roads, zero, start, goal)
show("UCS (all h = 0)", ucs)
over1 = dict(guess)
over1["Admin"] = 9
print("Changed h(Admin) from", guess["Admin"], "to", over1["Admin"])
r1 = find_route(roads, over1, start, goal)
show("A* with h(Admin) = 9", r1)
over2 = dict(guess)
over2["Hall"] = 20
print("Changed h(Hall) from", guess["Hall"], "to", over2["Hall"])
r2 = find_route(roads, over2, start, goal)
show("A* with h(Hall) = 20", r2)
print("EDGE CASES")
same = find_route(roads, guess, "Gate", "Gate")
print("Start equals goal:", same["path"], same["cost"], "expansions:", len(same["expanded"]))
none = find_route(roads, guess, "Gate", "Pool")
print("Goal is Pool:", none["path"], none["cost"])
blocked = find_route(roads, guess, "Pool", "Hostel")
print("Start Pool, goal Hostel:", blocked["path"], blocked["cost"])
print()
print("SUMMARY")
print("Run                  | Path                            | Cost | Expansions")
for name, r in [("A* given h", astar), ("UCS h=0", ucs), ("A* h(Admin)=9", r1), ("A* h(Hall)=20", r2)]:
    print(f"{name:<20} | {' -> '.join(r['path']):<31} | {r['cost']:<4} | {len(r['expanded'])}")
