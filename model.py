# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 15:33:43 2014
@author: juliegalia
"""
### help ('for')

import numpy as np
import matplotlib.pyplot as mpl
import random as rd
import time

#### matrice de tous les génotypes possibles avec redondance
genoredo = np.array([('A1', 'B1', 'A1', 'B1'),  ### unique
                     ('A1', 'B1', 'A1', 'B2'),  ### ligne 1=ligne2
                     ('A1', 'B2', 'A1', 'B1'),
                     ('A1', 'B1', 'A2', 'B1'),  ### ligne3=ligne 4
                     ('A2', 'B1', 'A1', 'B1'),
                     ('A1', 'B1', 'A2', 'B2'),  ### ligne5=ligne 6
                     ('A2', 'B2', 'A1', 'B1'),
                     ('A1', 'B2', 'A2', 'B1'),  ### ligne7=ligne8
                     ('A2', 'B1', 'A1', 'B2'),
                     ('A1', 'B2', 'A1', 'B2'),  ### unique
                     ('A1', 'B2', 'A2', 'B2'),  ###ligne 10= ligne11
                     ('A2', 'B2', 'A1', 'B2'),
                     ('A2', 'B1', 'A2', 'B1'),  ###unique
                     ('A2', 'B1', 'A2', 'B2'),  ### ligne13=ligne14
                     ('A2', 'B2', 'A2', 'B1'),
                     ('A2', 'B2', 'A2', 'B2'),  ### unique
                     ])

### matrice de tous les génotypes sans redondance
genotype = np.array([('A1', 'B1', 'A1', 'B1'),
                     ('A1', 'B1', 'A1', 'B2'),
                     ('A1', 'B1', 'A2', 'B1'),
                     ('A1', 'B1', 'A2', 'B2'),
                     ('A1', 'B2', 'A2', 'B1'),
                     ('A1', 'B2', 'A1', 'B2'),
                     ('A1', 'B2', 'A2', 'B2'),
                     ('A2', 'B1', 'A2', 'B1'),
                     ('A2', 'B1', 'A2', 'B2'),
                     ('A2', 'B2', 'A2', 'B2'),
                     ])

### demande à l'utilisateur les paramètres
N = int(input(
    "taille de la population?(multiple de 10)"))  # multiple de 10 pour que les fréquences de génotypes soit équiprobables
while N % 10 != 0:
    N = int(input(
        "non multiple de 10, taille de la population?"))  # multiple de 10 pour que les fréquences de génotypes soit équiprobables

S = int(input("nombre de simulation?"))  ### nombre de simulation

u = float(input("taux de mutation de A?"))
v = float(input("taux de mutation de B?"))
r = float(input("taux de recombinaison?"))

#### vecteurs des mutations
U = np.array([('A1'), ('A2')])
V = np.array([('B1'), ('B2')])

### matrice des féquences finales (au bout de 1000 générations) par simulation
freqfinale = np.zeros((10, S))

# timer pour connaître le temps de calcul
debut = time.time()

#### boucle for pour les simulations
for s in range(0, S):

    ### compteur
    rec = 0  ### compteur recombinaison
    mutu = 0  ### compteur mutation u
    mutv = 0  ### compteur mutation v

    #### création poulation initiale ##
    A = genotype
    for m in range(1, N / 10):
        A = np.append(A, genotype, axis=0)
        m += 1

    #### matrice des féquences par générations
    freq = np.zeros((10, 1000))

    ###fréquence de la population initiale
    gen = np.zeros((10))  ### nombre de chaque génotype dans la population initiale

    for i in range(0, N):
        for x in range(0, 10):
            if (A[i, :] == genotype[x, :]).all():
                gen[x] = gen[x] + 1
            x += 1
        i += 1
    freq[:, 0] = gen / N

    ## for t in range(1:1000): boucle pour 1000 générations
    for t in range(1, 1000):

        #### tirage alétoire parent
        #### matrice des parents
        P = np.zeros((2 * N, 4))  # matrice des parents 2xN car il faut 2 parents pour faire un enfant
        P = P.astype("str")
        b = np.zeros(2 * N)

        for x in range(0, 2 * N):
            b[x] = rd.randint(0, N - 1)
            P[x, :] = A[b[x], :]
            if rec == 1 / r:
                valx1 = P[x, 1]  ### sauvegarde la valeur de p[x,1]
                P[x, 1] = P[x, 3]
                P[x, 3] = valx1
            else:
                rec = rec + 1
            x += 1

            #### Matrice des enfants
        F = np.zeros((N, 4))
        F = F.astype("str")
        ### gamètes
        p = 0
        for x in range(0, N):
            p2 = p + 1
            g1 = rd.randint(1, 2)  ### tirage aléatoire du gamète 1
            g2 = rd.randint(1, 2)  ### tirage aléatoire du gamète 2
            if g1 == 1:
                F[x, 0:2] = P[p, 0:2]  ### haplotype 1 = gamète 1 du P1
            else:
                F[x, 0:2] = P[p, 2:4]  ### haplotype 1 = gamète 2 du P1
            if g2 == 1:
                F[x, 2:4] = P[p2, 0:2]  ### haplotype 2 = gamète 1 du P2
            else:
                F[x, 2:4] = P[p2, 2:4]  ### haplotype 2 = gamète 2 du P2
                p = p + 2
            if mutu == 1 / u:
                urand = rd.randint(1, 2)  ### pour choisir sur quel chromosome a lieu la mutation
                if urand == 1:
                    if F[x, 0] == U[0]:
                        F[x, 0] = U[1]
                    else:
                        F[x, 0] = U[0]
                else:
                    if F[x, 2] == U[0]:
                        F[x, 2] = U[1]
                    else:
                        F[x, 2] = U[0]
                mutu = 0
            else:
                mutu = mutu + 1
            if mutv == 1 / v:  ### s'il y a mutation
                urand = rd.randint(1, 2)  ### pour choisir sur quel chromosome a lieu la mutation
                if urand == 1:
                    if F[x, 1] == V[0]:  ### pour faire la mutation comparaison avec le vecteur des allèles
                        F[x, 1] = V[1]
                    else:
                        F[x, 1] = V[0]
                else:
                    if F[x, 3] == V[0]:
                        F[x, 3] = V[1]
                    else:
                        F[x, 3] = V[0]
                mutv = 0
            else:
                mutv = mutv + 1
            x += 1

        ### fréquence des génotypes dans la nouvelles générations
        nbgen = np.zeros(16)  ### nombre de chaque génotype (avec redondance) dans la nouvelles population
        for i in range(0, N):
            for x in range(0, 16):
                if (P[i, :] == genoredo[x, :]).all():
                    nbgen[x] = nbgen[x] + 1
                x += 1
            i += 1

        ### calcul des effectifs de chaque génotype sans redondance
        nbfreq = np.array([(nbgen[0]),
                           (nbgen[1] + nbgen[2]),
                           (nbgen[3] + nbgen[4]),
                           (nbgen[5] + nbgen[6]),
                           (nbgen[7] + nbgen[8]),
                           (nbgen[9]),
                           (nbgen[10] + nbgen[11]),
                           (nbgen[12]),
                           (nbgen[13] + nbgen[14]),
                           (nbgen[15]),
                           ])
        ###print (sum(nbfreq))
        freq[:, t] = nbfreq / N  ### calcul des fréquences
        A = F
        t += 1
    freqfinale[:, s] = freq[:, 999]
    s += 1

fin = time.time()
duree = (fin - debut) / 60
print(duree)

### graphique pour 1 simulations
### numpy.T(freq)    Trajectoirede de chague génotype pour la dernière simulation
mpl.figure(1)
Z = np.transpose(freq)
mpl.plot(Z)
mpl.title('Trajectoire de chaque génotype')
mpl.xlabel('temps')
mpl.ylabel('frequence')

### graphiques des fréquences finales pour chaque simulations
mpl.figure(2)
mpl.plot(freqfinale)  # une trajectoire = 1 simulation
mpl.title('Fréquence finale de chaque simulation')
mpl.xlabel('genotype')
mpl.ylabel('frequence')

mpl.text(-0.25, -0.02, 'A1B1', color='r')
mpl.text(-0.25, -0.05, 'A1B1', color='r')
mpl.text(0.75, -0.02, 'A1B1', color='r')
mpl.text(0.75, -0.05, 'A1B2', color='r')
mpl.text(1.75, -0.02, 'A1B1', color='r')
mpl.text(1.75, -0.05, 'A2B1', color='r')
mpl.text(2.75, -0.02, 'A1B1', color='r')
mpl.text(2.75, -0.05, 'A2B2', color='r')
mpl.text(3.75, -0.02, 'A1B2', color='r')
mpl.text(3.75, -0.05, 'A2B1', color='r')
mpl.text(4.75, -0.02, 'A1B2', color='r')
mpl.text(4.75, -0.05, 'A1B2', color='r')
mpl.text(5.75, -0.02, 'A1B2', color='r')
mpl.text(5.75, -0.05, 'A2B2', color='r')
mpl.text(6.75, -0.02, 'A2B1', color='r')
mpl.text(6.75, -0.05, 'A2B1', color='r')
mpl.text(7.75, -0.02, 'A2B1', color='r')
mpl.text(7.75, -0.05, 'A2B2', color='r')
mpl.text(8.75, -0.02, 'A2B2', color='r')
mpl.text(8.75, -0.05, 'A2B2', color='r')

### graphique des occurences des génotypes par intervalle de fréquence
Y = np.transpose(freqfinale)
mpl.figure(3)
histY = mpl.hist(Y)
mpl.xlabel('frequence')
mpl.ylabel('occurence')
mpl.title('Occurence sur les simulations des génotypes par intervalle de fréquence')
# histf=mpl.hist(freqfinale)

### Graphique des moyennes des fréquences finales
mean = np.mean(freqfinale, axis=1)
# mpl.figure(4)
# bins=c(0:0,1:1)
# hist=mpl.hist(mean,bins=10) ### nombre de génotype par classe de fréquence

####
mpl.figure(5)
ind = np.arange(10)
hist2 = mpl.bar(ind, mean)  ### fréquence moyenne de chaque généotype

#  histogramme des donn\'es
# n, bins, patches = plt.hist(x, 50, normed=1, facecolor='g', alpha=0.75)
mpl.xlabel('génotype')
mpl.ylabel('frequence')
mpl.title('Moyenne des fréquences finales de chaque génotype')

mpl.text(0, 0.01, 'A1B1', color='r')
mpl.text(0, 0, 'A1B1', color='r')
mpl.text(1, 0.01, 'A1B1', color='r')
mpl.text(1, 0, 'A1B2', color='r')
mpl.text(2, 0.01, 'A1B1', color='r')
mpl.text(2, 0, 'A2B1', color='r')
mpl.text(3, 0.01, 'A1B1', color='r')
mpl.text(3, 0, 'A2B2', color='r')
mpl.text(4, 0.01, 'A1B2', color='r')
mpl.text(4, 0, 'A2B1', color='r')
mpl.text(5, 0.01, 'A1B2', color='r')
mpl.text(5, 0, 'A1B2', color='r')
mpl.text(6, 0.01, 'A1B2', color='r')
mpl.text(6, 0, 'A2B2', color='r')
mpl.text(7, 0.01, 'A2B1', color='r')
mpl.text(7, 0, 'A2B1', color='r')
mpl.text(8, 0.01, 'A2B1', color='r')
mpl.text(8, 0, 'A2B2', color='r')
mpl.text(9, 0.01, 'A2B2', color='r')
mpl.text(9, 0, 'A2B2', color='r')

# plt.axis([40, 160, 0, 0.03])
mpl.grid(True)