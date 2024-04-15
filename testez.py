import random
import math

# Constants and function definition
myFunction = "-x^2 + x + 2"
a = -1
b = 2
population = 20
precision = 6 
recombinationProbability = 0.25
mutationProbability = 0.01
steps = 50

def calculateFunction(x):
    return -x**2 + x + 2

# Determine chromosome length
dimensionChromosome = math.ceil(math.log2((b-a)*(10**precision)))

with open("Evolutie1.txt", "w") as f:
    # Initialize population
    myDict = {}
    for i in range(1, population+1):
        x = [random.randint(0,1) for j in range(dimensionChromosome)]
        binaryChromosome = ''.join(str(z) for z in x)
        intChromosome = int(binaryChromosome, 2)
        c = ((b-a) / (2**dimensionChromosome - 1))*intChromosome + a
        c = round(c, 6)
        myDict[i] = [binaryChromosome, c, round(calculateFunction(c), precision)]
    
    # Log initial population
    f.write("Initial Population:\n")
    for key, value in myDict.items():
        f.write(f"{key}: {value[0]} x= {value[1]} f= {value[2]}\n")
    
    # Evolution process
    generation = 0
    while generation < steps:
        # Calculate total fitness
        fitnessTotal = sum(chromosome[2] for chromosome in myDict.values())
        
        # Selection using roulette wheel
        selectionProb = [chromosome[2] / fitnessTotal for chromosome in myDict.values()]
        intervals = [sum(selectionProb[:i+1]) for i in range(len(selectionProb))]
        selectedChromosomes = []
        for _ in range(population):
            u = random.random()
            for i, interval in enumerate(intervals):
                if u <= interval:
                    selectedChromosomes.append(i + 1)
                    break

        # Create new dictionary after selection
        newDict = {i: myDict[chrm] for i, chrm in enumerate(selectedChromosomes, 1)}

        # Crossover
        for i in range(1, population, 2):
            if random.random() < recombinationProbability:
                p = random.randint(0, dimensionChromosome - 1)
                x = newDict[i][0]
                y = newDict[i+1][0]
                newX = y[:p] + x[p:]
                newY = x[:p] + y[p:]
                newDict[i][0] = newX
                newDict[i+1][0] = newY

        # Mutation
        for i in range(1, population+1):
            chromosome = list(newDict[i][0])
            for j in range(len(chromosome)):
                if random.random() < mutationProbability:
                    chromosome[j] = '1' if chromosome[j] == '0' else '0'
            newDict[i][0] = ''.join(chromosome)
            aux = int(newDict[i][0], 2)
            c = ((b-a) / (2**dimensionChromosome - 1))*aux + a
            c = round(c, precision)
            newDict[i][1] = c
            newDict[i][2] = round(calculateFunction(c), precision)

        # Update myDict for the next generation
        myDict = newDict

        # Calculate max and average fitness
        maxFitness = max(chromosome[2] for chromosome in myDict.values())
        avgFitness = sum(chromosome[2] for chromosome in myDict.values()) / population

        # Log max and average fitness
        f.write(f"Generation {generation+1}: Max Fitness = {maxFitness}, Average Fitness = {avgFitness}\n")
        
        generation += 1
