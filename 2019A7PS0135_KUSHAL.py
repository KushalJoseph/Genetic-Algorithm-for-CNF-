import numpy as np
import time
from random import randrange
from CNF_Creator import *
from functools import cmp_to_key


# Global Variables
variables = 50            # Boolean varibles, for which we need to find the correct assignment
clauses = 0               # Number of clauses in the sentence
iterations = 0           
max_iterations = 4000
sentence = None           # Global variable created for the sentence
start_time = None

# Hyperparameters

population_size = 20            # Size of population at each iteration
elitism_rate = 0.7              # Fraction of population moved into next generation
max_mutation_size = 15          # Maximum number of bits that may be mutated 
iterations_to_terminate = 0
if(clauses <= 120):
  iterations_to_terminate = 350
elif(clauses <= 160):
  iterations_to_terminate = 700
elif(clauses <= 220):
  iterations_to_terminate = 1100
elif(clauses <= 300):
  iterations_to_terminate = 1300
else:
  iterations_to_terminate = 1800


def main():

    fitness_values = []
    times = []

    
    global iterations
    iterations = 0

    cnfC = CNF_Creator(n = variables) # n is number of symbols in the 3-CNF sentence
    global sentence, start_time, clauses
    # sentence = cnfC.CreateRandomSentence(m = clauses) # m is number of clauses in the 3-CNF sentence
    # print('Random sentence : ', sentence)

    sentence = cnfC.ReadCNFfromCSVfile()
    print('\nSentence from CSV file : ', sentence)
    clauses = len(sentence)

    start_time = time.time()

    best_value, assignment = genetic_algorithm(sentence)

    fitness_value = (best_value/clauses) * 100
        
        

    best_model = []
    for i in range(variables):
        if(assignment[i] == 0):
            best_model.append(-(i + 1))
        else:
            best_model.append(i + 1)
     
    print('\n\n')
    print('Roll No : 2019A7PS0135G')
    print(f'Number of clauses in CSV file : {len(sentence)}')
    print(f'Best model is: {best_model}')
    print(f'Fitness value of best model : {fitness_value}%.')
    print(f'Time taken : {str(round(time.time() - start_time, 3))} seconds.')
    print('\n\n')



def genetic_algorithm(sentence):
    population = []
    
    # First "population_size" randomly selected states
    for i in range(population_size - 2):
        # Create a random assignment of binary variables.
        assignment = np.random.randint(2, size = variables)
        population.append(assignment)

    all_ones = np.ones(variables)
    all_zeros = np.zeros(variables)
    population.append(all_zeros)
    population.append(all_ones)

    # Evolve the population
    return evolve(assignment, population, sentence)

# Utitility function to help sort 2 variable assignments
def compare(assignment1, assignment2):
    return return_satisfied_clauses(assignment1) - return_satisfied_clauses(assignment2)
       
def evolve(assignment, population, sentence):
    global iterations

    cur_best = 0
    cur_best_at_iteration = 0

    while(iterations < max_iterations):

        if(time.time() - start_time > 44.8):
            return best_value, population[0]

        # Sort the population (reverse) based on their fitness function
        population = sorted(population, reverse = True, key = cmp_to_key(compare))

        best_value = return_satisfied_clauses(population[0])

        if(best_value != cur_best):
          cur_best = best_value
          cur_best_at_iteration = iterations 
        elif(best_value == cur_best):
          if(iterations - cur_best_at_iteration > iterations_to_terminate):
            print("Stopping, as fitness not improving")
            return best_value, population[0]
        
        print(f'At iteration {iterations} : {best_value}')

        # Check if we have fully satisfied the formula
        if(best_value == clauses):
            print("Found correct assignment:")
            print(population[0])
            return best_value, population[0]

        # Choose some members to procreate into the next generation
        next_gen = []
        for i in range(int(population_size * elitism_rate)):
            next_gen.append(population[i])

        # Reproduce pairs of these members and append children to next_gen
        parent1, parent2 = next_gen[0], next_gen[1]
        while(len(next_gen) < population_size):
            child1, child2 = crossover(parent1, parent2)
            if(len(next_gen) < population_size): next_gen.append(child1)
            if(len(next_gen) < population_size): next_gen.append(child2)
            # if(len(next_gen) < population_size): next_gen.append(child3)
            # if(len(next_gen) < population_size): next_gen.append(child4)

            # Pick the best 2 for the next generation
            options = [parent1, parent2, child1, child2]
            options = sorted(options, reverse = True, key = cmp_to_key(compare))

            parent1, parent2 = options[0], options[1]

        # Population = next generation and iterate again
        iterations += 1
        population = next_gen

    
    return best_value, population[0]

# Crossover function, returns 2 children
def crossover(parent1, parent2):
    # 2 point crossover
    point1, point2 = randrange(0, 50), randrange(0, 50)

    if(point1 > point2):
        point1, point2 = point2, point1

    child1 = []
    child2 = []

    for i in range(0, point1):
        child1.append(parent1[i])
        child2.append(parent2[i])

    for i in range(point1, point2):
        child1.append(parent2[i])
        child2.append(parent1[i])

    for i in range(point2, variables):
        child1.append(parent1[i])
        child2.append(parent2[i])

    return mutate(child1), mutate(child2)


# Mutation Function
def mutate(child):
    mutation_size = randrange(1, max_mutation_size)

    mutation_points = np.random.randint(0, variables, size = mutation_size, dtype = int)

    for i in range(len(mutation_points)):
        if(child[mutation_points[i]] == 1):
            child[mutation_points[i]] = 0
        else:
            child[mutation_points[i]] = 1
    return child

# Fitness Function
def return_satisfied_clauses(assignment):
    satisfied_clauses = 0
    for i in range(len(sentence)):
        done = False
        for j in range(3):
            if(sentence[i][j] < 0 and assignment[(-sentence[i][j]) - 1] == 0):
                done = True
                break
            elif(sentence[i][j] > 0 and assignment[sentence[i][j] - 1] == 1):    
                done = True
                break

        if(done == True):
            satisfied_clauses += 1

    return satisfied_clauses

    
if __name__ == '__main__':
    main()
