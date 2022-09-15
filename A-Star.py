import random
import os.path
distWords=[]
F_dist=[]
words=[]
myPath=[]
dic=[]
minimom=[]

#you define
start='bike'
target='house'
inputBolean=True

#%%
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

#%%
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
                  
#%%
      
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



#%%distance
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
     By the amount of changes needed to be done to transforam the first to the sec
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
def options(source, myPath):
    '''
    Description:
    Pass on all dictionary
    Picks the words that are in distance 1 from given source
    '''
    del words[:]
    leng=len(source)
    for i in range (0,len(dic)):  
       if(abs(leng- len(dic[i]))<2): 
         x=distance(source,dic[i])
         if ((x==1 or x==0) and (dic[i] not in myPath)):
           words.append(dic[i] )
           
           
                                                                               #optinal#print ('my words are:',words)
  
    return words 

#%%
def distOption(words, target):
   '''
   Description:
   Calculates the distance of the words in words from target
   '''
   del distWords[:]
  
   for i in range (0,len(words)):
      x=distance(words[i],target)  
      distWords.append(x)
   
   return distWords
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
    


def mainA_Star(start,target,myPath,inputBolean)
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
#%%

    