from priorityQueue import PriorityQueue


# Trace the path from the source to the target using the nodeInfo dictionary (representing the search tree) from the A* search
def tracePath(artistSearchNodes, targetId):
    path = []
    current = targetId
    while current is not None:
        path.append(current)
        current = artistSearchNodes[current].parent
    return path

# Calculate the heuristic value for a node
# The heuristic value is the number of genres in common with the target node divided by the total number of genres plus the popularity of the node multiplied negatively by 1


def artistProximityHeuristic(src, targetGenreMap):
    sameGenres = 0
    for genre in src['genres']:
        if genre in targetGenreMap:
            sameGenres += 1
    sameGenres = 0 if len(
        targetGenreMap) == 0 else sameGenres / len(targetGenreMap)
    return sameGenres + src['popularity']

# Class to represent a node in the A* search tree


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

# Run an A* search on the graph


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
