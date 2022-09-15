import random
import math
import os.path
import numpy as np
Words=      []
minimom=    []
dic=        []  
distWords=  []
myK=        []
distBank=   []
F_dist=     []
population= []
population_fitness=[]
path=       []
words=      []

myBestPath= []
maxN=       20
currE=       0
nextE=       1
population_size = 10
mutation_rate   = 0.1
k=          3
myTopK=     [k]


#you define
inputBolean=True
start='house'
target='cuttle'
DetailOutput=4



#%%
def SerchAlgo(start,target,inputBolean,DetailOutput):
    myPath=[]#will be printed
    
    
    if DetailOutput==1:#hill
        ans=letsDoIt(start, target, myPath,0,maxN)
    
    if DetailOutput==2:#simulated
        ans=simulatedAnnealing(myPath,start,target,inputBolean)
        
    if DetailOutput==3:#beam   
        ans=mainBeam(start,target,myPath,k,inputBolean)
        
    if DetailOutput==4:#genetic
        ans= mainGenetic(start,target,inputBolean)
    
    if DetailOutput==5:#A-star 
        ans=mainA_Star(start,target,myPath,inputBolean)
    return ans

#%%read Dic
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

#%%A-Star
def G_of_n(words, dictionary,myPath,target):
    '''
    Description:
    Will add the smallest distance of a given neighbor from the start word
    Add to array all the distance from start word and return it
    '''
    distFromStart=[]
    l=len(myPath)
    for word in words:
      if word not in dictionary:
        dictionary[word]=l 
      if word==target:
        distFromStart.append(0)  
      else:   
        distFromStart.append(dictionary[word])  
                                                                               #optional#print('distance from start is:',distFromStart)  
    return distFromStart      
                  

      
def F_of_n(words,target,dictionary,myPath,inputBolean):
    '''
    Description:
    value of a word is calculated as f(n)=g(n)+h(n) 
    g(n) is the distance from the source word
    h(n) is the huristic to the target
    '''      
    words_distance_start=G_of_n(words,dictionary, myPath,target)               #the distance of all nighbors from start word
    distWords_target=H_of_n(words,target)                                      # the distance of all nighbors from target word
    if (inputBolean):
      print('huristic values are:',distWords_target)
    TotalDist=[]
    for i in range(len(distWords)):
       toTarget=distWords_target[i]
       if toTarget==1:
           TotalDist.append(toTarget) 
       else:
         fromStart=words_distance_start[i]                                     #total=g(word)+h(word)
         TotalDist.append(fromStart+toTarget)
                                                                               #optional#print('Total is:',TotalDist)  
    return  TotalDist

def H_of_n(words, target):
   '''
   Description:
   calculates heuristical distance for every word in words
   heuristical distance is diffiend as the amount of changes needed to combine the target word
   '''
   del distWords[:]
   for i in range (0,len(words)):
      x=distance(words[i],target) 
      distWords.append(x)
                                                                               #optional#print ('distance word:',distWords)
   return distWords

def mainA_Star(start,target,myPath,inputBolean):
    dictionary={}
    found=False
    counter=0
    dic=                               readDict('d.txt','dd.txt')   
    nextWord=start
    myPath.append(nextWord)
    while (found==False) and counter<100:
        words=                         options(nextWord,myPath)                #buid word bank in distance of 1 change
        if(len(words)==0):
          break                                                                #break condition
        F_dist=                        F_of_n(words,target,dictionary, myPath,inputBolean) #the f(n) distance for all neighbors
        nextWord=                      pickOne(F_dist, words)                  #pick out of the best options a random one
                                                                               #optional#print('the next word is:',nextWord)
        myPath.append(nextWord)                                                #add to the nextWord to myPath
        if nextWord==target:          
          found=True                                                           #if we found the target word 
        counter=counter+1 
   
    if(found):
      print('my path is:',myPath )  
    else:
      print('i didnt find a path but this is what i have:',myPath)  
#%%simulated annealing
def simulatedAnnealing (myPath, start, end,inputBolean):
    '''
    Description:
    for every loop will choose two random words from the words in distance 1 (in dic)   
    calculate there energy and compere them 
    if the nextWord improves my E will do it
    else it can be done in a specific chance
    '''
    lastWord=start
    myPath.append(start)
    T=1 
    thisWord=start
    found=False
    
    for t in range(100, 0, -1):   
       
        words=               optionsSimulated(thisWord, lastWord)              #neighbors of word 
        currE=               0.1*distance(thisWord,end)                        # 
        nextWord=            random.choice(words)
        nextE=               0.1*distance(nextWord,end)  
        if(inputBolean):
          print('the words i consider are:',words)  
        if nextE==0:         # break condition
            myPath.append(nextWord)
            return myPath
     
        if(currE-nextE>0):   # improving
           myPath.append(nextWord)
           thisWord=     nextWord
           lastWord=     thisWord
           
        else:                # i want a negative pow
            prob=math.exp((currE-nextE)/T)
            if (random.random()<=prob):
               myPath.append(nextWord)
               thisWord=              nextWord
               lastWord=              thisWord
            else:
              nextWord=random.choice(words) 
              T=T+0.03
        if end in words:    #break condition
            myPath.append(end)
            break
        else:
          T=T-0.01 
        
        myPath.append(t)  
    if (found):
      print('my path is:',myPath) 
    else:
      print('i couldnt find a path but this is my path:',myPath)                                                        #print('my temp is:',T)
    return myPath  
