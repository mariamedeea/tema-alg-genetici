import random
import math
myFunction = "-x^2 + x + 2"
a = -1
b = 2
population = 20
precision = 6 
recombinationProbability = 0.25
mutationProbability = 0.01
steps = 50

myChromosomes = []
myDict = {}

def calculateFunction(x):
    return -x**2 + x + 2


dimensionChromosome = math.ceil(math.log2((b-a)*(10**precision)))

with open("Evolutie1.txt", "w") as f:
    # primul pas, aflam populatia
    fitnessTotal  = 0
    for i in range(1, population+1):
        
        x = [random.randint(0,1) for j in range(dimensionChromosome)]
        binaryChromosome = ''
        
        for z in x:
            binaryChromosome=binaryChromosome+str(z)
        intChromosome = int(binaryChromosome, 2)

        # vrem sa aflam care este valoarea codificata a lui intChromosome
        c = ((b-a) / (2**dimensionChromosome - 1))*intChromosome + a
        c = round(c, precision)
        myDict[i] = [binaryChromosome, c, round(calculateFunction(c), precision)]
        fitnessTotal = fitnessTotal + round(calculateFunction(c), precision)


    elite_idx = max(myDict, key=lambda x: myDict[x][2])
    elite_chromosome = myDict[elite_idx]

    f.write("\n")
    f.write("Populatia initiala:\n")

    counter = 1
    for x in myDict:
        f.write(str(counter) + ": " + str(myDict[x][0]) + " x= " + str(myDict[x][1]) + " f= " + str(myDict[x][2]))
        f.write("\n")
        counter = counter+1


    # metoda ruletei 

    for i in range(1, population+1):
        myDict[i].append(calculateFunction(myDict[i][1]) / fitnessTotal)

    f.write("\nProbabilitati selectie\n")

    for i in range(1, population+1):
        f.write("Cromozom " + str(i) + " probabilitate " + str(myDict[i][3]) + "\n")


    f.write("\n" + "Intervale probabilitati selectie\n")
    interval = 0
    intervals = []
    for i in range(1, population+1):
        intervals.append(interval)
        f.write(str(interval) + " ")
        interval = interval + myDict[i][3]

    # generam numere random pe care apoi le cautam binar in probabilitatile de selectie

    f.write("\n")

    def findInterval(u, v):
        low  = 0
        high = len(v) - 1
        result = 0  

        while low <= high:
            mid = (low + high) // 2
            if v[mid] <= u:
                result = mid + 1 
                low = mid + 1
            else:
                high = mid - 1

        return result


    f.write("\n")
    selectedChromosomes = []
    for i in range(1, population+1):
        randomNumber = random.random()
        c = findInterval( randomNumber,intervals)
        f.write("u= " + str(randomNumber) + " selectam cromozomul " + str(c) + "\n")
        selectedChromosomes.append(c)

    newDict = {}

    for idx, selectedIdx in enumerate(selectedChromosomes, start=1):
        newDict[idx] = myDict[selectedIdx]


    f.write("\nDupa selectie\n")
    counter = 1
    for x in newDict:
        f.write(str(counter) + ": " + str(newDict[x][0]) + " x= " + str(newDict[x][1]) + " f= " + str(newDict[x][2]) +"\n")

        counter+=1

    f.write("\nProbabilitate de incrucisare " + str(recombinationProbability) + "\n")

    participants = []
    for i in range(1, population+1):
        u = random.random()
        if u<recombinationProbability:
            f.write(str(i) + ": " + str(newDict[i][0]) + "u= " + str(u) + " < " + str(recombinationProbability) + "participa\n")
            participants.append(i)
        else:
            f.write(str(i) + ": " + str(newDict[i][0]) + "u= " + str(u) + "\n")


    if(len(participants) % 2 == 1):
        participants = participants[:len(participants) - 1]
    
    f.write("\n")
    for i in range(0, len(participants), 2):
        f.write("\nRecombinare intre cromozomul " + str(participants[i]) + " cu cromozomul " + str(participants[i+1]) +"\n" )
        p = random.randint(0, dimensionChromosome)
        f.write(str(newDict[participants[i]][0]) + " " + str(newDict[participants[i+1]][0]) + " punct " + str(p) + "\n") 

        x = newDict[participants[i]][0]
        y = newDict[participants[i+1]][0]

        newX = y[:p] + x[p:]
        newY = x[:p] + y[p:]

        newDict[participants[i]][0] = newX
        aux = int(newX, 2)
        c = ((b-a) / (2**dimensionChromosome - 1))*aux + a
        c = round(c, precision)
        newDict[participants[i]][1] = c
        newDict[participants[i]][2] = round(calculateFunction(c), precision)


        newDict[participants[i+1]][0] = newY
        aux = int(newY, 2)
        c = ((b-a) / (2**dimensionChromosome - 1))*aux + a
        c = round(c, precision)
        newDict[participants[i+1]][1] = c
        newDict[participants[i+1]][2] = round(calculateFunction(c), precision)

        f.write("Rezultat" + str(newDict[participants[i]][0]) + " " + str(newDict[participants[i+1]][0]) + "\n") 


    f.write("\nDupa recombinare\n")
    counter = 1
    for x in newDict:
        f.write(str(counter) + ": " + str(newDict[x][0]) + " x= " + str(newDict[x][1]) + " f= " + str(newDict[x][2]) +"\n")

        counter+=1


    f.write("Probabilitate de mutatie pentru fiecare gena " + str(mutationProbability) + "\n")

    mutations = set()
    for i in range(1, population + 1):
        chromosome = list(newDict[i][0])  # Convert string to list for mutation
        mutated = False
        for j in range(len(chromosome)):
            p = random.random()
            if p <= mutationProbability:
                # Perform mutation
                original = chromosome[j]
                chromosome[j] = '0' if chromosome[j] == '1' else '1'
                mutations.add(i)  # Track which chromosomes mutated
                mutated = True

        if mutated:
            # Update only if any mutation occurred
            newDict[i][0] = ''.join(chromosome)
            aux = int(newDict[i][0], 2)
            c = ((b-a) / (2**dimensionChromosome - 1))*aux + a
            c = round(c, precision)
            newDict[i][1] = c
            newDict[i][2] = round(calculateFunction(c), precision)

    f.write("\nCromozomi care au suferit mutatie:\n")
    for i in mutations:
        f.write(str(i) + "\n")

    f.write("\nDupa mutatie:\n")
    counter = 1
    maxFitness = 0
    sum = 0

        
    for x in newDict:
        if newDict[x][2] > maxFitness:
            maxFitness = newDict[x][2]
        sum = sum + newDict[x][1]
        counter += 1

    avg = sum / population
    
    # Assuming mini and miniIndex need to be initialized
    mini = float('inf')  # Set to infinity so any real fitness is smaller
    miniIndex = -1  # Initialize to an invalid index
    index = 1  

    for x in range(1, population+1):
        if mini > newDict[x][2]:
            mini = newDict[x][2]
            miniIndex = index
        index += 1

    if miniIndex != -1:
        newDict[miniIndex] = elite_chromosome  # Copy the entire elite chromosome if necessary

    
    counter = 1
    
    f.write("\n")
    for x in newDict:
        f.write(str(counter) + ": " + str(newDict[x][0]) + " x= " + str(newDict[x][1]) + " f= " + str(newDict[x][2]) +"\n")
        counter += 1
    f.write("\n" + str(maxFitness) + " " + str(avg))

    