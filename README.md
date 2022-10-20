# ArtistsCollabDistance

This is a project for the discipline of Artificial Intelligence - SCC0230 at ICMC - USP.

The goal of this project is to compare a uninformed search algorithm (BFS) with an informed search algorithm (A\*) in a problem of finding the shortest path between two artists in a graph of artists being the nodes and their collaborations being the edges.

The dataset used in this project consists of two CSV files, one containig ~156k artists and other containing 300k+ collaborations between them. The data was collected from Spotify and was obtained from [this Kaggle dataset](https://www.kaggle.com/datasets/jfreyberg/spotify-artist-feature-collaboration-network).

## Students:

- Eduardo Rodrigues Amaral - 11735021
- Laís Saloum Deghaide - 11369767

## Specifications:

- Python 3.10.7

## Instructions:

- To run a search between two artists, run the following command:

  ```
  python3 main.py
  ```

  Enter the name of the first artist and then the name of the second artist, then enter the algorithm you want to use (bfs or aStar).

  The program will output the path between the two artists and the number of nodes visited.

- To analyze the degrees of each artist, run the following command:

  ```
  python3 main.py analyze degree
  ```

- To run x experiments with random artists, run the following command:

  ```
  python3 main.py analyze efficiency <number of experiments>
  ```

  The results will be saved in `experiments/dd-mm-yy hh-mm-ss.json`

- To plot information from the experiments, run the following command:
  ```
  python3 main.py plot efficiency <path to the json file>
  ```
- To plot the graph in a interactive way, run the following command:
  ```
    python3 main.py plot graph <number of nodes to include>
  ```

## Degree Analysis:

Degree of artists nodes distribution:
![Degree of artists nodes distribution](./figures/degreeDist.png)

![Zoomed Degree of artists nodes distribution](./figures/degreeDistZoomed.png)

## Efficiency Analysis:

An experiment was run with 1000 random artists pairs, the results are shown below:

### Number of paths found:

![Number of paths found](./figures/pathFound.png)

### Shortest Path Length:

- Average Path Length:
  7.18
- Path's Length Histogram:
  ![Path's Length Histogram](./figures/minPathSizeDist.png)

### Number of times each algorithm found the shortest path:

![Number of times each algorithm found the shortest path](./figures/bestAlgPathSize.png)

### Number of times each algorithm found a path in less steps than the other:

- BFS:
  36.88%

- A\*:
  63.12%
- ![Number of times each algorithm found a path in less steps than the other](./figures/bestAlgStepSize.png)

### Distribution of steps difference between the faster algorithm and the slower algorithm (when BFS was faster and when A\* was faster):

- When BFS was faster the average difference was 11178 steps

- When A\* was faster the average difference was 25436 steps

- ![Distribution of steps difference between the algorithms when the algorithm x was faster](./figures/stepDifference.png)

## Graph Plot:
