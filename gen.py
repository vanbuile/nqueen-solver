
from datetime import datetime
import random

Board_Size = int(input("Enter size of Board: "))   # Number of Queens
PopulationSize = 2 * Board_Size              # Maximum number of people can live in environment
Population = list()                         # Environment
max_children = PopulationSize//3            # Maximum number of children
max_offspring = 2                           # Maximum number of offspring per crossover
crossoverProbability = 0.5                  # Probability of crossover
mutationProbability = 0.95                 # Probability of mutation


# fitness function
# return number of couple attack
def fitness(chroe):
    sum = 0
    for i in range(Board_Size):
        for j in range(i + 1, Board_Size):
            if abs(j - i) == abs(chroe[j] - chroe[i]):
                sum = sum + 1
    return sum


# parent selection function
# tournament technique
def parent_selection():
    tmp = (list(), Board_Size)
    for _ in range(PopulationSize // 5):
        ch = random.choice(Population)
        if ch[-1] < tmp[1]:
            tmp = (ch, ch[-1])
    return tmp[0]


# crossover function
# PMX technique
def crossover(parent1, parent2):
    children = list()
    for _ in range(random.randint(1, max_offspring)):
        child = [-1]*(Board_Size + 1)
        p, q = random.randint(1, Board_Size//2 - 1), random.randint(Board_Size//2 + 1, Board_Size - 2)
        child[p: q+1] = parent1[p: q+1]
        for i in range(p, q+1):
            if parent2[i] not in child:
                t = i
                while p <= t <= q:
                    t = parent2.index(parent1[t])
                child[t] = parent2[i]
        for j in range(Board_Size):
            if child[j] == -1:
                child[j] = parent2[j]
        child[-1] = fitness(child)
        children.append(child)
        parent1, parent2 = parent2, parent1
    return children


# mutation function
# single swap technique
def mutation(chroe):
    p, q = random.randint(0, Board_Size - 1), random.randint(0, Board_Size - 1)
    chroe[p], chroe[q] = chroe[q], chroe[p]
    chroe[-1] = fitness(chroe)


if __name__ == "__main__":
    fitness_list = list()
    iteration_count = 0
    start_time = datetime.now()

    # initializing PopulationSize chromosome
    for _ in range(PopulationSize):
        chromosome = list(range(1, Board_Size + 1))   #1,2,3 Board_size
        random.shuffle(chromosome) # shuffle the list
        chromosome.append(fitness(chromosome)) 
        Population.append(chromosome)

    # sorting Population with fitness key
    Population.sort(key = lambda q: q[-1])
    fitness_list.append(Population[0][-1])  # the best value

    # starting algorithm
    while Population[4][-1]:
        random.shuffle(Population)
        # recombine parents
        new_children = list()
        for _ in range(max_children):
            p1, p2 = parent_selection(), parent_selection()
            done = False
            if random.random() < crossoverProbability:
                children = crossover(p1, p2)
                done = True
            else:
                children = [p1[:], p2[:]]
            for child in children:
                if random.random() < mutationProbability or not done:
                    mutation(child)
                new_children.append(child)
        Population.extend(new_children)

        # kill people with upper fitness (goal : minimizing fitness)
        Population.sort(key=lambda q: q[-1]) # sort by fitness
        del Population[PopulationSize:]
        fitness_list.append(Population[0][-1])
        iteration_count += 1

    end_time = datetime.now()
    del Population[0][-1]
    # print("%dth iteration, current fitness: %d" % (iteration_count, 0))
    print("Solution for %d Queen is: %s" % (Board_Size, str(Population[0])))
    print("total time for solution is %s" % (str(end_time - start_time)))



