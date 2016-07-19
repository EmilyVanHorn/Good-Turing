from __future__ import division
from operator import *
from collections import Counter
import csv
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.stem import *
from nltk.corpus import wordnet as wn
import string
import gensim
import json
from gensim import models
import xlsxwriter

def func1():
    return [["1", "2", "3", "4"],
            ["one", "two", "three", "four"]]
    
def func2():
    return [["one", "two", "three", "four"],
            ["1", "2", "3", "4"]]
    
def func3():
    return [["a", "b", "c", "d"],
            ["one", "two", "three", "four"]]

def func4():
    return [["z", "y", "x", "w"],
            ["one", "two", "three", "four"]]

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
    
    line.append(str((n1/n)*100) + "%")
    #line.append(str((nc1 * (c+1))/n * 100) + "%")
    
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
    line[1] = lem(line[1])
    
    
#def createScatterPlot(datasets, methods, thresholds):
 #   workbook = xlsxwriter.Workbook('Data Output/ExcelTesting.xlsx')
#  worksheet = workbook.add_worksheet()
#    chart5 = workbook.add_chart({'type': 'scatter',
#                                 'subtype':'smooth'})
    
#    chart5.add_series({
#        'name': 'test',
#        'categories
#    })
    #for set in datasets:
    #    for method in methods:
    #        for threshold in thresholds:
    #            i = 1
    #            chart5.add_series({
    #                'name':
    #                'categories':     "=Sheet1!$" + i + "  
    #            })
    
    
def nSim(inputSyn, comparisons):
    avg = 0
    for existing in comparisons:
        existingSyn = existing
        #get synset of existingSyn
        if(wn.synsets(existing)):
            existingSyn = wn.synsets(existing)[0]
        elif(wn.morphy(existing)):
            existingSyn = wn.morphy(existing)[0]
        else:
            #no synset; skip
            continue
            
        #compare input and existing
        sim = existingSyn.path_similarity(inputSyn)
        if(sim == None):
            sim = 0
        avg = (avg + sim)/2
    return avg


def getCombos(groupList):
    combos = set()
    print "START"
    
    x = 0
    while(x < len(groupList) - 1):
        print "\tX: ", x
        word1 = groupList[x]
        y = 1
        while(y < len(groupList)):
            print "\tY: ", y
            word2 = groupList[y]
            print "\tWord: ", word1
            print "\tNextWord: ", word2
            if(word1 == word2):
                print "\tequal"
            else:
                c = word1 + "-" + word2
                combos.update([c])
                print "\tCombo: ", c
            y = y + 1
        x = x + 1
            
    return combos
    
def getGroup(count, word, threshold, wordsSeen, groups):
    word = "".join(l for l in word if l not in string.punctuation)
    best = 0
    group = word
    
    #searchForExisting
    if(wordsSeen.has_key(word)):
        return wordsSeen.get(word)
    
    #get synset of word
    if(wn.synsets(word)):
        wordSyn = wn.synsets(word)[0]
    elif(wn.morphy(word)):
        wordSyn = wn.morphy(word)[0]
    else:
        #no synset; use word
        wordsSeen.update({word: group})
        
        if(groups.has_key(group)):
            newValue = groups.get(group)
            newValue.update([word])
            groups.update({group: newValue})
        else:
            newValue = set()
            newValue.update([word])
            groups.update({group: newValue})
            wordsSeen.update({word: group}) 
        return word
    
    #compare to each group
        # is there a way to compare one word to many words?
    for super_word in count.keys():
        #get synset of group being tested against
        comparisons = groups.get(super_word)
        sim = nSim(wordSyn, comparisons)
        
        if(sim >= threshold and sim > best):
            group = super_word
            best = sim
            
    wordsSeen.update({word: group})
    if(groups.has_key(group)):
        newValue = groups.get(group)
        newValue.update([word])
        groups.update({group: newValue})
    else:
        newValue = set()
        newValue.update([word])
        groups.update({group: newValue})
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
    #if a synonym is found, update group to that value
        #problem1: multiple synonyms may exist with differnt values
            #which to use?
            #update them to be the same?
        #problem2: synonymns' values to update to may change halfway through
            #search in a separate loop and then update? --> problem 1 still an issue, but
                #maybe less so if synonymns usually don't have different values
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
                
