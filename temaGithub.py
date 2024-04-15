import copy
import math
import random

#functia de maximizat, coeficientii fiind cititi la input
def myF(x, c):
    return c[0]*(x**2) + c[1]*x + c[2]

n = 20
a = -1
b = 2
coef = [-1, 1, 2]
precision = 6
pr = 0.25
pm = 0.01
stages = 50

g = open("Evolutie.txt", "w")

#formula din curs pentru discretizarea intervalului si calculul lungimii cromozomului
dimC = math.ceil(math.log2((b-a)*(10**precision)))
chromosomes = [[random.randint(0, 1) for j in range(dimC)] for i in range(n)] #fiecare gena este generata aleator la inceput

for stage in range(1, stages+1):
    if stage == 1:
        g.write("Populatia initiala\n")
    sumF = 0
    X = []
    Maxfittest = float('-inf')
    fittest = 0
    for i in range(n):
        b2string = ''.join([str(x) for x in chromosomes[i]])
        x = int(b2string, 2) #transform sirul de biti in baza 10
        interpolateX = ((b-a) / (2**dimC - 1))*x + a #formula din curs pentru valoarea codificata a unui cromozom (interpolarea sa pe D)
        print(x, interpolateX)
        X.append(interpolateX) #salvez toti x's corespunzatori cromozomilor
        if stage == 1:
            g.write(str(i+1) + " : " + b2string + " x= " + str(round(interpolateX, precision)) + " f= " + str(myF(round(interpolateX, precision), coef)))
            g.write('\n')
        sumF += myF(interpolateX, coef)
        if myF(round(interpolateX, precision), coef) > Maxfittest: #de asemenea calculez si cel mai fittest cromozom sa-l trec direct in etapa urmatoare
            Maxfittest = myF(round(interpolateX, precision), coef)
            fittest = i

    fittestch = chromosomes[fittest].copy()

    if stage == 1:
        g.write("\nProbabilitati selectie\n")
    probSelection = []
    for i in range(n):
        probSelection.append(myF(X[i], coef) / sumF) #probabilitatile de selectie prin metoda ruletei
        if stage == 1:
            g.write("cromozom " + str(i+1) + " probabilitate " + str(myF(X[i], coef) / sumF))
            g.write('\n')

    if stage == 1:
        g.write("\nIntervale probabilitate selectie\n")
    intervalsProbSel = [0]
    sumI = probSelection[0]
    intervalsProbSel.append(sumI)
    if stage == 1:
        g.write("0 " + str(sumI) + " ")
    for i in range(1, n):
        sumI += probSelection[i]
        intervalsProbSel.append(sumI) #intervalele ca fiind suma a probabilitatilor
        if stage == 1:
            g.write(str(sumI) + " ")


    def findI(u, v, st, dr): #cautarea binara pentru a gasi intervalul potrivit pentru un u dat
        global last
        while st <= dr:
            mij = (st + dr) // 2
            if v[mij] <= u:
                last = mij
                st = mij+1
            elif v[mij] > u:
                dr = mij-1
        return last+1

    if stage == 1:
        g.write("\n\n")
    selected = [0 for _ in range(n)]
    for i in range(n):
        u = random.random() #generez un u random pe care il caut binar in lista de probabilitati de selectie
        cr = findI(u, intervalsProbSel, 0, n) - 1
        if stage == 1:
            g.write("u= " + str(u) + " selectam cromozomul " + str(cr+1))
            g.write('\n')
        selected[i] = cr #ma folosesc de selected pentru a vedea ce cromozomi trec de selectie

    if stage == 1:
        g.write("\nDupa selectie\n")
    cc = []
    for i in range(n):
        if stage == 1:
            g.write(str(i+1) + ": " + ''.join([str(x) for x in chromosomes[selected[i]]]) + " x= " + str(round(X[selected[i]], precision)) + " f= " + str(myF(X[selected[i]], coef)))
            g.write('\n')
        cc.append(chromosomes[selected[i]])
    chromosomes = copy.deepcopy(cc) #copiez toti cromozomii care au trecut de selectie in lista initiala chromosomes si trec mai departe

    if stage == 1:
        g.write("\nProbabilitatea de incrucisare " + str(pr) + "\n")
    recomb = []
    for i in range(n):
        u = random.random() #generez un u random si pentru fiecare cromozom daca acest u este mai mic decat probabilitatea de incrucisare trec indicele cromozomului intr-un vector recomb
        if u < pr:
            if stage == 1:
                g.write(str(i+1) + ": " + ''.join([str(x) for x in chromosomes[i]]) + " u= " + str(u) + "<" + str(pr) + " participa\n")
            recomb.append(i)
        else:
            if stage == 1:
                g.write(str(i+1) + ": " + ''.join([str(x) for x in chromosomes[i]]) + " u= " + str(u) + "\n")

    if stage == 1:
        g.write('\n')
    while len(recomb) > 1: #recomb = lista de indici!
        i = random.randrange(len(recomb)) #iau un i random si un j tot la fel de radom (aici pot fi alese mai multe metode de alegere) si incrucisez cromozomii recomb[i] recomb[j]
        j = len(recomb)-i-1
        if i == j:
            continue
        if stage == 1:
            g.write("Recombinare dintre cromozomul " + str(recomb[i]+1) + " cu cromozomul " + str(recomb[j]+1) + "\n")
        pct = random.randrange(dimC) #punctul de la care se realizeaza incrucisarea
        if stage == 1:
            g.write(''.join([str(x) for x in chromosomes[recomb[i]]]) + " " + ''.join([str(x) for x in chromosomes[recomb[j]]]) + " punct " + str(pct) + "\n")
        chcopy = chromosomes[recomb[i]][:pct+1].copy() #incrucisarea
        chromosomes[recomb[i]][:pct+1] = chromosomes[recomb[j]][:pct+1].copy()
        chromosomes[recomb[j]][:pct+1] = chcopy.copy()
        if stage == 1:
            g.write("Rezultat " + ''.join([str(x) for x in chromosomes[recomb[i]]]) + " " + ''.join([str(x) for x in chromosomes[recomb[j]]]) + "\n")

        aux = [recomb[k] for k in range(len(recomb)) if k != i and k != j] #elimin indicii i si j din recomb
        recomb = aux.copy()

    if stage == 1:
        g.write("\nDupa recombinare\n")
    for i in range(n):
        b2string = ''.join([str(x) for x in chromosomes[i]])
        x = int(b2string, 2)
        interpolateX = ((b - a) / (2 ** dimC - 1)) * x + a #caluclez din nou valorile x pentru noii cromozomi
        X[i] = interpolateX
        if stage == 1:
            g.write(str(i + 1) + " : " + b2string + " x= " + str(round(interpolateX, precision)) + " f= " + str(myF(round(interpolateX, precision), coef)))
            g.write('\n')

    if stage == 1:
        g.write("\nProbabilitate de mutatie pentru fiecare gena 0.01\n")
        g.write("Au fost modificati cromozomii:\n")
    for i in range(n):
        u = random.random() #generez un u random si pentru cromozomii cu u<probabilitatea de mutatie, schimb un bit de pe pozitia poz care e si ea generata random
        if u < pm:
            poz = random.randrange(dimC)
            chromosomes[i][poz] = 1-chromosomes[i][poz]
            if stage == 1:
                g.write(str(i+1) + "\n")

    if stage == 1:
        g.write("\nDupa mutatie:\n")
    Max = float('-inf')
    worstVal = float('inf')
    worst = 0
    medValSum = 0
    for i in range(n):
        b2string = ''.join([str(x) for x in chromosomes[i]])
        x = int(b2string, 2)
        interpolateX = ((b - a) / (2 ** dimC - 1)) * x + a #la final recalculez din nou valorile x dupa mutatii
        X[i] = interpolateX
        if stage == 1:
            g.write(str(i + 1) + " : " + b2string + " x= " + str(round(interpolateX, precision)) + " f= " + str(myF(round(interpolateX, precision), coef)))
            g.write('\n')
        Max = max(Max, myF(round(interpolateX, precision), coef)) #valoarea maximizata a functiei
        medValSum += myF(round(interpolateX, precision), coef) #ajuta la calculul valorii medii a performantei
        if myF(round(interpolateX, precision), coef) < worstVal: #totodata vreau sa vad cromozomul cu worst performance pentru a-l inlocui cu cel mai fittest pe care l-am ales la inceput
            worstVal = myF(round(interpolateX, precision), coef) #deoarece folosim selectia de tip elitist, cel mai fittest trece automat mai departe
            worst = i

    chromosomes[worst] = fittestch.copy()
    Max = max(Max, Maxfittest)
    medValSum = medValSum - worstVal + Maxfittest

    if stage == 1:
        g.write("\n\nEvolutia maximului\n")
    g.write("Population " + str(stage+1) + " maxValue= " + str(Max) + " medium performance: " + str(medValSum/n) + "\n")

g.close()