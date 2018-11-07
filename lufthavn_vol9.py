# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:38:17 2018

@author: Alexander, Lasse og Magnus
"""

import numpy as np
import time
import matplotlib.pyplot as plt

start = time.time()

antal_år = 30 #maks 84
antal_simuleringer = 200
antal_baner = 1
maks_ventetid = 180

antal_baner2 = antal_baner

årligt_gennemsnit = []
årligt_gennemsnit2 = []
ny_bane = []

for f in range(0, 2):

    for år in range(0, antal_år):
        antal_fly_raw = 200*(1.05)**(år)
        bane_ventetid = []

        if år > 0 and f == 1:
            if gennemsnit_bane_ventetid > maks_ventetid:
                antal_baner2 += 1
                ny_bane.append(år-1)
                

        for i in range(antal_simuleringer):
            # ================================================================
            # Ankomsttider for fly
            # ================================================================
            fordeling_ankomst_raw = np.array([44, 34, 27, 22, 16, 13, 10, 8, 6,
                                              5, 4, 3, 2, 2, 1, 1, 1, 0, 1, 0])

            ankomst_akkumuleret = np.cumsum(fordeling_ankomst_raw)
            ankomst_akkumuleret = np.insert(ankomst_akkumuleret, 0, 0)

            rand = np.random.randint(0, 200, np.round_(antal_fly_raw).astype(int))
            fordeling_ankomst, bins = np.histogram(rand, ankomst_akkumuleret)

            # ================================================================
            # Landingstider for fly
            # ================================================================
            fordeling_landing_raw = np.array([0, 16, 33, 61, 41, 25, 10, 8, 6])

            landing_akkumuleret = np.cumsum(fordeling_landing_raw)
            landing_akkumuleret = np.insert(landing_akkumuleret, 0, 0)

            rand2 = np.random.randint(0, 200, np.round_(antal_fly_raw).astype(int))
            fordeling_landing, bins = np.histogram(rand2, landing_akkumuleret)

            # ================================================================
            # Beregning af ankomst- og landingstider
            # ================================================================
            interval_ankomst_raw = np.array([[0, 60], [60, 120], [120, 180],
                                             [180, 240], [240, 300],
                                             [300, 360], [360, 420],
                                             [420, 480], [480, 540],
                                             [540, 600], [600, 660],
                                             [660, 720], [720, 780],
                                             [780, 840], [840, 900],
                                             [900, 960], [960, 1020],
                                             [1020, 1080], [1080, 1140],
                                             [1140, 1200]])/((1.05)**år)

            interval_ankomst = np.round_(interval_ankomst_raw)

            interval_landing = np.array([[0, 30], [31, 60], [61, 90],
                                         [91, 120], [121, 150], [151, 180],
                                         [181, 210], [211, 240], [241, 270]])

            # ================================================================
            # Lister med med landingstider og ankomsttider "shufflet"
            # ================================================================
            antal_fly = sum(fordeling_ankomst)
            ankomst_sorted = np.zeros(antal_fly)
            landing_sorted = np.zeros(antal_fly)

            x = 0
            for i in range(0, len(interval_ankomst)):

                ankomst_sorted[x:x+fordeling_ankomst[i]] = np.random.randint(interval_ankomst[i][0],
                                                                             interval_ankomst[i][1],
                                                                             fordeling_ankomst[i])

                x += fordeling_ankomst[i]

            x = 0
            for i in range(0, len(interval_landing)):

                landing_sorted[x:x+fordeling_landing[i]] = np.random.randint(interval_landing[i][0],
                                                                             interval_landing[i][1]+1,
                                                                             fordeling_landing[i])

                x += fordeling_landing[i]

            ankomst_shuffled = np.copy(ankomst_sorted)
            np.random.shuffle(ankomst_shuffled)

            landing_shuffled = np.copy(landing_sorted)
            np.random.shuffle(landing_shuffled)

            # ================================================================
            # Beregning af køtider og fordeling af fly på baner
            # ================================================================
            bane_køtid = np.array([0 for i in range(antal_baner2)])

            for i in range(0, antal_fly):
                bane_køtid = bane_køtid - ankomst_shuffled[i]

                for q in range(0, len(bane_køtid)):
                    if bane_køtid[q] < 0:
                        bane_køtid[q] = 0

                bane_ventetid.append(bane_køtid[bane_køtid.argmin()])
                bane_køtid[bane_køtid.argmin()] += landing_shuffled[i]

            gennemsnit_bane_ventetid = sum(bane_ventetid)/len(bane_ventetid)
        if f == 0:
            årligt_gennemsnit.append(gennemsnit_bane_ventetid)
        else:
            årligt_gennemsnit2.append(gennemsnit_bane_ventetid)

plt.style.use(['dark_background'])
plt.plot(range(0, antal_år), årligt_gennemsnit, "bo-")
plt.title("Gennemsnitlig ventetid med {} landingsbane(r)".format(antal_baner))
plt.xlabel("År")
plt.ylabel("Gns. ventetid")
plt.savefig("ventetid_uden_nye_baner.png")
plt.show()

plt.plot(range(0, antal_år), årligt_gennemsnit2, "ro")
plt.title("Gennemsnitlig ventetid med konstruktion af landingsbaner")
plt.xlabel("År")
plt.ylabel("Gns. ventetid")
plt.grid(axis = 'both')
plt.savefig("ventetid_med_baner.png")
plt.show()


slut = time.time()
print("Det tager {:g} sekunder at eksekvere {} simuleringer for {} år".format(slut-start,antal_simuleringer,antal_år))
print("Der er {} landingsbaner efter {} år, og der er behov for at anlægge nye baner i årene {}".format(antal_baner2, antal_år, ny_bane))