def getGroup3(count, word, model, threshold, wordsSeen, groups):
    word = "".join(l for l in word if l not in string.punctuation)
    best = 0
    group = word
    
    
    #print word
    #searchForExisting
    if(wordsSeen.has_key(word)):
        return wordsSeen.get(word)
    
    
    for super_word in count.keys():
        comparisons = groups.get(super_word) # assume that comparisons is an array of words that make up the super_word
        try:
            #print "\t", item, " vs. ", word
            #sim = model.similarity(item, word)
            sim = model.n_similarity([word], comparisons)
            #print "\t\t", sim
        except:
            continue
               
        if(sim >= threshold and sim > best):
        #if this word is similar to an already existing one, add it as that group
            group = super_word
            best = sim
    #print "\tBest: ", best
    #print "\tGroup: ", group
    if(groups.has_key(group)):
        newValue = groups.get(group)
        newValue.update([word])
        groups.update({group: newValue})
    else:
        newValue = set()
        newValue.update([word])
        groups.update({group: newValue})
    wordsSeen.update({word: group})  
    return group
                
def countUniqueWords(file):
    stopwords = nltk.corpus.stopwords.words('english')
    useless = ["would", "could", "in", "use"]
    listOfWords = []
    count = Counter()
    newIdeaCount = 0
    
    for line in file:
        words = line[1].strip('"')
        words = line[1].split()
        listOfWords.append([w.lower() for w in words if
                            w.lower() not in stopwords and
                            w.lower() not in useless])
    listOfWords = sorted(listOfWords)
    
    for word in listOfWords:
        group = getGroup2(count, word)
        oldCount = count[group]
        count[group] += 1
        newCount = count[group]

        if newCount == 1:                           #was this a new bin?
            newIdeaCount += 1
    
    print "# of new Ideas: ", newIdeaCount    
    
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
        estimateNewIdea(count, output)
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
                estimateNewIdea(count, output)
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

def evaluate4(file, logs, method, threshold, dataset):#-------------------EVALUATE4
    groupsDictOut = []
    groupsDictOut.append(["Super_Word", "Value"])
    wordsSeen = {}
    groups = {}
    itemsSeen = {}
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
    model = models.Word2Vec.load("text8Model")
    #file.sort(key=itemgetter(3))
    
    logs.append(["--------------- START EXECUTION ---------------"])
    if(INTERVAL_MODE == 'time'):
        start = int(file[0][3])                     #unix time of first row
        end = start + INTERVAL
    elif(INTERVAL_MODE == 'count'):
        start = 0
        end = start + INTERVAL
        
    #output.append(["Time Slice",                        #file header
    #            "New Category?", 
    #            "# of New Categories", 
    #            "Total Ideas in Time Slice",
    #            "Probability of New Bin",
    #            "%New Categories in Time Slice",
    #            "%New Categories Overall",
    #            "Counter"])
    logs.append([str(timeSlice) + "------ TIME_SLICE" + str(timeSlice) + " -----"])
    while(i < len(file)):                                   #while more ideas still exist
        line = file[i]                                      #a line in a file
        if(INTERVAL_MODE == 'time'):
            current = int(line[3])
        elif(INTERVAL_MODE == 'count'):
            current = i          
        if(current <= end):                            #for each time slice
            format(line)                                    #convert idea content to list of relivant words
            logs.append(["\tIDEA " + str(i) + " -----"])
            # print groupType
            groupList = []
            for word in line[1]:                            #add to counter
                if(method == "nltk"):
                    group = getGroup(count, word, threshold, wordsSeen, groups)
                elif(method == "word2vec"):
                    group = getGroup3(count, word, model, threshold, wordsSeen, groups)
                oldCount = count[group]
                count[group] += 1
                newCount = count[group]
                #groupList.append(group)

                if newCount == 1:                           #was this a new bin?
                    newIdea = 'true'                            #if yes,
                    newIdeaCount += 1
                totalIdeas += 1
                logs.append(["\t\t" + word + ":\t" + group + "--> \t" + str(newCount)])
            for group in groupList:
                print group
            
            #COMBOS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #groupList = getCombos(groupList)
            #for combo in groupList:
            #    oldCount = count[combo]
            #    count[combo] += 1
            #    newCount = count[combo]
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
            #    if(newCount == 1 and newIdea == "false"):
            #        newIdeaCount += 1
            #    logs.append(["\t\t" + str(line[1]) + ":\t" + combo + "--> \t" + str(newCount)])
            i += 1
        else:                                                   #at the end of each time slice
            if(totalIdeas > 0):
                output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
                estimateNewIdea(count, output[timeSlice - 1])
                calculateCat(count, output, timeSlice - 1, newIdeaCount, totalIdeas)
                timeSlice += 1                                  #increment time slice id
                logs.append([str(timeSlice) + "------ TIME_SLICE" + str(timeSlice) + " -----"])
                
            start = end                                         #update time slice markers
            end = start + INTERVAL
            newIdea = 'false'
            newIdeaCount = 0
            totalIdeas = 0
    if(totalIdeas > 0):
        output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
        estimateNewIdea(count, output[timeSlice -1])
        calculateCat(count, output, timeSlice - 1, newIdeaCount, totalIdeas)
    #print count
    dictionary_to_save = "Dictionaries/wordkeyMyData_%s_%s_%.2f" %(dataset, method, threshold)
    dictionary_out = open(dictionary_to_save, 'w')
    dictionary_out.write(json.dumps(wordsSeen, indent=2))
    dictionary_out.close()
    for key in groups.keys():
        groupsDictOut.append([key, groups.get(key)])
    
    
    for line in groupsDictOut:
        print line
    print count
    writeOut(groupsDictOut, "Dictionaries/groupkeyMyData_%s_%s_%.2f.csv" %(dataset, method, threshold))
    return output

