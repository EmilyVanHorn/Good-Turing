import csv

def writeOut(output, fileName):#--------------------------------------WRITE_OUT
    #var dictionary
    #filename                                       #file to write to
    #output                                         #data to write
    #writer                                         #csv writer object
    
    with open(fileName, 'w') as file:               
        writer = csv.writer(file)
        for row in output:
            writer.writerow(row)
        else:
            print "Results written to ", fileName

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



OUTPUT_FILE = "Data Output/fullProjectTest.csv"
datasets = ['g','r','e','e','n']                #the list of input filenames
versions = [func1(),func2(),func3(),func4()]    #array of functions to try out
vText = ['p','i','n','k']                       #strings associated with the function of 
                                                    #"versions[]"
output = []                                     #output to be sent to csv
outLine = []                                    #one line of output taken from "returnedOut"
i = 0

output.append(["dataset", "method",             #header
               "timeSlice", "probability"])

for input_file in datasets:                     #for each dataset
    print "datasets: ", input_file              
    j = 0                   
    for function in versions:                       #run each version of the program
        returnedOut = function                      #output from this version
        print "\treturnedOut: ", returnedOut
        for line in returnedOut:                    #rotate output to desired format
            print "\t\tline: ", line                    #and save to "output[]"
            outLine = []
            outLine.append(datasets[i])
            outLine.append(vText[j])
            outLine.append(line[0])
            outLine.append(line[3])             #---> !!!this will be 4 in the real code!!!
            print "\t\t\t", outLine
        j = j+1
        output.append(outLine)                      
    i = i+1
    
print "Output"                                  #print output to terminal 
for item in output:
    print item
    
    
writeOut(output, OUTPUT_FILE)