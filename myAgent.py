import numpy as np
import random
import matplotlib.pyplot as plt

playerName = "myAgent"
nPercepts = 75  # This is the number of percepts
nActions = 5  # This is the number of actions
stored_fitness = []

#train against random for 300 generations and self for 50 generations
trainingSchedule = [("random", 300), ("self", 50)]



#class for creature/agent

class MyCreature:

    #initialisation of chromosome into 4-dimensional array
    def __init__(self):
        self.chromosome = np.random.randn(5, 5, 5, 3)

    #function to allow accessing the creature's chromosome using indices
    def __getitem__(self, item):
        return self.chromosome[item]

    #function mapping percepts to actions, with different behaviour for different chromosomes and percepts
    #takes chromosome and percepts as parameters
    #returns array of actions, where the index with the highest value is the action to be taken
    def AgentFunction(self, percepts):
        # 0 - move left
        # 1 - move up
        # 2 - move right
        # 4 - eat

        actions = np.zeros((nActions))

        for i in range(5):
            actions[i] = np.sum(np.multiply(self.chromosome[i], percepts))

        return actions


#Function returning a new population of creatures and the average fitness of the old population
#takes the old population of creatures as a parameter
def newGeneration(old_population):
    #length of population
    N = len(old_population)

    #initialise fitness array for all of the old population
    fitness = np.zeros((N))


    #iterate over old population and append to the fitness array based on a fitness function that gives a score to each creature
    for n, creature in enumerate(old_population):

        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies
        # creature.squares_visited - how many different squares the creature visited
        # creature.bounces - how many times the creature bounced


        fitness[n] = 112*creature.size + 86*creature.enemy_eats + 61*creature.strawb_eats + 16*creature.alive + 10*creature.squares_visited

    #declare a list of a new population
    new_population = list()
        
    #function for selecting new parents, taking a population into account and choosing parents
    #randomly, with probability weightings based on fitness scores
    #returns two new parents
    def select(set):
        parent_a = random.choices(set, weights=fitness)[0]
        parent_b = random.choices(set, weights=fitness)[0]
        return parent_a, parent_b

    #function for crossing the chromosomes of two parents (which are taken as parameters)
    #single point crossover with a randomly chosen split point
    def crossover(parent_a, parent_b):
        split = random.randint(1, (len(parent_a.chromosome) - 1))
        child = MyCreature()
        chr_a = parent_a.chromosome[:split]
        chr_b = parent_b.chromosome[split:]
        child.chromosome = np.concatenate((chr_a, chr_b))
        return child

    #choose elites by first sorting fitness array to get indices with the highest values of fitness scores
    #then iterate over to append the creatures at these indices to the new population
    sorted_arr = np.argsort(fitness)
    sorted_indices = sorted_arr[(len(sorted_arr) - 5):(len(sorted_arr))]

    for x in range(5):
        ind = sorted_indices[x]
        creat = MyCreature()
        creat = old_population[ind]
        new_population.append(creat)


    #iterate the required number of times (population size minus elites) to generate new population
    for n in range(N-5):

        #create new creature
        new_creature = MyCreature()

        #select two parents and crossover their chromosomes to create the new creatures chromosome
        par_a, par_b = select(old_population)
        new_creature = crossover(par_a, par_b)
        #perform mutation with a chance of 1%
        #if mutation is to occur, randomly select indices and fill with random float
        rnd = random.randint(1, 100)
        if rnd <= 1:
            r = random.randint(0, 4)
            s = random.randint(0, 4)
            t = random.randint(0, 2)
            u = random.random()
            new_creature.chromosome[r, s, t] = u

        #append newly created creature to the new population
        new_population.append(new_creature)

    #compute average fitness
    avg_fitness = np.mean(fitness)
    #store fitness scores in an array and plot (commented out for convenience)
    #stored_fitness.append(avg_fitness)
    #plt.plot(stored_fitness)
    #plt.show()

    #return the new population and the average fitness
    return (new_population, avg_fitness)