def evaluate5_1(file, realOutput, model):#---------------------------------EVALUATE5.1
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
        
    while(i < len(file)):                                   #while more ideas still exist
        line = file[i]                                      #a line in a file  
        
        if(INTERVAL_MODE == 'time'):
            current = int(line[3])
        elif(INTERVAL_MODE == 'count'):
            current = i            
        if(current <= end):                            #for each time slice
            format(line)                                    #convert idea content to list of relivant words 
            
            for word in line[1]:                            #add to counter
                group = getGroup3(count, word, model)
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
                #output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
                estimateNewIdea(count, output)
                #calculateCat(count, output, 0, newIdeaCount, totalIdeas)
                
                
                timeSlice += 1                                  #increment time slice id
                #realOutput.append(output[0])
                for item in output:
                    realOutput.append(item)
                
                
            start = end                                         #update time slice markers
            end = start + INTERVAL
            newIdea = 'false'
            newIdeaCount = 0
            totalIdeas = 0
    if(totalIdeas > 0):
        #output.append([timeSlice, newIdea, newIdeaCount, totalIdeas])
        estimateNewIdea(count, output)
        #calculateCat(count, output, 0, newIdeaCount, totalIdeas)

def evaluate5(file, logs):#-------------------------------------------------EVALUATE5
    file.sort(key=itemgetter(4))
    currentTheme = file[0][4]                               #sortBy category
    ideasByTheme = []
    row= []
    output = []
    model = models.Word2Vec.load("MODEL")

    for line in file:
        themeName = line[4]
        logs.append("themeName:" + themeName)
        if (themeName == currentTheme):
            ideasByTheme.append(line)
            continue
        else:
            ideasByTheme.sort(key=itemgetter(3))
            row.append(currentTheme)
            #output.append([currentTheme, "", "", "", "", ""])

            evaluate5_1(ideasByTheme, row, model)
            output.append(row)

            ideasByTheme = []
            row = []
            currentTheme = themeName
            ideasByTheme.append(line)
            continue
    
        if(len(ideasByTheme) > 0):
            ideasByTheme.sort(key=itemgetter(3))
            #output.append([currentTheme, "", "", "", "", ""])
                
            evaluate5_1(ideasByTheme, row, model)
            output.append(row)

            ideasByTheme = []
            row = []
            currentTheme = themeName
            ideasByTheme.append(line)
        
                
    return output

def evaluate6(file, logs):#-------------------------------------------------EVALUATE6
    datasets = ['SuperBoring',
                 'Boring',
                 'Normal',
                 'NewAtEnd',
                 'Exciting']              #the list of input filenames
    #datasets = ['smallIdeas']
    # versions = [evaluate4(file, logs, "getGroup", 0.5)]       #array of functions to try out
    #             evaluate4(file, logs, "getGroup", 0.9),
    #             evaluate4(file, logs, "getGroup3", 0.5),
    #             evaluate4(file, logs, "getGroup3", 0.9)]
    #methods = ["nltk", "word2vec"]
    methods = ["word2vec"]
    # method_names = {"getGroup": 'nltk', 'getGroup3': 'word2vec'}
    thresholds = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    #thresholds = [0.6]
    vText = ['nltk 0.5','nltk 0.9',                 #strings associated with the function of 
             'word2vec 0.5','word2vec 0.9']                       
                                                    #"versions[]"
    output = []                                     #output to be sent to csv
    outLine = []                                    #one line of output taken from "returnedOut"
    # i = 0

    output.append(["dataset", "method",             #header
               "timeSlice", "GT_predict", "true"])

    for dataset in datasets:                     #for each dataset
        input_file = "Input/MyData/%s.csv" %dataset
        print "datasets: ", dataset              
        # j = 0                   
        # for function in versions:                       #run each version of the program
        for method in methods:
            print "method: ", method
            for threshold in thresholds:
                print "threshold: ", threshold
                opened_input = getInputFile(input_file)
                returnedOut = evaluate4(opened_input, logs, method, threshold, dataset)                      #output from this version
                print "\treturnedOut: ", returnedOut
                for line in returnedOut:                    #rotate output to desired format
                    print "\t\tline: ", line                    #and save to "output[]"
                    outLine = []
                    outLine.append(dataset)
                    outLine.append("%s_%.2f" %(method, threshold))
                    outLine.append(line[0])
                    outLine.append(line[4])
                    outLine.append(line[5])             
                    print "\t\t\t", outLine
                    output.append(outLine) 
            # j = j+1                       
        # i = i+1
    writeOut(output, OUTPUT_FILE)

