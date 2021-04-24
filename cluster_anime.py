import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
def remplis_cluster(nb_pt, dim, k):
    liste_clusters = []
    for i in range(0, k):
        liste_clusters.append({"num": i, "points": []})
    j = 0
    for i in range(0, nb_pt):
        point = []
        for l in range(0, dim):
            x = random.uniform(0, 10)
            point.append(round(x, 2))
        liste_clusters[j]["points"].append(point)
        if j == k - 1:
            j = 0
        else:
            j += 1
    return liste_clusters
"""


def calcul_centres(liste_clusters):
    centre = []
    for cl in liste_clusters:
        dim = len(cl["points"][0])
        for i in range(0, dim):
            sum = 0
            for pt in cl["points"]:
                sum += pt[i]
            moy = sum / len(cl["points"])
            centre.append(round(moy, 2))
        cl["centre"] = centre
        centre = []
    return liste_clusters


def calcul_distance(pt, centre):
    sum = 0
    for i in range(0, len(pt)):
        sub = (pt[i] - centre[i]) ** 2
        sum += sub
    return round(math.sqrt(sum), 4)


def compare_centre(old_liste, new_liste):
    liste_variation = []
    for i in range(0, len(old_liste)):
        x = calcul_distance(old_liste[i], new_liste[i]["centre"])
        liste_variation.append(x)
    for var in liste_variation:
        if var > 0:
            return 1
    return 0


def algo(liste_clusters, dim, k):
    color = []
    for i in range(0, k):
        color.append("#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]))

    liste_clusters = calcul_centres(liste_clusters)
    test = 1
    fig = plt.figure()
    while test:
        old_centres = []
        for cl in liste_clusters:
            num_point = 0
            for pt in cl["points"]:
                dist = calcul_distance(pt, cl["centre"])
                nv_cluster = -1
                for cl2 in liste_clusters:
                    if not cl2 == cl:
                        x = calcul_distance(pt, cl2["centre"])
                        if x < dist:
                            nv_cluster = cl2["num"]
                            dist = x
                if not nv_cluster == -1:
                    pt = liste_clusters[cl["num"]]["points"].pop(num_point)
                    liste_clusters[nv_cluster]["points"].append(pt)
                num_point += 1
            old_centres.append(cl["centre"])
        liste_clusters = calcul_centres(liste_clusters)

        # graphique avec les clusters actuels
        plt.pause(0.001)
        fig.clear()
        if dim == 1:
            i = 0
            for cluster in liste_clusters:
                for point in cluster["points"]:
                    plt.scatter(point[0], 0, marker='.', c=color[i])
                plt.scatter(cluster["centre"][0], 0, marker='*', c=color[i], s=60)
                i += 1
        elif dim == 2:
            i = 0
            for cluster in liste_clusters:
                for point in cluster["points"]:
                    plt.scatter(point[0], point[1], marker='.', c=color[i])
                plt.scatter(cluster["centre"][0], cluster["centre"][1], marker='*', c=color[i], s=60)
                i += 1
        elif dim == 3:
            i = 0
            ax = Axes3D(fig)
            for cluster in liste_clusters:
                for point in cluster["points"]:
                    ax.scatter(point[0], point[1], point[2], marker='.', c=color[i])
                ax.scatter(cluster["centre"][0], cluster["centre"][1], cluster["centre"][2], marker='*', c=color[i],
                           s=50)
                i += 1
        test = compare_centre(old_centres, liste_clusters)
        plt.draw()
    plt.show()
    return liste_clusters


"""
def calcul_MSE(liste_clusters):
    sum = 0
    count = 0
    for cl in liste_clusters:
        for pt in cl["points"]:
            dist = calcul_distance(pt, cl["centre"])
            sum += dist ** 2
        count += len(cl["points"])
    return round(sum / count, 2)
"""


# liste_cluster = [ {'num' : 0, 'points' : [ [x, y, ...], [x, y, ...], ... ], 'centre' : [x, y, ...] },
#                   {'num' : 1, 'points' : [ [x, y, ...], [x, y, ...], ... ], 'centre' : [x, y, ...] },
#                   { ... },
#                       ...
#                   { ... }  ]

def main(liste_cluster, dimension, k):
    # dimension = 2
    # k = 10
    # liste_cluster = algo(remplis_cluster(200, dimension, k), dimension, k)
    liste_cluster = algo(liste_cluster, dimension, k)
    print(liste_cluster)
