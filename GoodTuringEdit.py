from operator import *
from collections import Counter
import csv
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.stem import *
from nltk.corpus import wordnet as wn
import string

def getInputFile(fileName):#-------------------------------------GET_INPUT_FILE
    #var dictionary
    file = []                                       #file as a list of entries
    #fileName                                       #name of input file
    #sortBy                                         #what to sort the data by:
                                                        #0: ideaId
                                                        #1: raw idea
                                                        #2: userId
                                                        #3: unix time
                                                        #4: theme
    #read each line and add to file
    for line in csv.reader(open(fileName), skipinitialspace = True):
        file.append(line)
    return file

def get_fof(count):#----------------------------------------------------GET_FOF
#in: Counter containing frequency of element bins
#out: Counter containing the frequencies of frequencies of element bins
  return Counter(map(itemgetter(1), count.items()))

def estimateNewIdea(count, line):#----------------------------ESTIMATE_NEW_IDEA
    freq = get_fof(count)                                   #Counter counting frequeny or frequencies
    n1 = freq[1]                                            #frequency of "1"
    nc1 = freq[2]                                           #frequency of 1+1
    c = 1                                                   
    n = float(sum(map(itemgetter(1), count.items())))       #total number of items
    
    #line.append(str((n1/n)*100) + "%")
    line.append(str((nc1 * (c+1))/n * 100) + "%")
    
def calculateCat(count, output, timeSlice, new, sliceTotal):#-----CALCULATE-CAT
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

def stem(unique):#---------------------------------------------------------STEM
    stem = SnowballStemmer("english")
    newList = list()
    
    for word in unique:
        newList.append(stem.stem(word))
        
        
    return newList

def lem(unique):#-----------------------------------------------------------LEM
    lem = WordNetLemmatizer()
    newList = list()
    
    for word in unique:
        newList.append(lem.lemmatize(word))
        
    return newList
    
    
def format(line):#-------------------------------------------------------FORMAT
    stopwords = nltk.corpus.stopwords.words('english')      #list of stopwords
    useless = ["would", "could", "in", "use"];
    real = list() 
    
    line[1] = line[1].strip('"')                                  #eliminate quotes
    line[1] = line[1].split()                                     #cut stop words
    real += [word.lower() for word in line[1] if 
             word.lower() not in stopwords and 
             word.lower() not in useless]
    line[1] = sorted(real)
    if(VERSION < 4):
        line[1] = lem(line[1])
        line[1] = stem(line[1])  

def getGroup(count, word):
    word = "".join(l for l in word if l not in string.punctuation)
    best = 0
    group = word
    
    #searchForExisting
    if(wordsSeen.has_key(word)):
        return wordsSeen.get(word)
    
    #get synset
    if(wn.synsets(word)):
        wordSyn = wn.synsets(word)[0]
    elif(wn.morphy(word)):
        wordSyn = wn.morphy(word)[0]
    else:
        #no synset; use word
        wordsSeen.update({word: group})
        return word
    
    for item in count.elements():
        itemSyn = item
        if(itemsSeen.has_key(item)):
            itemSyn = itemsSeen.get(item)
        else:
            if(wn.synsets(item)):
                itemSyn = wn.synsets(item)[0]
            elif(wn.morphy(item)):
                itemSyn = wn.morphy(item)[0]
            elif(itemSyn == word):
                wordsSeen.update({word: itemSyn})
                return itemSyn
            else:
                continue
        
        #if(itemSyn.path_similarity(wordSyn) >= 0.5 and itemSyn.path_similarity(wordSyn) > best):
        #if this word is similar to an already existing one, add it as that group
            #group = item
            #best = itemSyn.path_similarity(wordSyn)
            
        if(itemSyn.path_similarity(wordSyn) >= 0.5):
            group = item
            break;
        
    wordsSeen.update({word: group})
    
    return group

def getGroup2(count, word):
    #creates a dictionary/hash table of synonyms
    #nltk version
    #later try PyDictionary
    word = "".join(l for l in word if l not in string.punctuation)
    group = word
    
    #search hash table for existing entry (word)
    if(wordsSeen.has_key(word)):
        return wordsSeen.get(word)
    
    #get synset
    if(wn.synsets(word)):
        wordSyn = wn.synsets(word)
    elif(wn.morphy(word)):
        wordSyn = wn.morphy(word)
    else:
        #no synset; use word
        wordsSeen.update({word: group})
        return word
    
    
    #not entirly accurate
    for syn in wordSyn:
        for lem in syn.lemmas():
            if(wordsSeen.has_key(lem.name())):
                group = wordsSeen.get(lem.name())
            else:
                wordsSeen.update({lem.name(): group})
            
    return group
        
    #if not found: 
        #search english dictionary
            #if found in english dictionary:
                #add word and all synonymns with word as value
                #return word
            #if not found in english dictionary: 
                #stub: print        --> see what comes out and then decide
                #throw away?        --> probably a typo
                #return word?       --> lots of words are not in the dictionary
    
    
    
