import csv
import re
import sys
import random
import json
from datetime import datetime
from bfsSearch import bfsSearch
from aStarSearch import aStarSearch
import matplotlib.pyplot as plt
from pyvis.network import Network

# Parses the CSV file and returns a list of objects with the keys being the column names


def parseCsv(filename):
    content = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(reader)
        for row in reader:
            data = {}
            for i in range(len(header)):
                data[header[i]] = row[i]
            content.append(data)
    return content

# Removes artists with same name, keeps the most popular one


def removeArtistDuplicates(artists):
    artistsMap = {}
    for artist in artists:
        if artist['name'] not in artistsMap or artist['popularity'] > artistsMap[artist['name']]['popularity']:
            artistsMap[artist['name']] = artist
    return list(artistsMap.values())


# Map artists list and collabs list to a dictionary of nodes with the key being the artist id and the value being the artist object
# The artist object contains the artist name, popularity, a list of genres and a list of collabs
def artistsToNodes(artists, collabs):
    nodes = {}
    for artist in artists:
        nodes[artist['spotify_id']] = {
            'id': artist['spotify_id'],
            'name': artist['name'],
            'popularity': int(artist['popularity'])/100,
            'genres': [genre[1:-1]
                       for genre in re.findall("\".*\"|\'[^']*\'", artist['genres'])],
            'collabs': []
        }
    for collab in collabs:
        id0 = collab['id_0']
        id1 = collab['id_1']
        if id0 in nodes and id1 in nodes:
            nodes[id0]['collabs'].append(id1)
            nodes[id1]['collabs'].append(id0)
    return {k: v for k, v in nodes.items() if len(v['collabs']) > 0}


# Given a map of nodes, returns a map of degrees with the key being the degree and the value being the number of nodes with that degree
def getDegreeDistribution(nodes):
    degrees = {}
    for node in nodes.values():
        degree = len(node['collabs'])
        if degree not in degrees:
            degrees[degree] = 0
        degrees[degree] += 1
    dgs = sorted(degrees.keys())

    return {dg: degrees[dg] for dg in dgs}

# Given a map of nodes and a number x, runs x experiments finding a path between two random nodes using BFS and A* and returns a map with the key being a node id and value being a map with keys being the other node id and value being a dictionary with the experiment results
# Each experiment result contains the shortest path length between the two nodes, the path length found by BFS and A* and the steps taken to find a path by BFS and A*


def runExperiments(nodes, x):
    n = 1
    experiments = {}
    while n <= x:
        src = random.choice(list(nodes.keys()))
        dst = random.choice(list(nodes.keys()))

        if experiments.get(src, {}).get(dst, None) is not None:
            continue

        if experiments.get(dst, None) is None:
            experiments[dst] = {}

        print("Running experiment " + str(n) + " of " + str(x))

        bfsPath, bfsSteps = bfsSearch(nodes, src, dst)
        aStarPath, aStarSteps = aStarSearch(nodes, src, dst)

        bfsPath = len(bfsPath) if bfsPath is not None else -1
        aStarPath = len(aStarPath) if aStarPath is not None else -1

        minPathSize = min(bfsPath, aStarPath)

        experiments[dst][src] = {
            'minPathSize': minPathSize,
            'src': nodes[src].get('name', src),
            'dst': nodes[dst].get('name', dst),
            'bfs': {
                'pathSize': bfsPath,
                'steps': bfsSteps
            },
            'aStar': {
                'pathSize': aStarPath,
                'steps': aStarSteps
            }
        }

        n += 1
    return experiments


artists = removeArtistDuplicates(parseCsv('data/artists.csv'))
collabs = parseCsv('data/collabs.csv')

artistsNodes = artistsToNodes(artists, collabs)
nameIdMap = {v['name']: k for k, v in artistsNodes.items()}


# If no arguments are passed, run a search between nodes entered by the user
# Otherwise run other posible modes: analyze degree distribution, run experiments, plot results of experiments and plot the graph
mode = 'search'

