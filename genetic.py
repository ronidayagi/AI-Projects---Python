import os.path
import random
import numpy as np

#you define
# Configuration
population_size = 10
target          = 'david'
mutation_rate   = 0.1
inputBolean=True


dic=[]
population=[]
population_fitness=[]

def readDict(fname,dest):
  """
  Description:
  Reads the dictionary file into a string list.
  1. The function creates a file with duplicates removed.    
  2. The file entries are converted to lower case.
  3. A cahch file is created in order to speed up processing
  """
  clines=[]  
  if(os.path.exists(dest)):
    # cache file exist - read from the cache  
    f = open(dest, "r")
    clines=f.readlines()
    f.close()
    for i in range(0,len(clines)):
      clines[i]=clines[i].strip()  
  else:    
    # cache file not created yet  
    # read the orginal file
    f = open(fname, "r")
    lines=f.readlines()
    f.close()
    # create a clean list
    for i in range(0,len(lines)):
      word=lines[i].strip().lower()
      if word not in clines:
        clines.append(word)
    # create the cache file    
    f = open(dest, "w")
    for i in range(0,len(clines)):
       f.write(clines[i]+'\n') 
    f.close()
  return clines 

def selectPopulation(word_len,num=10):
  """
  Description:
  randomizes a population of words.
  the population shall contain num items.
  the population shall contain words with word_len characters    
  """  
  # create the list of words with an adequate length
  total_pop=[]  
  for i in range (0,len(dic)):
    if(len(dic[i])==word_len):
       total_pop.append(dic[i])
       
  # from these list, select the population      
  selected_pop=random.choices(population=total_pop,k=num)                      # select randomly with weight two parents     
  return selected_pop   

def calculatePopulationfitness(pop,word,exp=2.0):
  """
  Description:
  Calculates the fitness of each item in the population.
  Fitness is defined as a number from 0.0 to 1.0
  """  
  l=len(word)
  pop_fitness=[]
  for i in range(0,len(pop)):
    ref=pop[i]  
    match=0.0
    for j in range(0,l):
      if(word[j]==ref[j]):
        match += 1.0
    pop_fitness.append(pow(match/l,exp))                                       #exp=2 beacuse i want that a small erorr will have bigger chance
  return pop_fitness      

def selectParents(population,fitness,n=2):
  """
  Description:
  randomly selects two items from the population list.
  each item will have a selection probability in the fitness list    
  """
  indexs=range(0,len(population))                                              # create a list of the population indecies
  parents=random.choices(population=indexs,weights=fitness,k=n)                # select randomly with weight two parents
  return parents  

def createChild(father,mother):
  """
  Description:
  Create a child by adding half of the father characters with half from the mother    
  """
  n=len(father)
  fn=int(n/2)
  child=father[0:fn]+mother[fn:]  
  return child      

def mutateChild(child,rate=0.01):
  """
  Description:
  adds a mutation to a child
  """
  mutated=''
  for i in range(0,len(child)):
    gene_pool='abcdefghijklmnopqrstuvwxyz'  
    if(random.random() <= rate):                                               # if a mutation should be applied
      gene=random.randint(0,len(gene_pool)-1)                                  # randomly selec a mutation
      mutated += str(gene_pool[gene])                                          # replace the original char with the mutated one
    else:
      mutated += str(child[i])  
  return mutated 



def mainGenetic(start,target,inputBolean)
  found=False    
  generation=0
  dic                  = readDict('d.txt','dd.txt')                             
  population           = selectPopulation(len(target),10)                      # select initial population
  while(found==False) & (generation<10000):
    population_fitness = calculatePopulationfitness(population,target)         # calculate the fittness of each element in population
    parents            = selectParents(population,population_fitness)          # select the parents based of fittness probability
    child              = createChild(father=population[parents[0]],mother=population[parents[1]]) # create a child from the two parents
    mutated            = mutateChild(child,rate=mutation_rate)                 # mutate the child with a probability rate  
    
    #replace the least fittest with the mutated child
    if mutated not in population:
      min_index             = np.argmin(population_fitness)                    # find the index of the least fittest member in population
      population[min_index] = mutated                                          # replace least fittest with mutated
      
    # check if we found the target  
    if(mutated==target):
      found=True    
    generation += 1 
    if(inputBolean):
      print('the population is:',population)  
      
    print('Father=[{fa}] Mother=[{mo}] target=[{f}] Child=[{c}] Mutation=[{m}]'.format(fa=population[parents[0]],mo=population[parents[1]],f=target,c=child,m=mutated))
  if(found):
    print('Found after %d generations' % generation)  
  else:
    print('Not found')  
    
