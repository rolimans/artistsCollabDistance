from priorityQueue import PriorityQueue


def tracePath(artistSearchNodes, targetId):
    path = []
    current = targetId
    while current is not None:
        path.append(current)
        current = artistSearchNodes[current].parent
    return path


def artistProximityHeuristic(src, targetGenreMap):
    sameGenres = 0
    for genre in src['genres']:
        if genre in targetGenreMap:
            sameGenres += 1
    sameGenres = 0 if len(
        targetGenreMap) == 0 else sameGenres / len(targetGenreMap)
    return sameGenres + src['popularity']


class SearchNode():
    def __init__(self, artistId=None, parent=None,):
        self.parent = parent
        self.artistId = artistId
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.artistId == other.artistId

    def __lt__(self, other):
        return self.artistId < other.artistId


def aStarSearch(artistsNodes, sourceId, targetId):
    steps = 0

    targetGenreMap = {
        genre: True for genre in artistsNodes[targetId]['genres']}

    closedList = {}
    openList = PriorityQueue()
    artistSearchNodes = {}

    sourceNode = SearchNode(sourceId)
    artistSearchNodes[sourceId] = sourceNode
    openList.put(sourceNode, sourceNode.f)

    while not openList.empty():

        current = openList.get()

        if closedList.get(current.artistId, False):
            continue

        steps += 1

        if current.artistId == targetId:
            return tracePath(artistSearchNodes, targetId), steps

        closedList[current.artistId] = True

        for collab in artistsNodes[current.artistId]['collabs']:
            if collab not in closedList:
                newNode = SearchNode(collab, current.artistId)
                newNode.g = current.g + 1
                newNode.h = - artistProximityHeuristic(
                    artistsNodes[collab], targetGenreMap)
                newNode.f = newNode.g + newNode.h
                if(collab not in artistSearchNodes or artistSearchNodes[collab].f > newNode.f):
                    artistSearchNodes[collab] = newNode
                    openList.put(newNode, newNode.f)
    return None, steps