try:
    if sys.argv[1] == 'analyze':
        if sys.argv[2] == 'degree':
            mode = 'analyze-degree'
        elif sys.argv[2] == 'efficiency':
            mode = 'analyze-efficiency'
    elif sys.argv[1] == 'plot':
        if sys.argv[2] == 'efficiency':
            mode = 'plot-efficiency'
        elif sys.argv[2] == 'graph':
            mode = 'plot-graph'
except:
    mode = 'search'

if mode == 'search':

    sourceArtist = input('Insira o nome do artista de origem: ')
    targetArtist = input('Insira o nome do artista de destino: ')
    algorithm = input('Insira o algoritmo a ser utilizado (bfs ou aStar): ')

    print()

    if algorithm not in ['bfs', 'aStar']:
        print('Algoritmo inválido')
        exit(1)

    sourceId = nameIdMap.get(sourceArtist, None)
    targetId = nameIdMap.get(targetArtist, None)

    if sourceId is None:
        print(f'O artista {sourceArtist} não foi encontrado')
        exit(1)

    if targetId is None:
        print(f'O artista {targetArtist} não foi encontrado')
        exit(1)

    path, steps = aStarSearch(artistsNodes, sourceId, targetId) if algorithm == 'aStar' else bfsSearch(
        artistsNodes, sourceId, targetId)

    print(f'Artistas percorridos: {steps}')

    if path is None:
        print(
            f'Não foi possível encontrar caminho de colaborações entre {sourceArtist} e {targetArtist}')
        exit(1)

    print(f'Tamanho do caminho: {len(path)-1}')
    print(f'Caminho de colaborações entre {sourceArtist} e {targetArtist}:')
    for artistIdx in range(0, len(path)):
        artistName = artistsNodes[path[artistIdx]]['name']
        if artistIdx > 1:
            print(' que', end='')
        if artistIdx > 0:
            print(' colaborou com ', end='')
        print(artistName, end='')
    print('.')
elif mode == 'analyze-degree':
    degrees = getDegreeDistribution(artistsNodes)
    plt.plot(degrees.keys(), degrees.values())
    plt.title('Distribuição de graus')
    plt.xlabel('Grau')
    plt.ylabel('Número de artistas')
    plt.show()
elif mode == 'analyze-efficiency':
    if len(sys.argv) < 4:
        print('Número de experimentos não especificado')
        exit(1)
    nExperiments = int(sys.argv[3])
    experiments = runExperiments(artistsNodes, nExperiments)
    filename = datetime.now().strftime("%d-%m-%Y %H-%M-%S") + '.json'

    with open('experiments/'+filename, 'w') as f:
        json.dump(experiments, f)
