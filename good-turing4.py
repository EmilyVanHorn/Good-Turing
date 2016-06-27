
#!/usr/bin/env/python3

#super-words as bins

from operator import *
from collections import Counter
import csv
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.stem import *
from nltk.corpus import wordnet as wn
import string


INTERVAL_MODE = 'time'                              #options: time, count;
                                                    #options: words, categories;
INTERVAL = 60000                                    #1 minute
#INTERVAL = 600000                                  #10 minutes
#INTERVAL = 1800000                                 #30 minutes
#INTERVAL = 3600000                                 # 1 hour
#INTERVAL = 30

def get_fof(count):
#in: Counter containing frequency of element bins
#out: Counter containing the frequencies of frequencies of element bins
  return Counter(map(itemgetter(1), count.items()))

def estimateNewIdea(count, line):
    freq = get_fof(count)                                   #Counter counting frequeny or frequencies
    n1 = freq[1]                                            #frequency of "1"
    nc1 = freq[2]                                           #frequency of 1+1
    c = 1                                                   
    n = float(sum(map(itemgetter(1), count.items())))       #total number of items
    
    #line.append(str((n1/n)*100) + "%")
    line.append(str((nc1 * (c+1))/n * 100) + "%")
    
def calculateCat(count, output, timeSlice, new, sliceTotal):
    total = float(sum(map(itemgetter(1), count.items())))   #total number of items
    overallNew = 0
    line = output[timeSlice]
    
    for x in range(timeSlice + 1):
        if(x != 0):
            overallNew += output[x][2]
    
    #calculate per slice 
    perSlice = (new/sliceTotal)*100                         #percent of new per slice
    line.append(str(perSlice) + "%")
    
    #calculate overall
    overall = (overallNew/total)*100                        #percent of new overall
    line.append(str(overall) + "%")
    
    
def evaluate(file):
    #evaluate data
    i = 0                                                   #index for while loop
    if(INTERVAL_MODE == 'time'):
        start = int(file[0][2])
        end = start + INTERVAL
    elif(INTERVAL_MODE == 'count'):
        start = 0
        end = start + INTERVAL
                    
    count = Counter()                                       #counter
    timeSlice = 1                                           #timeSlice ID
    output = list([])                                       #output array   
    newIdea = 'false'                                       #true/false: new bin in the time slice
    newIdeaCount = 0
    totalIdeas = 0

    output.append(["Time Slice",                            #file header
                   "New Category?", 
                   "# of New Categories", 
                   "Total Ideas in Time Slice",
                   "Probability of New Bin",
                   "%New Categories in Time Slice",
                   "%New Categories Overall",
                   "Counter"])
    while(i < len(file)):                                   #while more ideas still exist
        line = file[i]                                      #a line in a file
        if(INTERVAL_MODE == 'time'):
            current = int(line[2])
        elif(INTERVAL_MODE == 'count'):
            current = i
                    
        if(current <= end):                            #for each time slice
            oldCount = count[line[3]]
            count[line[3]] += 1                                     #add to counter  
            newCount = count[line[3]]                               
            if newCount == 1:                                   #was this a new bin?
                newIdea = 'true'                                    #if yes,
                newIdeaCount += 1
            
            totalIdeas += 1
            i += 1                                                  #increment while loop
        else:                                                   #at the end of each time slice
            if(totalIdeas > 0):
                output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
                estimateNewIdea(count, output[timeSlice])
                calculateCat(count, output, timeSlice, newIdeaCount, totalIdeas)
                timeSlice += 1                                  #increment time slice id
                
            start = end                                         #update time slice markers
            end = start + INTERVAL
            newIdea = 'false'
            newIdeaCount = 0
            totalIdeas = 0
    if(totalIdeas > 0):
        output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
        estimateNewIdea(count, output[timeSlice])
        calculateCat(count, output, timeSlice, newIdeaCount, totalIdeas)
    
    #write to file
    writeOut(output)
    
def writeOut(output):
    fileName = 'Data Output/02 SuperWordTest.csv'
    with open(fileName, 'w') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile)
        for row in output:
            thedatawriter.writerow(row)
        print("Results written to " + fileName)
        

    
def stem(unique):
    stem = SnowballStemmer("english")
    newList = list()
    
    for word in unique:
        newList.append(stem.stem(word))
        #print(word + ": " + stem.stem(word) + "\n")
        
    return newList

def lem(unique):
    lem = WordNetLemmatizer()
    newList = list()
    
    for word in unique:
        newList.append(lem.lemmatize(word))
        #print(word + ": " + lem.lemmatize(word) + "\n")
    return newList
    
    
