# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:38:17 2018

@author: Alexander, Lasse og Magnus
"""

import numpy as np
import time
import matplotlib.pyplot as plt

start = time.time()

antal_år = 1 #maks 84
antal_simuleringer = 1
antal_baner = 2
maks_ventetid = 180

antal_baner2 = antal_baner

årligt_gennemsnit = []
årligt_gennemsnit2 = []
ny_bane = []
ankomst_shuffled=np.array([112,97,123,83,117])
landing_shuffled=np.array([536,467,611,571,521])
antal_fly = len(ankomst_shuffled)
bane_ventetid=[]


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
            


slut = time.time()
print("Det tager {:g} sekunder at eksekvere {} simuleringer for {} år".format(slut-start,antal_simuleringer,antal_år))
print("Der bør være {} landingsbaner efter {} år, og der er behov for at anlægge nye baner i årene {}".format(antal_baner2, antal_år, ny_bane))