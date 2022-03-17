# Tema 1 TM accepter in Python, Analiza Algoritmilor
# Nume: Talina Laura-Florina
# Grupa: 324CB

import sys

def read_TM():
    nr_stari = int(input())
    stari_finale = (input()).split()
    dictionar_tranzitii = {}

    # se citesc toate celelalte linii, fiecare reprezentand o tranzitie
    # care este divizata in doua tupluri, unul de doua elemente, reprezentand
    # cheia dictionarului, si celalalt de 3 elemente, reprezentand valoarea
    for line in sys.stdin:
        lista_elem = line.split()
        lista1 = lista_elem[0:2]
        lista2 = lista_elem[2:5]
        dictionar_tranzitii[tuple(lista1)] = tuple(lista2)

    # codificarea masinii este un tuplu, ce contine numarul starilor finale,
    # lista starilor finale si un dictionar al tranzitiilor
    codificare = (nr_stari, stari_finale, dictionar_tranzitii)
    return codificare

# functia "deplasare_cursor" primeste doua cuvinte, si simuleaza deplasarea cursorului
# la dreapta, stanga, sau deloc, in functie de parametrul "pozitie" care
# poate fi L, R sau H
def deplasare_cursor(cuv1, cuv2, pozitie):
    if (pozitie == "R"):
        cuv1 = cuv1 + cuv2[0]

        # acest if trateaza cazul in care stringul cuv2 ar ramane gol,
        # motiv pentru care se adauga un "#"
        if len(cuv2) == 1:
            cuv2 = cuv2 + "#"
        cuv2 = cuv2[1 : len(cuv2)]
    if (pozitie == "L"):
        cuv2 = cuv1[len(cuv1) - 1] + cuv2

        # acest if trateaza cazul in care stringul cuv1 ar ramane gol,
        # motiv pentru care se adauga un "#"
        if (len(cuv1) == 1):
            cuv1 = "#" + cuv1
        cuv1 = cuv1[0 : len(cuv1) - 1]

    return cuv1, cuv2

def step(dictionar, configuratie):
    # se formeaza tuplul, ce reprezinta cheia dupa care se va cauta in
    # dictionar
    stare_initiala = configuratie[1]
    caracter = configuratie[2][0]
    tuplu = (stare_initiala, caracter)

    # daca exista un element avand cheia corespunzatoare tuplului, se
    # memoreaza celelalte trei elementele necesare tranzitiei
    if tuplu in dictionar:
        stare_urm = dictionar[tuplu][0]
        caracter_nou = dictionar[tuplu][1]
        pozitie = dictionar[tuplu][2]
    else:
        return False

    # se simuleaza tranzitia
    cuv1 = configuratie[0]
    cuv2 = configuratie[2]
    cuv2 = caracter_nou + cuv2[1: len(cuv2)]
    cuv1, cuv2 = deplasare_cursor(cuv1, cuv2, pozitie)

    return (cuv1, stare_urm, cuv2)

# functia "string_to_tuple" transforma un string de forma "(#,0,ABC)"
# in tuplul corespunzator
# aceasta functie este utilizata de catre functia "do_step"
def string_to_tuple(string):
    continut = string[1 : len(string) - 1]
    return tuple(continut.split(","))

def afisare_configuratie(configuratie):
    print("(", configuratie[0], ",", configuratie[1], ",",
          configuratie[2], ")", sep = '', end = " ")

def do_step(input, dictionar):
    lista_configuratii = input.split();
    for configuratie in lista_configuratii:
        configuratie_noua = step(dictionar, string_to_tuple(configuratie))
        if configuratie_noua == False:
            print("False", end = " ")
        else:
            afisare_configuratie(configuratie_noua)


def accept(codificare_TM, cuvant):
    # pe baza cuvantului primit, se formeaza o configuratie initiala
    cfg_initiala = ("#", '0', cuvant)
    dictionar = codificare_TM[2]

    while cfg_initiala != False:
        # se verifica daca starea la care s-a ajuns este finala
        if (cfg_initiala[1] in codificare_TM[1]):
            return True
        cfg_urmatoare = step(dictionar, cfg_initiala)
        cfg_initiala = cfg_urmatoare

    return False

def do_accept(codificare_TM, input):
    lista_cuvinte = input.split()
    for cuvant in lista_cuvinte:
        print(accept(codificare_TM, cuvant), end = " ")

def k_accept(codificare_TM, cuvant, k):
    cfg_initiala = ("#", '0', cuvant)
    dictionar = codificare_TM[2]

    i = 0
    while i < k:
        # se verifica daca starea la care s-a ajuns este finala
        if (cfg_initiala[1] in codificare_TM[1]):
            return True
        cfg_urmatoare = step(dictionar, cfg_initiala)
        if (cfg_urmatoare == False):
            return False
        cfg_initiala = cfg_urmatoare
        i += 1

    # verificam ultima configuratie, respectiv starea in care s-a ajuns,
    # in cazul in care nu s-a ajuns deja la o stare finala sau o tranzitie
    # imposibila in interiorul while-ului
    if (cfg_initiala[1] in codificare_TM[1]):
        return True
    return False

def do_k_accept(codificare_TM, input):
    lista_input = input.split()
    i = 0
    for i in range(len(lista_input)):
        # pereche este o lista care contine doua elemente:
        # cuvantul si numarul k
        pereche = lista_input[i].split(",")
        print(k_accept(codificare_TM, pereche[0], int(pereche[1])), end = " ")


def main():
    task = input()
    input_task = input()
    codificare_TM = read_TM()

    if task == "step":
        do_step(input_task, codificare_TM[2])
    if task == "accept":
        do_accept(codificare_TM, input_task)
    if task == "k_accept":
        do_k_accept(codificare_TM, input_task)

if __name__ == '__main__':
    main()