def format(line):
    stopwords = nltk.corpus.stopwords.words('english')      #list of stopwords
    real = list()
    
    line[1] = line[1].strip('"')                                  #eliminate quotes
    line[1] = line[1].split()                                     #cut stop words
    real += [word.lower() for word in line[1] if word.lower() not in stopwords]
    line[1] = sorted(real)
    #line[1] = lem(line[1])
    #line[1] = stem(line[1])  

def getGroup(count, word):
    word = "".join(l for l in word if l not in string.punctuation)
    best = 0;
    
    print "01 Word: ", word
    
    
    if(wn.synsets(word)):
        wordSyn = wn.synsets(word)[0]
    elif(wn.morphy(word)):
        wordSyn = wn.morphy(word)[0]
    else:
        print "Return"
        return word
    
    print "02 Synset of Word: ", wordSyn
        
    group = word
    
    for item in count.elements():
        print "03 Item: ", item
        itemSyn = item
        if(wn.synsets(item)):
            itemSyn = wn.synsets(item)[0]
        elif(wn.morphy(item)):
            itemSyn = wn.morphy(item)[0]
        else:
            print "Continue"
            continue
            
        print "04 Synset of item: ", itemSyn
        
        if(itemSyn.path_similarity(wordSyn) >= 0.5 and itemSyn.path_similarity(wordSyn) > best):
        #if this word is similar to an already existing one, add it as that group
            group = item
            best = itemSyn.path_similarity(wordSyn)
            
        print "05 Group: ", group
    print "Finished"
    
    
    
    return group
    
    
    
def tempEvaluate(file):
    #evaluate data
    i = 0                                                   #index for while loop
    if(INTERVAL_MODE == 'time'):
        start = int(file[0][3])
        end = start + INTERVAL
    elif(INTERVAL_MODE == 'count'):
        start = 0
        end = start + INTERVAL
                    
    count = Counter()                                       #counter
    timeSlice = 1                                           #timeSlice ID
    output = list([])                                       #output array   
    newIdea = 'false'                                       #true/false: new bin in the time slice
    newIdeaCount = 0
    totalIdeas = 0

    output.append(["Time Slice",                            #file header
                   "New Category?", 
                   "# of New Categories", 
                   "Total Ideas in Time Slice",
                   "Probability of New Bin",
                   "%New Categories in Time Slice",
                   "%New Categories Overall",
                   "Counter"])
    print(len(file));
    while(i < len(file)):                                   #while more ideas still exist
        line = file[i]                                      #a line in a file
        if(INTERVAL_MODE == 'time'):
            current = int(line[3])
        elif(INTERVAL_MODE == 'count'):
            current = i          
        if(current <= end):                            #for each time slice
            format(line)                                    #convert idea content to list of relivant words                                  
            for word in line[1]:                            #add to counter
                group = getGroup(count, word)
                oldCount = count[group]
                count[group] += 1
                newCount = count[group]

                if newCount == 1:                           #was this a new bin?
                    newIdea = 'true'                            #if yes,
                    newIdeaCount += 1
                totalIdeas += 1
            i += 1 
        else:                                                   #at the end of each time slice
            if(totalIdeas > 0):
                output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
                estimateNewIdea(count, output[timeSlice])
                calculateCat(count, output, timeSlice, newIdeaCount, totalIdeas)
                timeSlice += 1                                  #increment time slice id
                
            start = end                                         #update time slice markers
            end = start + INTERVAL
            newIdea = 'false'
            newIdeaCount = 0
            totalIdeas = 0
    if(totalIdeas > 0):
        output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
        estimateNewIdea(count, output[timeSlice])
        calculateCat(count, output, timeSlice, newIdeaCount, totalIdeas)
    
    #write to file
    print count
    writeOut(output)

#__________________________________________________________________________________________________#


#get data
#file = open('Input/ideas2.csv').read().splitlines()     #input file of ideas
#file = [line.split(',') for line in file]               #splits each line into fields
#file.sort(key=itemgetter(3))                            #sorts by unixTime

file = []

for line in csv.reader(open('Input/smallIdeas.csv'), skipinitialspace = True):
    file.append(line)
    
file.sort(key=itemgetter(3))


#freqDist = FreqDist(format(file))                       #get frequencies of words
tempEvaluate(file)


'''thing = []

for line in file:
   format(line)
    for word in line[1]:
        thing.append(word)
        
for word in sorted(thing):
    print word'''







    
#evaluate data
#evaluate(file)






    

