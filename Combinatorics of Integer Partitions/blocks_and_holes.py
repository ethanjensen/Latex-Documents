import math

def fact(n):
    if n == 1:
        return 1
    else:
        return n * fact(n-1)

def getRecombinations(blocks):
    recombinations = [blocks]
    ##Shouldn't have to do this to get an arbitrary partition.
    keyList = list(blocks.keys())
    for i in range(0, len(keyList)):
        key1 = keyList[i]
        partition = removeKey(blocks, key1)
        newKeyList = list(partition.keys())
        for j in range(0, len(newKeyList)):
            key2 = newKeyList[j]
            newPartition = recombine(partition, key1, key2)
            for partition2 in getRecombinations(newPartition):
                if partition2 not in recombinations:
                    recombinations.append(partition2)
    return recombinations

def removeKey(blocks, key):
    partition = blocks.copy()
    partition[key] = partition[key] - 1
    if partition[key] == 0:
        del partition[key]
    return partition

def recombine(inputPartition, key1, key2):
    partition = removeKey(inputPartition, key2)
    key3 = key1 + key2
    if key3 in partition:
        partition[key3] = partition[key3] + 1
    else:
        partition[key3] = 1
    return partition

def getRecombinationNumber(blocks, holes):
    total = 0
    blocks = sort(blocks)
    holes = sort(holes)
    if len(blocks.keys()) == 1:
        key1 = next(iter(blocks.copy()))
        total = fact(blocks[key1])
        for key2 in iter(holes.copy()):
            if (key2/key1).is_integer():
                total = int(total/(fact(key2/key1)**holes[key2]))
            else:
                total = 0
    else:
        key1 = next(iter(blocks.copy()))
        blocks = removeKey(blocks, key1)
        for key2 in validKeys(key1, holes):
            value2 = holes[key2]
            newHoles = holes.copy()
            newHoles = place(newHoles, key1, key2)
            total = total + value2 * getRecombinationNumber(blocks, newHoles)
    return total

def sort(partition):
    sortedPartition = dict()
    sortedList = sorted(list(partition.keys()), reverse = True)
    for i in range(0, len(sortedList)):
        sortedPartition[sortedList[i]] = partition[sortedList[i]]
    return sortedPartition

def validKeys(key1, holes):
    validKeys = []
    for key2 in holes:
        if not key2 < key1:
            validKeys.append(key2)
    return validKeys

def place(holes, key1, key2):
    holes = removeKey(holes, key2)
    key3 = key2 - key1
    if key3 != 0:
        if key3 not in holes.keys():
            holes[key3] = 1
        else:
            holes[key3] = holes[key3] + 1
    return holes

def getRecombinationList(blocks):
    recombinationList = []
    holes = getRecombinations(blocks)
    for hole in holes:
        recombinationList.append([hole, getRecombinationNumber(blocks, hole)])
    return recombinationList

def getEvenZeta(n):
    if n == 1:
        return zetaValues[0]
    else:
        allCombos = getRecombinationList({1 : n})
        final_terms = solveSystem(allCombos)
        #Counting the amount of zeta(n) found inside the final_terms.
        total = collectFinalTerms(final_terms)
        fraclist = [(1,6**n),(-fact(n),fact(2*n+1))]
        for term in final_terms:
            fraclist.append(getFractionFor(term))
        f = addFractions(fraclist)
        f = (int(f[0]/math.gcd(f[0],f[1]*total)), int(f[1]*total/math.gcd(f[0],f[1]*total)))
        f = (abs(f[0]), abs(f[1]))
        return f

def solveSystem(allCombos):
    final_terms = []
    del allCombos[0]
    while (len(allCombos) > 0):
        partialCombos = getRecombinationList(allCombos[0][0])
        multiplier = int(allCombos[0][1] / partialCombos[0][1])
        partialCombos[0][1] = -multiplier
        final_terms.append(partialCombos[0])
        del partialCombos[0]
        del allCombos[0]
        substitute(partialCombos, allCombos, multiplier)
    return final_terms

def substitute(partialCombos, allCombos, multiplier):
    for partition2 in partialCombos:
        inside = False
        for partition1 in allCombos.copy():
            if(partition1[0] == partition2[0]):
                partition1[1] = partition1[1] - multiplier * partition2[1]
                inside = True
        if(not inside):
            partition2[1] =  - partition2[1] * multiplier
            allCombos.append(partition2)

def collectFinalTerms(final_terms):
    total = 0
    badvalues = []
    for i in range (0, len(final_terms)):
        if len(list(final_terms[i][0].values())) == 1 and list(final_terms[i][0].values())[0] == 1:
            total = total + final_terms[i][1]
            badvalues.append(i)
    badvalues.reverse()
    for i in badvalues:
        del final_terms[i]
    return total

def getFractionFor(term):
    partition = term[0]
    n = term[1]
    d = 1
    for key in list(partition.keys()):
        value = partition[key]
        n = n * zetaValues[key -1][0] ** value
        d = d * zetaValues[key -1][1] ** value
    return (int(n/math.gcd(n,d)), int(d/math.gcd(n,d)))

def addFractions(fracList):
    outputfraction = (0,1)
    for fraction in fracList:
        n = fraction[1]*outputfraction[0] + fraction[0]*outputfraction[1]
        d = outputfraction[1] * fraction[1]
        outputfraction = (int(n/math.gcd(n,d)), int(d/math.gcd(n,d)))
    return outputfraction

zetaValues = [(1,6)]

n = int(input("Calculate Zeta(2n). Select a value for n> "))
for i in range(2,n+1):
    zetaValues.append(getEvenZeta(i))

print(zetaValues[n-1])
