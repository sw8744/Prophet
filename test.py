# 순열 사이클!!
from collections import deque


# start num =1
def find(graph, start_num):
    global N
    while start_num <= N:

        queue = deque()

        if len(graph[start_num]) == 0:
            find(graph, start_num + 1)
        else:
            print(start_num)
            print(graph[start_num][0])
            queue.append(graph[start_num][0])

        print(queue)
        v = queue.popleft()

        if len(graph[v]) == 0 or graph[v][0] in graph[start_num]:
            start_num += 1
            find(graph, start_num)

        print(v, start_num)
        if graph[v][0] not in graph[start_num]:
            graph[start_num].append(graph[v][0])
            queue.append(graph[v][0])
            graph[v] = []

    k = 0
    for i in range(1, N + 1):
        if len(graph[i]) > 0:
            k += 1
    return k


T = int(input())

for _ in range(T):
    N = int(input())
    x = list(map(int, input().split()))
    x.insert(0, 0)

    graph = []
    for _ in range(N + 1):
        graph.append([])
    for i in range(1, N + 1):
        graph[i].append(x[i])
    print(find(graph, 1))