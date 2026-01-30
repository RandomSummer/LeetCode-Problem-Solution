from typing import List
import heapq
from collections import defaultdict

INF = 10**18

class Solution:
    def minimumCost(
        self,
        source: str,
        target: str,
        original: List[str],
        changed: List[str],
        cost: List[int]
    ) -> int:
        n = len(source)
        if n != len(target):
            return -1

        # Group conversion rules by substring length
        rules_by_len = defaultdict(list)
        for o, c, w in zip(original, changed, cost):
            if len(o) == len(c):
                rules_by_len[len(o)].append((o, c, w))

        lengths = sorted(rules_by_len.keys())
        if not lengths:
            return 0 if source == target else -1

        # Build graph for each length L: strings -> ids, adjacency list
        graphs = {}  # L -> (id_map, adj, V)
        for L in lengths:
            id_map = {}
            def get_id(s: str) -> int:
                if s not in id_map:
                    id_map[s] = len(id_map)
                return id_map[s]

            # Keep minimum edge cost per (u,v)
            best_edge = {}
            for o, c, w in rules_by_len[L]:
                u = get_id(o)
                v = get_id(c)
                key = (u, v)
                if key not in best_edge or w < best_edge[key]:
                    best_edge[key] = w

            adj = defaultdict(list)
            for (u, v), w in best_edge.items():
                adj[u].append((v, w))

            graphs[L] = (id_map, adj, len(id_map))

        # Cache Dijkstra results: dist_cache[L][start_id] = dist_array
        dist_cache = {}

        for L in lengths:
            id_map, adj, V = graphs[L]

            # We'll run Dijkstra only from needed source-substrings
            starts = set()
            for i in range(0, n - L + 1):
                sseg = source[i:i+L]
                tseg = target[i:i+L]
                if sseg == tseg:
                    continue
                if sseg in id_map and tseg in id_map:
                    starts.add(id_map[sseg])

            def dijkstra(start: int):
                dist = [INF] * V
                dist[start] = 0
                pq = [(0, start)]
                while pq:
                    d, u = heapq.heappop(pq)
                    if d != dist[u]:
                        continue
                    for v, w in adj.get(u, []):
                        nd = d + w
                        if nd < dist[v]:
                            dist[v] = nd
                            heapq.heappush(pq, (nd, v))
                return dist

            dist_cache[L] = {}
            for st in starts:
                dist_cache[L][st] = dijkstra(st)

        # DP: dp[i] = min cost to convert source[0:i] -> target[0:i]
        dp = [INF] * (n + 1)
        dp[0] = 0

        for i in range(n):
            if dp[i] == INF:
                continue

            # move 1 char if already equal
            if source[i] == target[i]:
                dp[i+1] = min(dp[i+1], dp[i])

            # try convert a segment starting at i with each allowed length L
            for L in lengths:
                j = i + L
                if j > n:
                    break

                sseg = source[i:j]
                tseg = target[i:j]

                if sseg == tseg:
                    dp[j] = min(dp[j], dp[i])
                    continue

                id_map, _, _ = graphs[L]
                if sseg not in id_map or tseg not in id_map:
                    continue

                sid = id_map[sseg]
                tid = id_map[tseg]

                if sid not in dist_cache[L]:
                    continue

                cst = dist_cache[L][sid][tid]
                if cst == INF:
                    continue

                dp[j] = min(dp[j], dp[i] + cst)

        return -1 if dp[n] == INF else dp[n]
