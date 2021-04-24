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


def calcul_2_centres(liste_clusters, num_old_cluster, num_new_cluster):
    num = [num_old_cluster, num_new_cluster]
    for x in num:
        centre = []
        dim = len(liste_clusters[x]["points"][0])
        for i in range(0, dim):
            sum = 0
            for pt in liste_clusters[x]["points"]:
                sum += pt[i]
            moy = sum / len(liste_clusters[x]["points"])
            centre.append(round(moy, 3))
        liste_clusters[x]["centre"] = centre
    return liste_clusters


def calcul_distance(pt, centre):
    sum = 0
    for i in range(0, len(pt)):
        sub = (pt[i] - centre[i]) ** 2
        sum += sub
    return round(math.sqrt(sum), 3)


def trouve_plus_grand_cout(liste_points):
    cout = 0
    point = 0
    for pt in liste_points:
        if pt["dist"] > cout:
            cout = pt["dist"]
            point = pt
    if cout == 0:
        return 1
    else:
        return point


def algo(liste_clusters):
    liste_clusters = calcul_centres(liste_clusters)
    test = 1
    while test:
        couts = []
        for cl in liste_clusters:
            num_point = 0
            for pt in cl["points"]:
                point = {}
                dist = calcul_distance(pt, cl["centre"])
                for cl2 in liste_clusters:
                    if not cl2 == cl:
                        x = calcul_distance(pt, cl2["centre"])
                        if x < dist:
                            point["num_point"] = num_point
                            point["old_cluster"] = cl["num"]
                            point["new_cluster"] = cl2["num"]
                            point["dist"] = x
                if len(point) > 0 :
                    couts.append(point)
                num_point += 1
        point_final = trouve_plus_grand_cout(couts)
        if point_final == 1:
            test = 0
        else:
            pt = liste_clusters[point_final["old_cluster"]]["points"].pop(point_final["num_point"])
            liste_clusters[point_final["new_cluster"]]["points"].append(pt)
            liste_clusters = calcul_2_centres(liste_clusters, point_final["old_cluster"], point_final["new_cluster"])
    return liste_clusters