#%%Hill

def execute(start,target,myPath,flag,maxN):
    '''
    Description: recursive func
    Build a bank of words in distance 1 from source word
    Calculate the distance between the words to the target word
    Pick a random word from all the minimom distance options     
    '''
   
    if flag>maxN:#break condition
        return myPath
       
    myPath.append(start)
    words=options(start , myPath)                                              # options from dic on the start word
    
    if(len(words)==0):#break condition
        return myPath
                                                                               #optinal#print ('dic words ',words)
    disWords=distOption(words, target)                                         #distance of every word from target
                                                                               #optional#print ('distance', disWords)
    newPic=pickOne(disWords,words)                                             #randomly choose my next word
                                                                               #optinal#print('my path is',myPath)
                                                                               #optional#print('my newPic',newPic)
    if newPic==target:
       myPath.append(target) 
                                                                               #optinal# print ('the path is',myPath)
       return myPath
    else:
      return  execute (newPic,target,myPath,flag+1,maxN)
    
def letsDoIt(start,target,myPath,flag,maxN):
    '''
    Description:
    simulates the hill climbing process 5 times and pickes the shortest option    
        
    '''
    path=execute(start,target,myPath,flag,maxN)
    maxN=len(myPath)
    print('my best path so far is:', path)
    for i in range(0,3):
      myPath=[]
      path1=execute(start,target,myPath,flag,maxN)
      if (len(path1)<len(path)):
        path=path1
        maxN=len(myPath)
        print('my best path so far is:', path)
    if(target in path):
      print('my path is:',path) 
    else:
      print('i couldnt find a path but my best path was:',myPath)  
    return path  
   
#%% beamSerch
def mainBeam(start,target,myPath,k,inputBolean):
    
    m=                 10                                                      #amount of iterations
    found=             False                                                   
    myTopK=            firstK(start,target,myPath,k)                           #first three words
    if target in myTopK:
      myPath.append    (myTopK)
      found=           True 
    
   
    while (m>0)and(found==False):
      Bank=                     buildBank(myTopK,myPath)                              #the neigbors of all the 3 words
      if(inputBolean):
        print('words i consider are:',Bank)  
      if len(Bank)==0:break
      distBank=                 distOption(Bank,target)                        #banks distance
      myTopK=                   pickThree(distBank,Bank,k)                     #choose the top 3
      myPath.append             (m) 
      myPath=                   myPath+myTopK                                  #add them to my path
      m=                        m-1  
      del                       Bank[:]
                                                                               #optional#print('the path so far is:',myPath)
      if target in myTopK:
        found=                  True
      
    if(found):
      print('my path is:', myPath)
    
    else:
      print('there is no path but this is what i have:',myPath)  
        

def  pickThree(distWords,Words,k):
     '''
     Description: 
     Will collect all minimom elements 
     If there are a few equal minimom will randomize between them 
     Will pick the top 3 candidates
     '''
     del minimom[:]
     del myK[:]
    
     
     while (len(myK)<3):
       #this part will inizialize a min  
       minVal=      min(distWords)                                             # min distance
       minIndex=    distWords.index(minVal)                                    #index of minVAl
       minWord=     Words[minIndex]                                            #the word that match the minVal
       distWords.remove(minVal)                                                #delete it
       Words.remove(minWord)                                                   #delete it 
       minimom.append(minWord)                                                 #add it to minimom array
   
       #as long as there are more equal minimom collect them
       if len(distWords)>0 and (min(distWords))==minVal:
         while ((len(distWords)>0 and min(distWords))==minVal):
           minVal1=     min(distWords)
           minIndex1=   distWords.index(minVal1)
           minWord1=    Words[minIndex1]
           distWords.remove(minVal1)
           Words.remove(minWord1)
           minimom.append(minWord1)
           
       #this part will put the elements in my k picks      
   
       #if all  min  can enter in myK
       if len(minimom)<(k-(len(myK))):
         for i in range(len(minimom)):    
           r=random.randint(0,len(minimom)-1)
           myK.append(minimom[r])
           dic.remove(minimom[r])
           minimom.remove(minimom[r])
       else:  
         #meaning minimom is bigger then the space in myK
         for i in range(k-len(myK)):    
           r=random.randint(0,(len(minimom)-1))
           myK.append(minimom[r])
           dic.remove(minimom[r])
           minimom.remove(minimom[r])
         
    
     return myK
 