def errorLog(errorCode):#---------------------------------------------ERROR_LOG
    if(errorCode == 0):
        return "ERROR: NO VERSION SPECIFIED"
    else:
        return "THERE WAS AN ERROR"
        
    
def writeOut(output, fileName):#--------------------------------------WRITE_OUT
    #var dictionary
    #filename                                       #file to write to
    #output                                         #data to write
    #writer                                         #csv writer object
    
    with open(fileName, 'w') as file:               
        writer = csv.writer(file)
        for row in output:
            writer.writerow(row)
        if(output == logs):
            print "Log file written to ", fileName
        else:
            print "Results written to ", fileName
            logs.append(["Results written to " + fileName])

#--------------------------------------------------------------------------MAIN

INPUT_FILE = "Input/Normal.csv"            
OUTPUT_FILE = "Data Output/MyDataWord2VecWithStemming.csv"
LOG_FILE = "MyDataWord2VecWithStemming.txt"
VERSION = 6
INTERVAL_MODE = 'count'                              #options: time, count;
                                                    #options: words, categories;
#INTERVAL = 60000                                    #1 minute
#INTERVAL = 600000                                    #10 minutes
#INTERVAL = 1800000                                  #30 minutes
#INTERVAL = 3600000                                  # 1 hour
INTERVAL = 3
out = []                                            #data output to print
logs = []                                           #log  output to print
#f = open('dictNLTK.file', 'r')
#word2Vec = eval(f.read())                          #dictionary in key-value form where
                                                        #key = words and their synonymns
                                                        #value = the group that is entered
                                                            #the counter for that word
#f.close()

#f = open('dict.file', 'r')
#nltk = eval(f.read())
#f.close()

#wordsSeen = {}
#itemsSeen = {}

#getInput
file = getInputFile(INPUT_FILE)

#setup Log File
logs.append(["VERSION:\t" + str(VERSION)])
logs.append(["INPUT_FILE:\t" + INPUT_FILE])
logs.append(["INTERVAL_MODE:\t" + INTERVAL_MODE])

#process
if(VERSION == 1):
    out = evaluate(file)
elif(VERSION == 2):
    out = evaluate2(file)
elif(VERSION == 3):
    out = evaluate3(file)
elif(VERSION == 4):
    out = evaluate4(file, logs)
elif(VERSION == 5):
    out = evaluate5(file, logs)
elif(VERSION == 6):
    evaluate6(file, logs)
else:
    print "NO VERSION SPECIFIED"
    logs.append([errorLog(0)])
    writeOut(logs, LOG_FILE)
    quit()

#print wordsSeen
#countUniqueWords(file)

#print output to screen
#f = open('dictNLTK.file', 'w')
#f.write(str(word2Vec))
#f.close()

#f = open('dict.file', 'w')
#f.write(str(nltk))
#f.close()

#for line in out:
#   print line

#VERSION 1:     basic; category as bin              IN-PROGRESS -- functional
#               INPUTS:
#                   ideas.csv
#               TODO:
#                   - implement log
#VERSION 2:     words as bins                       IN-PROGRESS -- functional   
#               INPUTS:
#                   ideas2.csv
#               TODO:
#                   - implement log
#VERSION 3:     words as bins; separate by theme    IN-PROGRESS -- not functional
#               INPUTS:
#                   ideas_corrected.csv
#                   smallIdeas.csv
#               TODO:
#                   - fix bugs that arose in compilation
#                   - implement log
#VERSION 4:     super-words as bins                 IN-PROGRESS -- functional
#               INPUTS:
#                   ideas_corrected.csv
#                   smallIdeas.csv
#               TODO:
#                   improve time/accuracy 
#VERSION 5:     super-words as bins;                IN-PROGRESS -- functional
#               separate by theme
#               TODO:
#                   - flip data 
#VERSION 6:     full test                           IN-PROGRESS -- not functional

#printResults
#writeOut(out, OUTPUT_FILE)
writeOut(logs, LOG_FILE)