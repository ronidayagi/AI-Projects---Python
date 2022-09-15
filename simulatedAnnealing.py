import random
import math

myPath=  []
words=   []
currE=   0
nextE=   1

#you define
start='bike'
target='david'
inputBolean=True

def mainSimulated(myPath,start,target,inputBolean):
    ans=simulatedAnnealing(myPath, start, target,inputBolean)

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
       
        words=               optionsSimulated(thisWord, lastWord)
        currE=               distance(thisWord,end) 
        nextWord=            random.choice(words)
        nextE=               distance(nextWord,end)  
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
#%%
def optionsSimulated(source,lastWord):
    del words[:]
    leng=len(source)
    for i in range (0,len(dic)):  
       if(abs(leng- len(dic[i]))<2): 
         x=distance(source,dic[i])
         if ((x==1 or x==0) and dic[i] != lastWord):
           words.append(dic[i] )
                                                                               #optional#print ('word bank is:',words)
  
    return words 


   
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
d='C:\\ai\\dclean.txt'#path
with open(d) as f:
  dic = f.readlines()
  for i in range (0,len(dic)):
    dic[i]=dic[i].strip()
    dic[i]= dic[i].lower()    
    
    
ans=simulatedAnnealing(myPath,'bike','david',inputBolean)