def firstK(start,target,myPath,k):                                             #beamSearch
   '''
   Description:
   Pick the first 3 words 
   In distance 1 from start-word    
   
   '''
   Words=       options(start,myPath)
   distWords=   distOption(Words,target)
   myTopK=      pickThree(distWords,Words,k)
   myPath=      myPath+myTopK
   return       myTopK

def buildBank(myTopK,myPath):                                                  #beamSearch
    '''
    Description:
    will build a bank of words from the top picks
    '''
    BankS=set()                                                                #no duplicates
    for i in myTopK:
      BankS.update(options(i,myPath))
      
    Bank=list(BankS)                  
    return Bank
        
#%%neighbors in distance of 1 change from a word
def optionsSimulated(source,lastWord):
    '''
    Description:
    the same function as options other then the secound if     
    '''
    del words[:]
    leng=len(source)
    for i in range (0,len(dic)):  
       if(abs(leng- len(dic[i]))<2): 
         x=distance(source,dic[i])
         if ((x==1 or x==0) and dic[i] != lastWord):                           # if i will not alow all the words from my path to re-enter we will get stuck pretty quickly
           words.append(dic[i] )
                                                                               #optional#print ('word bank is:',words)
  
    return words 

def options(source, myPath):
    '''
    Description:
    Pass on all dictionary
    Picks the words that are in distance 1 or 0 from given source word
    '''
    del words[:]
    leng=len(source)
    for i in range (0,len(dic)):  
       if(abs(leng- len(dic[i]))<2): 
         x=distance(source,dic[i])
         if ((x==1 or x==0) and (dic[i] not in myPath)):
           words.append(dic[i] )
           
           
                                                                               #optional#print ('my words are:',words)
  
    return words 
#%%array of distances
def distOption(words, target):
   '''
   Description:
   Will tell the distance from the target-word for every word in words
   '''
   del distWords[:]
   for i in range (0,len(words)):
      x=distance(words[i],target)  
      distWords.append(x)
                                                                               #optional#print ('distance word:',distWords)
   return distWords

#%% distance
def distance(source, target): 
    '''
    Description:
    will initialize a 2d array with (-1)
    '''
    FlenS=len(source)+1
    FlenT=len (target)+1
            
    table=[[-1]*FlenT]*FlenS
    return distance1(table,source,target)

def distance1(table, source, target):
     """
     Description: req function
     Will tell the distance between two given words, 
     Distance is calculated by the amount of changes needed to be done to transforam the first word to the other
     """
     if (len(source)== 0):  
        return len(target)
     if (len(target) == 0): 
        return len(source)
    
     if (table[len(source)][len(target)]) == -1:
       if (source[0] == target[0]): 
          table[len(source)][len(target)] = distance1(table,source[1:],target[1:])
       else:
          substitution = distance1(table,source[1:], target[1:])
          deletion     = distance1(table,source[1:], target)
          insertion    = distance1(table,source, target[1:])
          table[len(source)][len(target)] = 1 + min(min(substitution, deletion), insertion)
                 
     return table[len(source)][len(target)]
 
#%%
def pickOne( distWords , Words ):
    '''
    Description:
    Collectes all minimom values
    Randomly choose between the top options
    '''
    del minimom[:]
    
    minVal=         min(distWords)                                             # min distance
    minIndex=       distWords.index(minVal)                                    #index of minVAl
    minWord=        Words[minIndex]                                            #the word that match the minVal
    distWords.remove(minVal)                                                   #delete it
    Words.remove(minWord)                                                      #delete it 
    minimom.append(minWord)                                                    #add it to minimom array
   
    if minVal==0:
        return minWord#break condition
    
    if len(distWords)>0 and (min(distWords))==minVal:
      while ((len(distWords)>0 and min(distWords))==minVal):
        minVal1=                 min(distWords)
        minIndex1=               distWords.index(minVal1)
        minWord1=                Words[minIndex1]
        distWords.remove(minVal1)
        Words.remove(minWord1)
        minimom.append(minWord1)
    
    if len(minimom)==1:#break condition
        return minimom[0]
    r=random.randint(0,len(minimom)-1)
    dic.remove(minimom[r])
    return minimom[r]
    
#%%genetic
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



def mainGenetic(start,target,inputBolean):
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
    
#%%
dic= readDict('d.txt','dd.txt') 
answer=SerchAlgo(start,target,inputBolean,DetailOutput)    