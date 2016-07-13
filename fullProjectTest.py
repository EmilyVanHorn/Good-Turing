#import gensim
#from gensim import models

#model = models.Word2Vec.load('text8Model')
#dict = open('dict.file', 'r')
#dict = eval(dict.read())
#newDict = {}

#for word in dict.keys():
#    current = dict.get(word)
#    best = model.similarity(word, current)
#    working = current
#    for word in dict.keys()


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




datasets = ['g','r','e','e','n']
versions = [func1(),func2(),func3(),func4()]
vText = ['p','i','n','k','!']
output = []
outLine = []
i = 0

for input_file in datasets:
    print "datasets: ", input_file
    for function in versions:
        returnedOut = function
        print "\treturnedOut: ", returnedOut
        for line in returnedOut:
            print "\t\tline: ", line
            outLine = []
            outLine.append(datasets[i])
            outLine.append(vText[i])
            outLine.append(line[3])
            print "\t\t\t", outLine
        output.append([outLine])
    i = i+1
    
print "Output"    
for item in output:
    print item