import outils
import copy
import time


def T0(j, l, s):
    if (l == 0) :
        return True
    if (l >= 1) :
        if j < s[l-1] - 1 :
            return False
        if j == s[l-1] - 1 :
            return l <= 1
        else :
            return T0(j - 1, l, s) or T0(j - s[l-1] - 1, l - 1, s) 

def is_not(li,fin,color):
  for i in range(fin):
    if li[i] == color:
      return False
  return True

def put_block(li,first,nb):
  if li[first] == 1:
    return False
  for i in range(first + 1,first+nb):
    if li[i] == -1:
      return False
  return True

def T_mem(j, l, s, li,dict):
  if (j,l) in dict :
    return dict[(j,l)]
  elif l == 0:
   dict[(j,l)] =  is_not(li,j+1,1)
  elif j < s[l-1] - 1:
    dict[(j,l)] = False
  elif j == s[l-1] - 1:
    if l > 1:
      dict[(j,l)] = False
    else:
      dict[(j,l)] = is_not(li,j+1,-1)
  else:
    if li[j] == -1:
        dict[(j,l)] = T_mem(j-1, l, s, li,dict)
    elif li[j] == 1:
        dict[(j,l)] = put_block(li,j-s[l-1],s[l-1]) and T_mem(j-s[l-1]-1, l-1, s, li,dict)
    else:
        dict[(j,l)] = (put_block(li,j-s[l-1],s[l-1]) and T_mem(j-s[l-1]-1, l-1, s, li,dict)) or T_mem(j-1, l, s, li,dict)
  return dict[(j,l)]

def colorlig(A, i,j, blocs,nouveaux):
  L = len(A[i])-1
  l = len(blocs)
  if j == -1:
    return True,A,nouveaux
  if A[i][j] != 0 :
    if not(T_mem(L,l,blocs,A[i],dict())):
      return False, outils.init(1, 1), set()
    return colorlig(A,i,j-1,blocs,nouveaux)
  A[i][j] = 1
  black = T_mem(L,l,blocs,A[i],dict())
  A[i][j] = -1
  white = T_mem(L,l,blocs,A[i],dict())
  if not(black) and not(white):
    return False, outils.init(1, 1), set()
  elif not(white) and black:
      A[i][j] = 1
      nouveaux.add(j)
      return colorlig(A,i,j-1,blocs,nouveaux)
  elif white and not(black):
      A[i][j] = -1
      nouveaux.add(j)
      return colorlig(A,i,j-1,blocs,nouveaux)
  else:
    A[i][j] = 0
    return colorlig(A,i,j-1,blocs,nouveaux)
  

def colorcol(A, i ,blocs):
  l = len(blocs)
  li = [A[j][i] for j in range(len(A))]
  c = set()
  L = len(li) -1
  for j in range(L+1):
    if li[j] != 0:
      if not(T_mem(L, l, blocs, li,dict())):
        return False, outils.init(1, 1), set()
      continue
    li[j] = 1
    black = T_mem(L, l, blocs, li,dict())
    li[j] = -1
    white = T_mem(L, l, blocs, li,dict())
    if not(black) and not(white):
      return False, outils.init(1, 1), set()
    elif not(white) and black:
      A[j][i] = 1
      c.add(j)
    elif white and not(black):
      A[j][i] = -1
      c.add(j)
    li[j] = 0
  return True, A, c
    
      
def coloration(fichier_source):
  s_lignes, s_colonnes, nb_lignes, nb_colonnes = outils.lecture(fichier_source)
  A = outils.init(nb_lignes, nb_colonnes)
  ligne_a_voir = {i for i in range(nb_lignes)}
  colonne_a_voir = {i for i in range(nb_colonnes)} 
  while len(ligne_a_voir) != 0 or len(colonne_a_voir) != 0:
    for i in ligne_a_voir:
      ok, A, c = colorlig(A, i,nb_colonnes-1, s_lignes[i],set())
      if not(ok):
        return "F", outils.init(nb_lignes,nb_colonnes)
      colonne_a_voir.update(c)
    ligne_a_voir = set()
    for j in colonne_a_voir:
      ok, A, l = colorcol(A,j, s_colonnes[j])
      if not(ok):
        return "F", outils.init(nb_lignes, nb_colonnes)
      ligne_a_voir.update(l)
    colonne_a_voir = set()
  if outils.matrice_complete(A):
    return "T", A
  return "N", A


def colorierEtPropager(A, i, j, c, s_lignes, s_colonnes):
  nb_lignes, nb_colonnes = outils.taille(A)
  A[i][j] = c
  ligne_a_voir = {i}
  colonne_a_voir = {j}  
  while len(ligne_a_voir) != 0 or len(colonne_a_voir) != 0:
    for i in ligne_a_voir:
      ok, A, cl = colorlig(A, i,nb_colonnes-1, s_lignes[i],set())
      if not(ok):
        return "F", outils.init(nb_lignes,nb_colonnes)
      colonne_a_voir = colonne_a_voir.union(cl)
    ligne_a_voir = set()
    for j in colonne_a_voir:
      ok, A, li = colorcol(A, j, s_colonnes[j])
      if not(ok):
        return "F", outils.init(nb_lignes, nb_colonnes)
      ligne_a_voir = ligne_a_voir.union(li)
    colonne_a_voir = set()
  if outils.matrice_complete(A):
    return "T", A
  return "N", A



def enum_rec(A, k, c, s_lignes, s_colonnes):
  M, N = outils.taille(A)
  if k == M * N: 
    return True, A
  i = int(k/M)
  j = k % M
  
  ok, B = colorierEtPropager(A, i, j, c, s_lignes, s_colonnes)
  if ok == "F":
    return False, outils.init(1, 1)
  if ok == "T":
    return True, B

  while A[i][j] != 0:
    k = k + 1
    i = int(k/M)
    j = k % M

  A1 = copy.deepcopy(B)
  ok1, A1 = enum_rec(A1, k, -1, s_lignes, s_colonnes)
  if ok1:
    return ok1, A1
  return enum_rec(B, k, 1, s_lignes, s_colonnes)


def enum(fichier_source):
  s_lignes, s_colonnes, _, _ = outils.lecture(fichier_source)
  ok, A = coloration(fichier_source)
  if ok == "F":
    return False, outils.init(1, 1)
  elif ok == "T":
    return True, A
  A1 = copy.deepcopy(A)
  ok1, A1 = enum_rec(A1, 0, -1, s_lignes, s_colonnes)
  if ok1:
    return ok1, A1
  return enum_rec(A, 0, 1, s_lignes, s_colonnes)