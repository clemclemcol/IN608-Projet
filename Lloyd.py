import math


def calcul_centres(liste_clusters):
    centre = []
    for cl in liste_clusters:
        dim = len(cl["points"][0])
        for i in range(0, dim):
            sum = 0
            for pt in cl["points"]:
                sum += pt[i]
            moy = sum / len(cl["points"])
            centre.append(round(moy, 3))
        cl["centre"] = centre
        centre = []
    return liste_clusters


def calcul_distance(pt, centre):
    sum = 0
    for i in range(0, len(pt)):
        sub = (pt[i] - centre[i]) ** 2
        sum += sub
    return round(math.sqrt(sum), 3)


def compare_centre(old_liste, new_liste):
    liste_variation = []
    for i in range(0, len(old_liste)):
        x = calcul_distance(old_liste[i], new_liste[i]["centre"])
        liste_variation.append(x)
    for var in liste_variation:
        if var > 0:
            return 1
    return 0


def algo(liste_clusters):
    liste_clusters = calcul_centres(liste_clusters)
    test = 1
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
        test = compare_centre(old_centres, liste_clusters)
    return liste_clusters

