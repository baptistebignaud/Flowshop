#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 11:26:12 2020

@author: baptistebignaud
"""
import numpy as np
import job
import statistics as stats
import ordonnancement
import math
from random import *
# Définition des paramètres
alpha=1.1
beta=1.1
A=500
B=500
D=600
C=350
E=100
#nb_machines=5

#Définition des paramètres de précision sur la recherche du minimum
p=30
nb_iter_max=100
ectp_max=0,8
nombre_iteration=50


#%%


def calcul_distance(L_jobs):

    p=L_jobs[0].nb_op
    N=len(L_jobs)
    D=np.zeros((N+1,N+1), dtype='float')
    for i in range (N):
        for j in range (N):
            if i!=j:
  
                D[i][j]=(alpha*(sum(L_jobs[i].duree_op[:p-1])+sum(L_jobs[j].duree_op[:p-1]))
                                +beta*(L_jobs[j].duree_op[p-1]+L_jobs[i].duree_op[p-1]))/2
                         

    
    #Permet de prendre en compte que nous ne bouclons pas du dernier job au premier
    D[0][0]=50000
    for j in (1,range(N+1)):
        D[N][j]=50000
        D[j][N]=50000
   
    return D

#%%
def kronecker(i,j):
    if i==j:
        return 1
    return 0

#%%
#Définition matrice de poids et constante externe
def W_ijkl(L_jobs,i,j,k,l):
    calculDistance=calcul_distance(L_jobs)
    #print(L_jobs)
    return((-A*kronecker(i,k)*(1-kronecker(j,l))
           -B*kronecker(j,l)*(1-kronecker(i,k))
           -C
           -D*kronecker(i,k)*calculDistance[i][k]*(1-kronecker(j,l-1))))

def I_ij(L_jobs,i,j):
    N=len(L_jobs)
    return(N*C+E*kronecker(i,N)*kronecker(j,N))



#%%
def file_attente(Tab,elem_a_rajouter):
    n=len(Tab)
    Tab_copy=Tab.copy()
    for i in range(n-1):
        Tab[i+1]=Tab_copy[i]
    Tab[0]=elem_a_rajouter
    return Tab

#%%
#Définition fonction objectif

#Quadruple somme avec indices i,j,k,l
def quadruple_somme(L_jobs,X):
    S_quadruple=0
    N=len(L_jobs)
    for i in range (N):
        for j in range (N):
            for k in range (N):
                for l in range (N):
                    S_quadruple+=W_ijkl(L_jobs,i,j,k,l)* X[i][j]*X[k][l]
    return S_quadruple

def double_somme(L_jobs,X):
    S_double=0
    N=len(L_jobs)
    for i in range (N):
        for j in range(N):
            S_double+=I_ij(L_jobs,i,j)*X[i][j]
    return S_double

                
def fonction_objectif(X,L_jobs):
    N=len(L_jobs)
    fonction_obj=-(quadruple_somme(L_jobs, X))/2+double_somme(L_jobs, X)+((C*N**2)/2)+E*(1-X[N][N])**2
    return(fonction_obj)
                   
            
#%%
def f_methode(Y,L_jobs,i,j):
    f_Y=0
    if Y[i][j]>0:
        f_Y=1
    else:
        f_Y=0
    return f_Y

def Y_t_plus_1_methode(L_jobs,Y,i,j):
    N=len(L_jobs)
    Y_t_plus_1=0
    for k in range(N):
        for l in range(N):
            Y_t_plus_1+=W_ijkl(L_jobs,i, j, k, l)*f_methode(Y,L_jobs,k,l)
    Y_t_plus_1+=I_ij(L_jobs,i,j)
    return Y_t_plus_1
              
              
    
def f(Y,L_jobs):
    N=len(L_jobs)
    f_Y=np.zeros((N,N),dtype='float')
    for i in range(N):
        for j in range(N):
            if Y[i][j]>0:
                f_Y[i][j]=1
            else:
                f_Y[i][j]=0
    return f_Y

def Y_t_plus_1(L_jobs,Y):
    N=len(L_jobs)
    Y_t_plus_1=np.zeros((N,N),dtype='float')
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    Y_t_plus_1[i][j]+=W_ijkl(L_jobs,i, j, k, l)*f(Y,L_jobs)[i][j]    
            Y_t_plus_1+=I_ij(L_jobs,i,j)
    return Y_t_plus_1
    
    
    

#%%


#Calcul de la durée total pour un ordonnancement précis
def calcul_duree(X,L_jobs,nb_machines):
    duree=0
    n=len(X)
    for i in range(n):
        a=0
        for j in range(n):
            if X[i][j]==1:
                a+=1
        if a!=1:
            duree= 50000
            return (duree,[],[])
    for j in range(n):
        a=0
        for i in range(n):
            if X[i][j]==1:
                a+=1
        if a!=1:
            duree= 50000
            return (duree,[],[])
    liste_numero_job=np.zeros(n,dtype='int')
    for j in range(n):
        for i in range(n):
            if X[i][j]==1:
                liste_numero_job[j]=i
    ordonnancement_jobs=ordonnancement.Ordonnancement(nb_machines)
    #print(liste_numero_job)
    l_1=[]
    for i in range(n):
        #print(L_jobs[liste_numero_job[i]])
        #l_1+=[L_jobs[liste_numero_job[i]]]
        l_1.append(L_jobs[liste_numero_job[i]])
    #for i in l_1:
        #print(i.numero())
    ordonnancement_jobs.ordonnancer_liste_job(l_1)
    #print(ordonnancement_jobs.seq)
    
    #print(ordonnancement_jobs.seq)
    #print (duree)
    return(ordonnancement_jobs.ordonnancer_liste_job(L_jobs),ordonnancement_jobs.afficher(),liste_numero_job)
    
    
    
                
            

#%%
def calcul_ordo(L_jobs):
    
    nb_machines=L_jobs[1].nb_op
    N=len(L_jobs)
    #print (N)
    f_y=np.zeros((N,N), dtype='float')
    #print (f_Y)
    compteur=0
    
    
    #Tableau qui contient les durées pour voir la convergence; initialisation avec écart type élevé
    Tab=np.arange(1,p**2,p,dtype='float')
    Y=np.zeros((N,N), dtype='float')
    #print (Y)
    #print(Tab)
    
    ectp=stats.stdev(Tab)
    moy=stats.mean(Tab)
    ectp_norm=ectp/moy
    
    #initialisation
    
    N=len(L_jobs)
    for k in range(N):
        i=randint(0,N-1)
        j=randint(0,N-1)
        f_y[i][j]=1
    
    # for i in range (N):
    #     for j in range(N):
            
    #         f_y[i][j]=randint(0,1)
    #f_y=np.eye(N)
    #print (f_y)

    Y=Y_t_plus_1(L_jobs,Y)
    #print("f_y")
    #print(f_y)
    file_attente(Tab, calcul_duree(f_y, L_jobs,nb_machines)[0])
    #print(ectp_norm)
    #print(moy)
    duree_opt=50000
    liste_jobs=[]
    liste_indice=[]
    
    while (compteur< nb_iter_max):# or ectp_norm>ectp_max or moy==50000):
        #print("entrée while")
        #Mat=[(i,j) for i in range(N) for j in range(N)]
        #print(Mat)
        for i in range(N):
            j=randint(0,N-1)
            Y[i][j]=Y_t_plus_1_methode(L_jobs, Y,i,j)
            f_y[i][j]=f_methode(Y,L_jobs,i,j)
        # while (len(Mat)>(N**2)/4):
        #     i_j=choice(Mat)
        #     #print(i_j)
        #     #print(f_y)
        #     Y[i_j[0]][i_j[1]]=Y_t_plus_1_methode(L_jobs, Y,i_j[0],i_j[1])
        #     f_y[i_j[0]][i_j[1]]=f_methode(Y,L_jobs,i_j[0],i_j[1])
        #     Mat.remove(i_j)
        #print("f_y")
        #print(f_y)
        #print("Durées")
        #print(Tab[0])
        #print(calcul_duree(f_y,L_jobs,nb_machines))
        duree=calcul_duree(f_y,L_jobs,nb_machines)[0]
        liste_job=calcul_duree(f_y,L_jobs,nb_machines)[1]
        file_attente(Tab,duree )
        if calcul_duree(f_y,L_jobs,nb_machines)[0]<duree_opt:
            duree_opt=duree
            liste_jobs=liste_job
            liste_indice=calcul_duree(f_y,L_jobs,nb_machines)[2]
        ectp=stats.stdev(Tab)
        moy=stats.mean(Tab)
        ectp_norm=ectp/moy
            
        compteur+=1
        compteur_un_colonne=sum(f_y)
        compteur_un=sum(compteur_un_colonne)
        #print(f_y,compteur_un)
 
        
        # #Méthode à notre sauce
        # file_attente(Tab, calcul_duree(f_y, L_jobs))
        # #A faire #Ajoute la valeur de la durée correspondante dans Tab
        # Y=Y_t_plus_1(L_jobs, Y) #Maj de la valeur de Y(t)
        # f_y=f(Y,L_jobs)
        # compteur+=1
    
    
    compteur_un_colonne=sum(f_y)
    compteur_un=sum(compteur_un_colonne)
    
    return (duree_opt,liste_indice)


        
j0=job.Job(0,[54,79,16,66,58])
j1=job.Job(1,[83,3 ,89, 58, 56])
j2=job.Job(2,[15, 11, 49, 31, 20 ])
j3=job.Job(3,[71, 99, 15, 68, 85])
j4=job.Job(4,[77, 56, 89, 78, 53])
j5=job.Job(5,[36, 70, 45, 91, 35 ])
j6=job.Job(6,[53, 99, 60, 13, 53])
j7=job.Job(7,[38, 60, 23, 59, 41])
j8=job.Job(8,[27, 5, 57, 49, 69 ])
j9=job.Job(9,[87, 56, 64, 85, 13 ])
j10=job.Job(10,[76, 3, 7, 85, 86  ])
j11=job.Job(11,[91, 61, 1, 9, 72  ])
j12=job.Job(12,[14, 73, 63, 39, 8 ])
j13=job.Job(13,[29, 75, 41, 41, 49 ])
j14=job.Job(14,[12, 47, 63, 56, 47 ])
j15=job.Job(15,[77, 14, 47, 40, 87 ])
j16=job.Job(16,[32, 21, 26, 54, 58 ])
j17=job.Job(17,[87, 86, 75, 77, 18 ])
j18=job.Job(18,[68, 5, 77, 51, 68 ])
j19=job.Job(19,[38, 60, 23, 59, 41])

l=[j0,j1,j2,j3,j4,j5,j6,j7,j8,j9,j10,j11,j12,j13,j14,j15,j16,j17,j18,j19]



        
        

    

    
            
