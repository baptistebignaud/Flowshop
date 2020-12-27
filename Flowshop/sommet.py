#!/usr/bin/env python

""" Classe Sommet :

A utiliser avec une file de priorité (heapq)
pour la recherche arborescente de la méthode
par évaluation-séparation
"""

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import heapq
import ordonnancement


class Sommet():

    def __init__(self, seq, non_places, val, num):
        self.seq = seq
        self.non_places = non_places
        self.val = val
        self.num = num

    def sequence(self):
        return self.seq

    def jobs_non_places(self):
        return self.non_places

    def evaluation(self):
        return self.val

    def numero(self):
        return self.num

    def creer_sommet(self,s,job):
        sauv=s.seq
        self.seq=sauv+[job]
        sauv2=s.non_places
        self.non_places=sauv2[:sauv2.index(job)]+sauv2[sauv2.index(job)+1:]
        o=ordonnancement.Ordonnancement(5)
        #o.ordonnancer_liste_job(s2.seq)
        #f=Flowshop(len(s2.seq),5,s2.seq)
        #self.val=f.calculer_borne_inf(o,self.seq)

    def best_first(self, l_jobs):
        pass





    def __lt__(self, autre):
        """ Etablit la comparaison selon l'évaluation associée au sommet """
        return self.val < autre.val
