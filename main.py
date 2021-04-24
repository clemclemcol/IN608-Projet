import random
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Lloyd
import Prog_Greedy as PG
import tableau
import cluster_anime
import parallelisation as Para


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


def determine_MSD_Lloyd(nbtests):
    print("Creation et remplissage du fichier...")
    nbpts = [50, 100, 1000, 5000, 10000]
    nbcluster = [5, 10]
    dimension = 2
    mse = []
    for k in nbcluster:
        for nb in nbpts:
            for j in range(0, nbtests):
                print("k =", k, "nb de pts =", nb, "j =", j)
                liste_clusters = remplis_cluster(nb, dimension, k)
                liste_clusters = Lloyd.algo(liste_clusters)
                mse.append(calcul_MSD(liste_clusters))
            create_data_file(k, mse, "resultat_Lloyd.txt", nb, nbtests)
            mse = []
    print("Fichier 'resultat_Lloyd.txt' cree dans le dossier courant.")


def determine_MSD_PG(nbtests):
    print("Creation et remplissage du fichier...")
    nbpts = [50, 100, 1000, 5000, 10000]
    nbcluster = [5, 10]
    dimension = 2
    mse = []
    for k in nbcluster:
        for nb in nbpts:
            for j in range(0, nbtests):
                print("k =", k, "nb de pts =", nb, "j=", j)
                liste_clusters = remplis_cluster(nb, dimension, k)
                liste_clusters = PG.algo(liste_clusters)
                mse.append(calcul_MSD(liste_clusters))
            create_data_file(k, mse, "resultat_PG.txt", nb, nbtests)
            mse = []
    print("Fichier 'resultat_PG.txt' cree dans le dossier courant.")


def create_data_file(k, list_MSE, name_file, nbpoints, nbtests):
    minMSE = min(list_MSE)
    maxMSE = max(list_MSE)
    avgMSE = sum(list_MSE)
    avgMSE = round(avgMSE / len(list_MSE), 3)

    file = open(name_file, "a")
    file.write("Nombre tests = " + str(nbtests) + "\n")
    file.write("K = " + str(k) + "\t" + "nb points : " + str(nbpoints) + "\n")
    file.write("min MSD \t " + str(minMSE) + "\n")
    file.write("avg MSD \t " + str(avgMSE) + "\n")
    file.write("max MSD \t " + str(maxMSE) + "\n")
    file.write("__" + "\n")
    file.close()


def average_time(list_time):
    sumtime = sum(list_time, datetime.timedelta(0))
    if len(list_time) == 0:
        print("empty")
    else:
        avgtime = sumtime / len(list_time)
        print("sum:", sumtime, "avg:", avgtime)
        return avgtime.total_seconds()


def list_of_times(nbcluster, nbpts, case, nbtest):
    time = []
    avgtime = []
    algo_times = []
    for k in nbcluster:
        for nb in nbpts:
            if case == 1:
                for j in range(0, nbtest):
                    liste_clusters = remplis_cluster(nb, 2, k)
                    begin_time = datetime.datetime.now()
                    Lloyd.algo(liste_clusters)
                    time.append(datetime.datetime.now() - begin_time)
            if case == 2:
                for j in range(0, nbtest):
                    print("k =", k, "nb de pts =", nb, "j=", j)
                    liste_clusters = remplis_cluster(nb, 2, k)
                    begin_time = datetime.datetime.now()
                    PG.algo(liste_clusters)
                    time.append(datetime.datetime.now() - begin_time)

            avgtime.append(average_time(time))
            time = []
        algo_times.append(avgtime)
        avgtime = []
    return algo_times


def time_curve():
    print("Creation et remplissage du fichier...")
    nbpts = [50, 100, 500, 1000, 5000, 10000]
    nbcluster = [3, 4, 5, 10]
    lloyd_times = list_of_times(nbcluster, nbpts, 1, 2)
    pg_times = list_of_times(nbcluster, nbpts, 1, 2)
    tableau.create_excel(lloyd_times, pg_times)

    print("Fichier 'tabs.xls' cree dans le dossier courant.")
    



""""""" MAIN """""""
dimension = 2  
k = 5
nb_pts = 100
nbtests = 6

# PROPOSITION 1
""" 
# --->  1 creation liste_cluster
liste_cluster_lloyd = remplis_cluster(nb_pts, dimension, k)
liste_cluster_PG = liste_cluster_lloyd

# --->  2 appel algo
liste_cluster_lloyd = Lloyd.algo(liste_cluster_lloyd)
liste_cluster_PG = PG.algo(liste_cluster_PG)

# --->  3 affichage graphique
affiche_graphique(liste_cluster_lloyd, dimension)
affiche_graphique(liste_cluster_PG, dimension)
"""

# PROPOSITION 2
""" 
# --->  1 creation liste_cluster
liste_cluster_lloyd = remplis_cluster(nb_pts, dimension, k)
# liste_cluster_PG = liste_cluster_lloyd

# --->  2 affichage animations
cluster_anime.main(liste_cluster_lloyd, dimension, k)
# cluster_anime.main(liste_cluster_PG, dimension, k)
"""

# PROPOSITION 3

# --->  1 creation fichiers Lloyd et PG MSD
#determine_MSD_Lloyd(nbtests)
#determine_MSD_PG(nbtests)
path_dir = "/home/user/Bureau/IN608 - Projet/projet_v2/projet_v2" #depend de ou est votre dossier logique
Para.parallelisation(path_dir)

# --->  2 creation fichier tabs.xls
#time_curve()

