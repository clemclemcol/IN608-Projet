import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Lloyd
import Prog_Greedy as PG


def remplis_cluster(nb_pt, dim, k):
    liste_clusters = []
    for i in range(0, k):
        liste_clusters.append({"num": i, "points": []})
    j = 0
    for i in range(0, nb_pt):
        point = []
        for l in range(0, dim):
            x = random.uniform(0, 10)
            point.append(round(x, 3))
        liste_clusters[j]["points"].append(point)
        if j == k - 1:
            j = 0
        else:
            j += 1
    return liste_clusters


def affiche_graphique(liste_clusters, dimension):
    if dimension == 1:
        for cluster in liste_clusters:
            color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for point in cluster["points"]:
                plt.scatter(point[0], 0, marker='.', c=color)
            plt.scatter(cluster["centre"][0], 0, marker='*', c=color, s=60)
    elif dimension == 2:
        for cluster in liste_clusters:
            color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for point in cluster["points"]:
                plt.scatter(point[0], point[1], marker='.', c=color)
            plt.scatter(cluster["centre"][0], cluster["centre"][1], marker='*', c=color, s=60)
    elif dimension == 3:
        fig = plt.figure()
        ax = Axes3D(fig)
        for cluster in liste_clusters:
            color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for point in cluster["points"]:
                ax.scatter(point[0], point[1], point[2], marker='.', c=color)
            ax.scatter(cluster["centre"][0], cluster["centre"][1], cluster["centre"][2], marker='*', c=color, s=50)
    plt.show()


def calcul_MSD(liste_clusters):
    sum = 0
    count = 0
    for cl in liste_clusters:
        for pt in cl["points"]:
            dist = Lloyd.calcul_distance(pt, cl["centre"])
            sum += dist ** 2
        count += len(cl["points"])
    return round(sum / count, 3)


def determine_MSD_Lloyd():
    print("Création et remplissage du fichier...")
    nbpts = [50, 100, 1000, 5000, 10000]
    nbcluster = [5, 10]
    mse = []
    for k in nbcluster:
        for nb in nbpts:
            for j in range(0, 30):
                print("k =", k, "nb de pts =", nb, "j =", j)
                liste_clusters = remplis_cluster(nb, 3, k)
                liste_clusters = Lloyd.algo(liste_clusters)
                mse.append(calcul_MSD(liste_clusters))
            create_data_file(k, mse, "resultat_Lloyd.txt", nb)
            mse = []
    print("Fichier 'resultat_Lloyd.txt' créé dans le dossier courant.")


def determine_MSD_PG():
    print("Création et remplissage du fichier...")
    nbpts = [50, 100, 1000, 5000, 10000]
    nbcluster = [5, 10]
    mse = []
    for k in nbcluster:
        for nb in nbpts:
            for j in range(0, 25):
                print("k =", k, "nb de pts =", nb, "j =", j)
                liste_clusters = remplis_cluster(nb, 3, k)
                liste_clusters = PG.algo(liste_clusters)
                mse.append(calcul_MSD(liste_clusters))
            create_data_file(k, mse, "resultat_PG.txt", nb)
            mse = []
    print("Fichier 'resultat_PG.txt' créé dans le dossier courant.")


def create_data_file(k, list_MSE, name_file, nbpoints):
    minMSE = min(list_MSE)
    maxMSE = max(list_MSE)
    avgMSE = sum(list_MSE)
    avgMSE = round(avgMSE / len(list_MSE), 3)

    file = open(name_file, "a")
    file.write("K = " + str(k) + "\t" + "nb points : " + str(nbpoints) + "\n")
    file.write("min MSD \t " + str(minMSE) + "\n")
    file.write("avg MSD \t " + str(avgMSE) + "\n")
    file.write("max MSD \t " + str(maxMSE) + "\n")
    file.write("__" + "\n")
    file.close()


""""""" MAIN """""""

# dimension = 3

# liste_cluster_lloyd = remplis_cluster(100, dimension, 10)
# liste_cluster_PG = liste_cluster_lloyd

# liste_cluster_lloyd = Lloyd.algo(liste_cluster_lloyd)
# liste_cluster_PG = PG.algo(liste_cluster_PG)

# affiche_graphique(liste_cluster_lloyd, dimension)
# affiche_graphique(liste_cluster_PG, dimension)

# determine_MSD_Lloyd()
# determine_MSD_PG()
