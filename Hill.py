import random
path=       []
minimom=    []
dic=        []  
disWords=   []
words=      []
myPath=     []#will be printed
myBestPath= []
maxN=       20

#you define
start='bike'
target='david'
    
 
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
 
    
#%%
def distOption(words, target):
   '''
   Description:
   Calculates the distance of the words in words from target
   '''
   del disWords[:]
   for i in range (0,len(words)):
      x=distance(words[i],target)  
      disWords.append(x)
   return disWords



#%%
def pickOne( disWords , Words ):
    '''
    Description:
    Collectes all minimom values
    Randomly choose between the top options
    '''
    del minimom[:]
    
    minVal=         min(disWords)# min distance
    minIndex=       disWords.index(minVal)#index of minVAl
    minWord=        Words[minIndex]#the word that match the minVal
    disWords.remove(minVal)#delete it
    Words.remove(minWord)#delete it 
    minimom.append(minWord)#add it to minimom array
   
    if minVal==0:
        return minWord#break condition
    
    if len(disWords)>0 and (min(disWords))==minVal:
      while ((len(disWords)>0 and min(disWords))==minVal):
        minVal1=                 min(disWords)
        minIndex1=               disWords.index(minVal1)
        minWord1=                Words[minIndex1]
        disWords.remove(minVal1)
        Words.remove(minWord1)
        minimom.append(minWord1)
    
    if len(minimom)==1:#break condition
        return minimom[0]
    r=random.randint(0,len(minimom)-1)
    dic.remove(minimom[r])
    return minimom[r]
    
#%%

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
    words=options(start , myPath)# options from dic on the start word
    
    if(len(words)==0):#break condition
        return myPath
    
    #print ('dic words ',words)
    disWords=distOption(words, target)#distance of every word from target
    #print ('distance', disWords)
    newPic=pickOne(disWords,words)#randomly choose my next word
   
   
    #print('my path is',myPath)
    #print('my newPic',newPic)
  
   
    if newPic==target:
       myPath.append(target) 
      # print ('the path is',myPath)
       return myPath
    else:
      return  execute (newPic,target,myPath,flag+1,maxN)
    

#%%
def letsDoIt(start,target,myPath,flag,maxN):
    '''
    Description:
    simulates the hill climbing process 5 times and pickes the shortest option    
        
    '''
    
    path=                execute(start,target,myPath,flag,maxN)
    maxN=                len(myPath)
    print('my best path so far is:', path)
    for i in range(0,3):
      myPath=            []
      path1=             execute(start,target,myPath,flag,maxN)
      if (len(path1)<len(path)):
        path=                   path1
        maxN=                   len(myPath)
        print('my best path so far is:', path)
    if(target in path):
      print('my path is:',path) 
    else:
      print('i couldnt find a path but my best path was:',myPath)  
    return path      
#%%


  

d='C:\\ai\\dclean.txt'#path
with open(d) as f:
  dic = f.readlines()
  for i in range (0,len(dic)):
    dic[i]=dic[i].strip()
    dic[i]= dic[i].lower() 
    
ans=letsDoIt(start, target, myPath,0,maxN)




