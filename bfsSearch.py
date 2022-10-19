from collections import deque


def tracePath(visited, targetId):
    path = []
    current = targetId
    while current is not None:
        path.append(current)
        current = visited[current]['parent']
    return path


def bfsSearch(artistsNodes, sourceId, targetId):
    steps = 0
    visited = {}
    queue = deque()
    queue.append(sourceId)

    visited[sourceId] = {
        'parent': None,
    }

    while len(queue) > 0:
        steps += 1
        current = queue.popleft()

        if current == targetId:
            return tracePath(visited, targetId), steps

        for collab in artistsNodes[current]['collabs']:
            if collab not in visited:
                visited[collab] = {
                    'parent': current,
                }
                queue.append(collab)
    return None, steps
