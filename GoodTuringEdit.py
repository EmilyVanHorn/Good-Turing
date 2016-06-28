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
    real = list()
    
    line[1] = line[1].strip('"')                                  #eliminate quotes
    line[1] = line[1].split()                                     #cut stop words
    real += [word.lower() for word in line[1] if word.lower() not in stopwords]
    line[1] = sorted(real)
    line[1] = lem(line[1])
    line[1] = stem(line[1])  
    
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
        print themeName
        print currentTheme
        if (themeName == currentTheme):
            ideasByTheme.append(line)
        else:
            ideasByTheme.sort(key=itemgetter(3))
            output.append([currentTheme, "", "", "", "", ""])

            evaluate3_1(ideasByTheme, output)

            ideasByTheme = []
            currentTheme = themeName
            ideasByTheme.append(line)
    
        if(ideasByTheme.length > 0){
            ideasByTheme.sort(key=itemgetter(3))
            output.append([currentTheme, "", "", "", "", ""])

            evaluate3_1(ideasByTheme, output)

            ideasByTheme = []
            currentTheme = themeName
            ideasByTheme.append(line)
        }
                
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
INTERVAL_MODE = 'time'                              #options: time, count;
                                                    #options: words, categories;
#INTERVAL = 60000                                    #1 minute
INTERVAL = 600000                                    #10 minutes
#INTERVAL = 1800000                                  #30 minutes
#INTERVAL = 3600000                                  # 1 hour
#INTERVAL = 30
out = []                                            #output to print

#getInput
file = getInputFile(INPUT_FILE)

#process
out = evaluate3(file)
for line in out:
    print line
#evaluate:      basic; category as bin              DONE
#               ideas.csv
#evaluate2:     words as bins                       DONE    
#               ideas2.csv
#evaluate3:     words as bins; separate by theme    DONE
#               ideas_corrected.csv
#               smallIdeas.csv
#evaluate4:     super-words as bins                 IN-PROGRESS

#printResults
writeOut(out, OUTPUT_FILE)