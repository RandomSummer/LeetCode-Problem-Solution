class Solution {
    public int minCost(int n, int[][] edges) {
        // adjacency list for normal edges 
        List<int[]> [] graph = new ArrayList[n];
        // incoming edges to enable reverse option 
        List<int[]> [] incoming = new ArrayList[n];

        for (int i=0; i<n; i++) {
            graph[i] = new ArrayList<>();
            incoming[i] = new ArrayList<>();
        }

        // build graph 
        for (int[] e:edges) {
            int u = e[0], v = e[1], w = e[2];
            graph[u].add(new int[]{v, w});
            incoming[v].add(new int[]{u, w}); // store incoming for reverse
        }

        // Dijkstra's algorithm
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;

        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
        pq.offer(new int[]{0, 0}); // node, cost
        
        boolean[] usedSwitch = new boolean[n];

        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int u = cur[0], cost = cur[1];

            if (u == n-1) return cost;
            if (cost > dist[u]) continue;

            for (int[] e:graph[u]) {
                int v = e[0], w = e[1];
                if (cost + w < dist[v]) {
                    dist[v] = cost + w;
                    pq.offer(new int[]{v, dist[v]});
                }
            }
            if (!usedSwitch[u]) {
                usedSwitch[u] = true;
                for (int[] e:incoming[u]) {
                    int prev = e[0], w = e[1];
                    int newCost = cost + 2 * w;
                    if (newCost < dist[prev]) {
                        dist[prev] = newCost;
                        pq.offer(new int[]{prev, newCost});
                    }
                }
            }
        }
        return -1;
    }
}