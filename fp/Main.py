'''
This is an algorithm that implements FP-Growth algorithm(Frequent Pattern).
Indepth explanation can be found here :http://slidewiki.org/deck/1506_fpgrowth-a-frequent-pattern-growth-approach#tree-1506-slide-22049-1-view

Outline: First the frequent items are found and then a table in a very specific format is generated.
The table is then used to create a "Tree", which we traverse and find frequent patterns-This we do recursively at each level

After mining frequent patterns, we check what type of frequent pattern are they(Max pattern, Closed pattern)

Note:Lot of formatting had to be done to get the data in the usable format and also to convert the results into required format in the course
'''



class Node:
    def __init__(self, id):
        self.id = id
        self.count = 0
        self.children = []
        self.parent = None

with open("topic-0.txt") as dFile:
    data = dFile.read().splitlines()
with open("vocab.txt") as dFile:
        vocab = dFile.read().splitlines()


min = len(data)*0.01 # minimum frequency
dic = {}
clearData = []
for line in data: #To count the occurences
    clearLine = []
    line = line.strip().split(" ")
    for e in line:
        e = e.strip()
        clearLine.append(e)
        if e in dic:
            dic[e] += 1
        else:
            dic[e] = 1
    clearData.append(clearLine)

# removing infrequent items
dic = {k:v for k, v in dic.items() if v >= min}

from operator import itemgetter
import itertools
d = sorted(dic.items(), key=itemgetter(1, 0), reverse = True)


fData = []
for line in clearData: #To transform data with only frequent items
    fLine = []
    for e in d:
        if e[0] in line:
            fLine.append(e[0])
    fData.append(fLine)

table = {}
root = Node("")
for line in fData: # To generate the table in a specific format
    t = root
    for e in line:
        f = None
        for n in t.children:
            if e == n.id:
                f = n

        if f is None:
            f = Node(e)
            f.count += 1
            f.parent = t
            t.children.append(f)
            t = f
            if e in table:
                table[e][1].append(t)
            else:
                table[e] = [dic[e], [t]]
        else:
            f.count += 1
            t = f
table = sorted(table.items(), key=lambda e: (e[1][0], e[0]), reverse = True)

# Function to create tree and then traverse recursively
def createTree(data, min, cnt):
    root = Node("")
    fre = {}
    for l in data:
        for e in l[1]:
            if e in fre:
                fre[e] += l[0]
            else:
                fre[e] = l[0]

    fre = {k: v for k, v in fre.items() if v >= min}
    d = sorted(fre.items(), key = itemgetter(1, 0), reverse = True)

    fData = []
    for line in data:
        fLine = []
        for e in d:
            if e[0] in line[1]:
                fLine.append(e[0])
        fData.append([line[0], fLine])

    table = {}
    for line in fData:
        t = root
        for e in line[1]:
            f = None
            for n in t.children:
                if e == n.id:
                    f = n

            if f is None:
                f = Node(e)
                f.count += line[0]
                f.parent = t
                t.children.append(f)
                t = f
                if e in table:
                    table[e][1].append(t)
                else:
                    table[e] = [fre[e], [t]]
            else:
                f.count += line[0]
                t = f
    table = sorted(table.items(), key=lambda e: (e[1][0], e[0]), reverse=True)

    patterns = []
    # terminating condition
    if isUnbranched(root):
        elements = [a for a, b in table]
        for i in range(len(elements)):
            patterns1 = itertools.combinations(elements, i + 1)
            for e in patterns1:
                patterns.append([fre[e[0]], e])
    # If it is branced then a new tree with the items above this level is generated and then traverse
    else:
        tableL = len(table)
        for i in range(tableL):
            ind = tableL - i - 1
            data1 = []
            for n in table[ind][1][1]:
                line = []
                t = n.parent
                while t.id != "":
                    line.append(t.id)
                    t = t.parent
                data1.append([n.count, line])
            prefixes = createTree(data1, min, table[ind][1][0])
            for i in prefixes:
                patterns.append([i[0], i[1] + (table[ind][0], )])
            patterns.append([table[ind][1][0], (table[ind][0], )])

    return patterns

# function to check if the tree is branced or not
def isUnbranched(root):
    while (len(root.children) > 0):
        if (len(root.children) > 1):
            return False
        root = root.children[0]
    return True

tableL = len(table)
patterns = []

# start code which initializes the algorithm
for i in range(tableL):
    ind = tableL - i - 1
    data1 = []
    for n in table[ind][1][1]:
        line = []
        t = n.parent
        while t.id != "":
            line.append(t.id)
            t = t.parent
        data1.append([n.count, line])
    prefixes = createTree(data1, min, table[ind][1][0])
    for i in prefixes:
        patterns.append([i[0], i[1] + (table[ind][0], )])
    patterns.append([table[ind][1][0], (table[ind][0], )])

patterns = [[i[0], list(i[1])] for i in patterns]
dict1 = {}
for l in vocab:
    l = l.split()
    dict1[l[0]] = l[1]


decode = []
for l in patterns:
    x = [dict1[i] for i in l[1]]
    decode.append([l[0], " ".join(x)])
decode = sorted(decode, key=lambda e: (e[0], e[1]), reverse=True)



patterns = [[i[0], set(i[1])] for i in patterns]
closedP = []
maxP = []

# Checking the type of pattern they are
for i in range(len(patterns)):
    isClosed = True
    isMax = True
    for j in range(len(patterns)):
        if i != j:
            if patterns[i][1].issubset(patterns[j][1]) and patterns[j][0] >= patterns[i][0]:
                isClosed = False
                break
    for j in range(len(patterns)):
        if i != j:
            if patterns[i][1].issubset(patterns[j][1]):
                isMax = False
    if isClosed:
        closedP.append([patterns[i][0], patterns[i][1]])
    if isMax:
        maxP.append([patterns[i][0], patterns[i][1]])

closedP = [list(i) for i in closedP]
maxP = [list(i) for i in maxP]

closedD = []
for l in closedP:
    x = [dict1[i] for i in l[1]]
    closedD.append([l[0], " ".join(x)])

maxD = []
for l in maxP:
    x = [dict1[i] for i in l[1]]
    maxD.append([l[0], " ".join(x)])

closedD = sorted(closedD, key=lambda e: (e[0], e[1]), reverse=True)
maxD = sorted(maxD, key=lambda e: (e[0], e[1]), reverse=True)

with open("pattern-0.txt", "w") as wFile:
    for i in decode:
        wFile.write(str(i[0]) + " " + i[1] + "\n")

with open("closed-0.txt", "w") as wFile:
    for i in closedD:
        wFile.write(str(i[0]) + " " + i[1] + "\n")

with open("max-0.txt", "w") as wFile:
    for i in maxD:
        wFile.write(str(i[0]) + " " + i[1] + "\n")
