import os
import pandas as pd

class P:
    def __init__(self, id, indep, dep):
        self.id = id
        self.indep = indep
        self.dep = dep
        self.neighbors = []

    def add_neighbors(self, neighbors):
        self.neighbors = neighbors


def distance(A, B):
    """ A and B are instances of type P """
    assert(len(A.indep) == len(B.indep)), "Something is wrong"
    assert(A.id != B.id), "Something is wrong"
    sum = 0
    for i,j in zip(A.indep, B.indep):
        sum += (i-j)**2
    return sum ** 0.5

data_folder = "./Data/"
files = [data_folder + f for f in os.listdir(data_folder) if ".csv" in f]

for f in files:
    c = pd.read_csv(f)
    head = list(c)
    cindep = [cc for cc in head if '$<' not in cc]
    cdep = [cc for cc in head if '$<' in cc]
    assert(len(cindep) + len(cdep) == len(head)), "Something is wrong"

    points = []
    for id, (i, d) in enumerate(zip(c[cindep].values.tolist(), c[cdep].values.tolist())):
        points.append(P(id, i, d[-1]))

    assert(len(points) == len(c)), "Somethign is wrong"

    for i, point in enumerate(points):
        distances = {}
        # find distance between all points
        for r, rest in enumerate(points):
            if i != r:
                t = distance(point, rest)
                if t not in distances.keys():
                    distances[t] = [r]
                else:
                    distances[t].append(r)

        min_value = min(distances.keys())
        neighbors = distances[min_value]
        point.add_neighbors(neighbors)

    # create graph
    import graphviz as gv
    g1 = gv.Graph(format='png')
    for point in points:
        g1.node(str(point.id))
    g1.edge('A', 'B')
    for p in points:
        for n in p.neighbors:
            g1.edge(str(p.id), str(n))

    # filename = g1.render(filename='img/g1', view=False)
    # print filename
    filename = f.replace('./Data/', '').replace('.csv', '')
    f = open('img/'+ filename + '.dot', 'w')
    f.write(g1.source)
    f.close()

    import pdb
    pdb.set_trace()


