import math

def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n-1)

def getRecombinations(blocks):
    recombinations = [blocks]
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

def addFractions(fracList):
    outputfraction = (0,1)
    for fraction in fracList:
        n = fraction[1]*outputfraction[0] + fraction[0]*outputfraction[1]
        d = outputfraction[1] * fraction[1]
        outputfraction = (int(n/math.gcd(n,d)), int(d/math.gcd(n,d)))
    return outputfraction

print(getRecombinations({1:3}))

def spicySum(k):
    total = 0
    i = 0
    while (i < k/2):
        total = total + (-1)**i * fact(k)/(fact(i)*fact(k-i))*(k-2*i)**(2+k)
        print("total:",total)
        i = i + 1
    total = total - (1/6)*2**(k-1)*fact(2+k)*k
    return total

print(spicySum(12))