def evaluate(file):#---------------------------------------------------EVALUATE
    #var dictionary
    #file                                           #raw input file
    #start                                          #starting point for intervals
    #end                                            #end point for current interval
    count = Counter()                               #counter for frequencies
    timeSlice = 1                                   #timeSlice ID
    newIdea = 'false'                               #true/false:
                                                        #new bin in the time slice?
    newIdeaCount = 0                                #number of new ideas so far
    totalIdeas = 0                                  #total ideas per timeSlice
    output = []                                     #output array
    i = 0                                           #index for while loop
    file.sort(key=itemgetter(2))
    
    
    
    if(INTERVAL_MODE == 'time'):
        start = int(file[0][2])                     #unix time of first row
        end = start + INTERVAL
    elif(INTERVAL_MODE == 'count'):
        start = 0
        end = start + INTERVAL
        
    output.append(["Time Slice",                        #file header
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
        
    return output
def evaluate2(file):#-------------------------------------------------EVALUATE2
    #var dictionary
    #file                                           #raw input file
    #start                                          #starting point for intervals
    #end                                            #end point for current interval
    count = Counter()                               #counter for frequencies
    timeSlice = 1                                   #timeSlice ID
    newIdea = 'false'                               #true/false:
                                                        #new bin in the time slice?
    newIdeaCount = 0                                #number of new ideas so far
    totalIdeas = 0                                  #total ideas per timeSlice
    output = []                                     #output array
    i = 0                                           #index for while loop
    file.sort(key=itemgetter(3))
    
    
    
    if(INTERVAL_MODE == 'time'):
        start = int(file[0][3])                     #unix time of first row
        end = start + INTERVAL
    elif(INTERVAL_MODE == 'count'):
        start = 0
        end = start + INTERVAL
        
    output.append(["Time Slice",                        #file header
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
            current = int(line[3])
        elif(INTERVAL_MODE == 'count'):
            current = i          
        if(current <= end):                            #for each time slice
            format(line)                                    #convert idea content to list of relivant words
            for word in line[1]:
                oldCount = count[word]
                count[word] += 1
                newCount = count[word]

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
    
    return output

def evaluate3_1(file, realOutput):#---------------------------------EVALUATE3.1
    #var dictionary
    #file                                           #raw input file
    #start                                          #starting point for intervals
    #end                                            #end point for current interval
    count = Counter()                               #counter for frequencies
    timeSlice = 1                                   #timeSlice ID
    newIdea = 'false'                               #true/false:
                                                        #new bin in the time slice?
    newIdeaCount = 0                                #number of new ideas so far
    totalIdeas = 0                                  #total ideas per timeSlice
    output = []                                     #output array
    i = 0                                           #index for while loop
    file.sort(key=itemgetter(3))
    
    
    
    if(INTERVAL_MODE == 'time'):
        start = int(file[0][3])                     #unix time of first row
        end = start + INTERVAL
    elif(INTERVAL_MODE == 'count'):
        start = 0
        end = start + INTERVAL
        
    realOutput.append(["Time Slice",                        #file header
                "New Category?", 
                "# of New Categories", 
                "Total Ideas in Time Slice",
                "Probability of New Bin",
                "%New Categories in Time Slice",
                "%New Categories Overall",
                "Counter"])
    while(i < len(file)):                                   #while more ideas still exist
        line = file[i]                                      #a line in a file
        output = list([])                                   #output array   
        
        if(INTERVAL_MODE == 'time'):
            current = int(line[3])
        elif(INTERVAL_MODE == 'count'):
            current = i            
        if(current <= end):                            #for each time slice
            format(line)                                    #convert idea content to list of relivant words                                 
            for word in line[1]:                            #add to counter
                oldCount = count[word]
                count[word] += 1
                newCount = count[word]

                if newCount == 1:                           #was this a new bin?
                    newIdea = 'true'                            #if yes,
                    newIdeaCount += 1
                totalIdeas += 1
            i += 1 
        else:                                                   #at the end of each time slice
            if(totalIdeas > 0):
                output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
                estimateNewIdea(count, output[0])
                calculateCat(count, output, 0, newIdeaCount, totalIdeas)
                timeSlice += 1                                  #increment time slice id
                realOutput.append(output[0])
                
                
            start = end                                         #update time slice markers
            end = start + INTERVAL
            newIdea = 'false'
            newIdeaCount = 0
            totalIdeas = 0
    if(totalIdeas > 0):
        output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
        estimateNewIdea(count, output[0])
        calculateCat(count, output, 0, newIdeaCount, totalIdeas)


def evaluate3(file):#-------------------------------------------------EVALUATE3
    file.sort(key=itemgetter(4))
    currentTheme = file[0][4]                               #sortBy category
    ideasByTheme = []
    output = []

    for line in file:
        themeName = line[4]
        print "themeName:", themeName
        print "currentTheme:", currentTheme
        if (themeName == currentTheme):
            print "append"
            ideasByTheme.append(line)
        else:
            print "else"
            ideasByTheme.sort(key=itemgetter(3))
            output.append([currentTheme, "", "", "", "", ""])

            print "EVALUATE"
            evaluate3_1(ideasByTheme, output)

            ideasByTheme = []
            currentTheme = themeName
            ideasByTheme.append(line)
    
        if(len(ideasByTheme) > 0):
            ideasByTheme.sort(key=itemgetter(3))
            output.append([currentTheme, "", "", "", "", ""])

            evaluate3_1(ideasByTheme, output)

            ideasByTheme = []
            currentTheme = themeName
            ideasByTheme.append(line)
        
                
    return output

def evaluate4(file):#-------------------------------------------------EVALUATE4
    #var dictionary
    #file                                           #raw input file
    #start                                          #starting point for intervals
    #end                                            #end point for current interval
    count = Counter()                               #counter for frequencies
    timeSlice = 1                                   #timeSlice ID
    newIdea = 'false'                               #true/false:
                                                        #new bin in the time slice?
    newIdeaCount = 0                                #number of new ideas so far
    totalIdeas = 0                                  #total ideas per timeSlice
    output = []                                     #output array
    i = 0                                           #index for while loop
    file.sort(key=itemgetter(3))
    
    
    
    if(INTERVAL_MODE == 'time'):
        start = int(file[0][3])                     #unix time of first row
        end = start + INTERVAL
    elif(INTERVAL_MODE == 'count'):
        start = 0
        end = start + INTERVAL
        
    output.append(["Time Slice",                        #file header
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
            current = int(line[3])
        elif(INTERVAL_MODE == 'count'):
            current = i          
        if(current <= end):                            #for each time slice
            format(line)                                    #convert idea content to list of relivant words                                  
            print line[1]
            for word in line[1]:                            #add to counter
                group = getGroup2(count, word)
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
    print count
    return output
    
def writeOut(output, fileName):#--------------------------------------WRITE_OUT
    #var dictionary
    #filename                                       #file to write to
    #output                                         #data to write
    #writer                                         #csv writer object
    
    with open(fileName, 'w') as file:               
        writer = csv.writer(file)
        for row in output:
            writer.writerow(row)
        print "Results written to ", fileName

#--------------------------------------------------------------------------MAIN

INPUT_FILE = "Input/ideas_corrected.csv"            
OUTPUT_FILE = "Data Output/00 BasicTest.csv" 
VERSION = 4
INTERVAL_MODE = 'time'                              #options: time, count;
                                                    #options: words, categories;
#INTERVAL = 60000                                    #1 minute
INTERVAL = 600000                                    #10 minutes
#INTERVAL = 1800000                                  #30 minutes
#INTERVAL = 3600000                                  # 1 hour
#INTERVAL = 30
out = []                                            #output to print
wordsSeen = {}
itemsSeen = {}

#getInput
file = getInputFile(INPUT_FILE)

#process
if(VERSION == 1):
    out = evaluate(file)
elif(VERSION == 2):
    out = evaluate2(file)
elif(VERSION == 3):
    out = evaluate3(file)
elif(VERSION == 4):
    out = evaluate4(file)

#print wordsSeen

for line in out:
    print line

#VERSION 1:     basic; category as bin              DONE
#               ideas.csv
#VERSION 2:     words as bins                       DONE    
#               ideas2.csv
#VERSION 3:     words as bins; separate by theme    IN-PROGRESS
#               ideas_corrected.csv
#               smallIdeas.csv
#VERSION 4:     super-words as bins                 IN-PROGRESS

#printResults
writeOut(out, OUTPUT_FILE)