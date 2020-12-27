#!/usr/bin/env python

"""Résolution du flowshop de permutation :

 - par algorithme NEH
 - par une méthode évaluation-séparation
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job
import ordonnancement
import sommet
#import numpy as np

import heapq

MAXINT = 10000

class Flowshop():
    def __init__(self, nb_jobs=0, nb_machines=0, l_job=[]):
        self.nb_jobs = nb_jobs
        self.nb_machines = nb_machines
        self.l_job = l_job

    def nombre_jobs(self):
        return self.nombre_jobs

    def nombre_machines(self):
        return self.nombre_machines

    def liste_jobs(self, num):
        return self.l_job[num]

    def definir_par(self, nom):
        """ crée un problème de flowshop à partir d'un fichier """
        # ouverture du fichier en mode lecture
        fdonnees = open(nom,"r")
        # lecture de la première ligne
        ligne = fdonnees.readline()
        l = ligne.split() # on récupère les valeurs dans une liste
        self.nb_jobs = int(l[0])
        self.nb_machines = int(l[1])

        for i in range(self.nb_jobs):
            ligne = fdonnees.readline()
            l = ligne.split()
            # on transforme les chaînes de caractères en entiers
            l = [int(i) for i in l]
            j = job.Job(i, l)
            self.l_job += [j]
        # fermeture du fichier
        fdonnees.close()


    # exo 4 A REMPLIR
    def creer_liste_NEH(self):
        self.l_job=sorted(self.l_job,key= lambda job:job.calculer_duree_job(), reverse=True)
        neh_list=[self.l_job[0]]
        list_inter=neh_list
        temps1=float('inf')
        #neh_liste=ordonnancement.Ordonnancement.sequence([self.l_job[0]])

        #Ordo_intermediaire= ordonnancement.Ordonnancement(5)
        #Ordo_intermediaire.seq.append(self.l_job[0])
        #for i in range (1,self.nb_jobs):
         #   Ordo_intermediaire.seq.append(self.l_job[i])
          #  ordonnancement.Ordonnancement.ordonnancer_liste_job(Ordo_intermediaire,neh_liste)
           # neh_liste=sorted(neh_liste,key= lambda ordonnancement:neh_liste.duree(), reverse=False)
        for i in range (len(self.l_job)-1):
                    for j in range (len(neh_list)+1):
                        list_inter.insert(j,self.l_job[i+1])
                        ordo=ordonnancement.Ordonnancement(5)
                        ordonnancement.Ordonnancement.ordonnancer_liste_job(ordo,list_inter)
                        temps2=ordonnancement.Ordonnancement.duree(ordo)
                        if temps1 > temps2:
                            temps1=temps2
                            placer=j
                        del list_inter[j]
                    neh_list.insert(placer,self.l_job[i+1])
                    temps1=1000
        return(neh_list)



    # exo 5 A REMPLIR

    # calcul de r_kj tenant compte d'un ordo en cours
    def calculer_date_dispo(self, ordo, machine, job):
        indice=ordo.seq.index(job)
        #for i in range (self.nb_jobs):
            #if ordo.seq[i]==job:
                #indice+=i
                #print (indice)
        return (ordo.seq[indice].date_deb[machine-1])


    # calcul de q_kj tenant compte d'un ordo en cours
    def calculer_duree_latence(self, ordo, machine, job):
        Indice_Job = ordo.seq.index(job)
        return job.date_deb[-1] + job.duree_op[-1] - job.date_deb[machine-1] - job.duree_op[machine-1]

    # calcul de la somme des durées des opérations d'une liste
    # exécutées sur une machine donnée
    def calculer_duree_jobs(self, machine, liste_jobs):
        duree_job=0
        for i in range(len(liste_jobs)):
            duree_job+=liste_jobs[i].duree_op[machine-1]
        return (duree_job)

    # calcul de la borne inférieure en tenant compte d'un ordonnancement en cours
    def calculer_borne_inf(self, ordo, liste_jobs):
        date_dispo=[[0 for i in range (len(liste_jobs))] for j in range((self.nb_machines))]
        date_latence=[[0 for i in range (len(liste_jobs))] for j in range((self.nb_machines))]

        for job in liste_jobs:
            for k in range (self.nb_machines):
                #print (date_dispo[1][3])
                date_dispo[k][liste_jobs.index(job)]=self.calculer_date_dispo(ordo,k,job)

                date_latence[k][liste_jobs.index(job)]=self.calculer_duree_latence(ordo,k,job)
        LB_liste=[0 for i in range (self.nb_machines)]


        for k in range(self.nb_machines):

            #print(min(date_dispo[k]))
            #print(min(date_latence[k]))
            #print(self.calculer_duree_jobs(k, liste_jobs))
            LB_liste[k]=min(date_dispo[k])+min(date_latence[k])+ self.calculer_duree_jobs(k, liste_jobs)
        LB=max(LB_liste)
        return (LB)

    # exo 6 A REMPLIR
    # procédure par évaluation et séparation



    def evaluation_separation(self):
        Sommet1=sommet.Sommet([],self.l_job,0,1)

        l_sommet=[Sommet1]
        #On Transforme la liste en heapq
        heapq.heapify(l_sommet)
        optimum=100000
        optimum_seq=[]


        while l_sommet !=[]:

            s=sommet.Sommet([],[],0,0)
            #print(s)
            #On prend le plus petit élément
            s=heapq.heappop(l_sommet)
            sauv=s.seq
            sauv2=s.non_places
            if s.non_places==[]:

                o1=ordonnancement.Ordonnancement(5)
                o1.ordonnancer_liste_job(s.seq)
                #print (s.seq)

                #On calcule la durée de l'ordonnancement
                s.val=o1.duree()

                #Test de si la valeur est meilleure que la précédente
                if s.val<optimum:
                    optimum=s.val
                    optimum_seq=s.seq
                    print(optimum)

            else:


                for job in s.non_places:
                    #On crée des sommets pour chaque job non placés
                    s2=sommet.Sommet([],[],0,0)
                    s2.seq=sauv.copy()
                    s2.seq.append(job)
                    s2.non_places=sauv2.copy()
                    s2.non_places.remove(job)
                    o=ordonnancement.Ordonnancement(5)
                    o.ordonnancer_liste_job(s2.seq)
                    f=Flowshop(len(s2.seq),5,s2.seq)
                    s2.val=f.calculer_borne_inf(o,s2.seq)
                    if l_sommet!=[]:
                        s2.num=l_sommet[-1].num+1

                    #On rajoute ensuite a heapq
                    if s2.val<optimum:
                        heapq.heappush(l_sommet,s2)

        return( optimum, optimum_seq)

if __name__ == "__main__":

    Ordo = ordonnancement.Ordonnancement(5)
	#j1=job.job(1,[1,3,5,2])
	#j2=job.job(2,[3,6,8,1])
	#Ordo.ordonnancer_liste_job([j1,j2])

    j0=job.Job(0,[54,79,16,66,58])
    j1=job.Job(1,[83,3 ,89, 58, 56])
    j2=job.Job(2,[15, 11, 49, 31, 20 ])
    j3=job.Job(3,[71, 99, 15, 68, 85])
    j4=job.Job(4,[77, 56, 89, 78, 53])
    j5=job.Job(5,[36, 70, 45, 91, 35 ])
    j6=job.Job(6,[53, 99, 60, 13, 53])
    j7=job.Job(7,[38, 60, 23, 59, 41])
    l=[j2,j7,j5,j3,j1,j0,j4]
    l.append(j6)


    f=Flowshop(8,5,l)
    Ordo.ordonnancer_liste_job(l)
    f.evaluation_separation()