elif mode == 'plot-efficiency':
    if len(sys.argv) < 4:
        print('Nome do arquivo de experimentos não especificado')
        exit(1)
    filename = sys.argv[3]
    with open(filename, 'r') as f:
        experiments = json.load(f)

    minPathSizes = []
    bestInSteps = {
        'bfs': [],
        'aStar': [],
        'equal': 0
    }

    bestInSize = {
        'bfs': 0,
        'aStar': 0,
        'equal': 0
    }

    foundMap = {
        'found': 0,
        'notFound': 0
    }

    for dst in experiments.values():
        for src in dst.values():
            if src['minPathSize'] != -1:
                foundMap['found'] += 1
                minPathSizes.append(src['minPathSize'])
                if src['bfs']['pathSize'] < src['aStar']['pathSize']:
                    bestInSize['bfs'] += 1
                elif src['aStar']['pathSize'] < src['bfs']['pathSize']:
                    bestInSize['aStar'] += 1
                else:
                    bestInSize['equal'] += 1
                if src['bfs']['steps'] < src['aStar']['steps']:
                    bestInSteps['bfs'].append(
                        src['aStar']['steps'] - src['bfs']['steps'])
                elif src['aStar']['steps'] < src['bfs']['steps']:
                    bestInSteps['aStar'].append(
                        src['bfs']['steps'] - src['aStar']['steps'])
                else:
                    bestInSteps['equal'] += 1
            else:
                foundMap['notFound'] += 1

    print(f'Número de experimentos: {sum(foundMap.values())}')
    print(
        f'Número de experimentos com caminho encontrado: {foundMap["found"]}')
    print(
        f'Número de experimentos sem caminho encontrado: {foundMap["notFound"]}')
    print(
        f'Média do tamanho do menor caminho: {sum(minPathSizes)/len(minPathSizes)}')
    print(
        f'Número de vezes que BFS encontrou caminho menor: {bestInSize["bfs"]}')
    print(
        f'Número de vezes que A* encontrou caminho menor: {bestInSize["aStar"]}')
    print(
        f'Número de vezes que os dois algoritmos encontraram caminho do mesmo tamanho: {bestInSize["equal"]}')
    print(
        f'Número de vezes que BFS encontrou caminho em menos passos: {len(bestInSteps["bfs"])}')
    print(
        f'BFS encontrou o caminho em menos passos {(len(bestInSteps["bfs"])/foundMap["found"])*100}% das vezes.')
    print(
        f'Número de vezes que A* encontrou caminho em menos passos: {len(bestInSteps["aStar"])}')
    print(
        f'A* encontrou o caminho em menos passos {(len(bestInSteps["aStar"])/foundMap["found"])*100}% das vezes.')
    print(
        f'Número de vezes que os dois algoritmos encontraram caminho em igual número de passos: {bestInSteps["equal"]}')
    print(
        f'Média de passos a menos que BFS encontrou caminho quando foi o mais rápido: {sum(bestInSteps["bfs"])/len(bestInSteps["bfs"])}')
    print(
        f'Média de passos a menos que A* encontrou caminho quando foi o mais rápido: {sum(bestInSteps["aStar"])/len(bestInSteps["aStar"])}')

    plt.hist(minPathSizes, bins=range(0, max(minPathSizes)+1))
    plt.xticks(range(0, max(minPathSizes)+1))
    plt.title('Distribuição de tamanhos de caminhos mínimos')
    plt.xlabel('Tamanho do caminho mínimo')
    plt.ylabel('Número de pares de artistas')
    plt.show()

    plt.bar(bestInSize.keys(), bestInSize.values())
    plt.title(
        'Vezes que um algoritmo encontrou o caminho menor')
    plt.xlabel('Algoritmo')
    plt.ylabel('Número de pares de artistas')
    plt.show()

    plt.bar(bestInSteps.keys(), [len(x) if type(x)
            == list else x for x in bestInSteps.values()])
    plt.title('Vezes que um algoritmo encontrou o caminho em menos passos')
    plt.xlabel('Algoritmo')
    plt.ylabel('Número de pares de artistas')
    plt.show()

    plt.bar(foundMap.keys(), foundMap.values())
    plt.title('Vezes que um caminho foi encontrado')
    plt.xlabel('Caminho encontrado')
    plt.ylabel('Número de pares de artistas')
    plt.show()

    plt.hist([bestInSteps['bfs'], bestInSteps['aStar']], label=['BFS', 'A*'])
    plt.legend(loc='upper right')

    plt.title('Diferença de passos entre o melhor algoritmo e o pior')

    plt.xlabel('Diferença de passos')
    plt.ylabel('Número de pares de artistas')
    plt.show()
elif mode == 'plot-graph':

    if len(sys.argv) < 4:
        print('Números de nós não especificado')
        exit(1)

    nNodes = int(sys.argv[3])

    addedArtists = {}
    net = Network(height='100vh', width='100vw',)

    while nNodes > 0:
        artist = random.choice(artists)
        if artist['spotify_id'] in addedArtists:
            continue
        addedArtists[artist['spotify_id']] = True
        net.add_node(artist['spotify_id'], artist['name'])
        nNodes -= 1

    for collab in collabs:
        artist0 = collab['id_0']
        artist1 = collab['id_1']

        if artist1 in addedArtists and artist0 in addedArtists:
            net.add_edge(artist0, artist1)

    net.toggle_physics(True)
    net.show('graph.html')
