def lecture(path):
  file = open(path, "r")

  # variables qui servent à stocker ce qu'on va lire
  s_lignes = []
  s_colonnes = []
  nb_lignes = 0
  nb_colonnes = 0

  # variable qui sert a savoir si on doit rajouter un bloc dans s_lignes et s_colonnes
  b = True

  for line in file :
    bloc = []

    if line.startswith('#') :
      b = False

    else :
      bloc = []
      a = ""
      for c in line:
        if (c == ' ' or c == '\n') and a != '':
          bloc.append(int(a))
          a = ""
        else:
          a = a + c

      if b :
        s_lignes.append(bloc)
        nb_lignes = nb_lignes + 1
      else :
        s_colonnes.append(bloc)
        nb_colonnes = nb_colonnes + 1

      bloc = []
      
  file.close()
  
  return s_lignes, s_colonnes, nb_lignes, nb_colonnes


def init(n, m):
  res = []
  for i in range(n):
    add = [0 for j in range(m)]
    res.append(add)
  return res


def setN(M, i, j):
  M[i][j] = 1

def setB(M, i, j) :
  M[i][j] = -1

def affichage(M):
  for i in range(len(M)):
    for j in range(len(M[i])):
      if M[i][j] == 0 :
        print("x ", end='')
      elif M[i][j] == 1 :
        print("■ ", end='')
      elif M[i][j] == -1 :
        print("  ", end='')
    print()

def matrice_complete(M):
  for i in range(len(M)) :
    for j in range(len(M[i])) :
      if M[i][j] == 0:
        return False
  return True

def taille(A):
  return len(A), len(A[0])
