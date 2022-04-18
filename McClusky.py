# Quine McClusky Technique
# By Pandula

# Although i used a list called essentialPrimes, later i added primes to that list to keep it simple.
# therefore note that essentialPrimes have all the prime implicants.

def checkEssentials(list1, list2):     # Generates uncrossed essential primes
    global essentialPrimes
    for i in list1:
        if i not in list2 and i not in essentialPrimes:
            essentialPrimes.append(i)


def dec(x):  # bin>>dec converter
    return int(x, 2)


def isBitShift_1(x, y):       # This function captures if bit/character differance is 1
    for i in range(len(x)):
        if x[i] == '_':
            if x[i] != y[i]:
                return False
    n = x.replace('_', '')
    m = y.replace('_', '')
    c = 0
    for i in range(len(n)):
        if n[i] != m[i]:
            c+=1
    if c!=1:
        return False
    return True


def dash(x, y):     # generates _ terms for 2 inputs
    output = ''
    for i in range(len(x)):
        if x[i] == y[i]:
            output += x[i]
        else:
            output += '_'
    return output


essentialPrimes = []

n = int(input('Enter number of Variables: '))
minTerms = list((map(int,input("Enter minterms separated by a space: ").split(' '))))

''' Some Test Data
2,4,5,6,7
0, 1, 3, 7, 8, 9, 11, 15
0,1,2,5,6,7,9,10,11,14
0,1,3,7,8,9,11,15
0,1,2,3,6,8,9,10,11,17,20,21,23,25,28,30,31
0,2,3,6,7,8,10,12,13
'''
# minTerms =[0,1,2,3,6,8,9,10,11,17,20,21,23,25,28,30,31]       # <<<< ENTER MIN TERMS MANUALLY TO TEST
# minTerms =[0,2,3,6,7,8,10,12,13]
# minTerms =[2,4,5,6]
# minTerms = [0, 1, 3, 7, 8, 9, 11, 15]
# minTerms = [0,2,3,6,7,8,10,12,13]

# n = 5                                                         # <<<< ENTER number of variables MANUALLY TO TEST
group1 = []
for i in range(n + 1):
    group1.append([])



binaryMinTerms = []

for i in minTerms:
    binaryTerm = bin(i)[2:]
    if binaryTerm == n:
        continue
    else:
        while len(binaryTerm) < n:
            binaryTerm = '0' + binaryTerm

    binaryMinTerms.append(binaryTerm)  # Gets the binary terms of each min term
#print(binaryMinTerms)
for i in binaryMinTerms:
    group1[i.count('1')].append(i)  # Group minterms according to number of '1's to the group1

check1 = []   # Check lists(1 and 2) are used to mine essential prime implicants.
check2 = []
group2 = []   # Group 1 and group 2 stores the data that is processing at the moment
for i in range(n):
    group2.append([])

# print(group1)
for group in group1[:-1]:
    for i in group:
        if i not in check1:check1.append([dec(i),i])
        for j in group1[group1.index(group) + 1]:
            if j not in check1: check1.append([dec(j),j])
            if dec(i) > dec(j):
                continue
            elif isBitShift_1(i, j):
                if i not in check2: check2.append([dec(i),i])
                if j not in check2: check2.append([dec(j),j])
                group2[group1.index(group)].append([[dec(i), dec(j)], dash(i, j)])

for i in group2:
    if i == []:
        group2.remove([])

'''
for i in group2:
    print(i)
'''

checkEssentials(check1, check2)
#print(essentialPrimes)
kill = 1
while True:             # This loop does the table calculation and generates the essential prime Is.
    if len(group2) == 1 :
        for i in group2[0] :
            essentialPrimes.append(i)
        break

    group1 = group2
    group2 = []
    check1 = []
    check2 = []

    for i in range(len(group1) - 1):
        group2.append([])

    for i in group1[:-1]:
        for j in i:
            if j[-1] not in check1: check1.append(j)
            for k in group1[group1.index(i) + 1]:
                if k[-1] not in check1: check1.append(k)
                if isBitShift_1(j[-1], k[-1]):
                    kill = 0
                    if j[-1] not in check2: check2.append(j)
                    if k[-1] not in check2: check2.append(k)
                    group2[group1.index(i)].append([j[0] + k[0], dash(j[-1], k[-1])])

    for i in group2:  # To remove unused lists
        if i == []:
            group2.remove([])

    checkEssentials(check1, check2)
    if len(group2)==0 :
        break
    if len(group2[0]) == 0:
        break
    if len(group2[0]) != 0 and len(group2)==1:
        essentialPrimes.append(group2[0][0])
        break
#print(essentialPrimes)

filtered = []

for i in essentialPrimes:  # This function removes duplicates in essentialPrimes(if there are any)
    x =i[0]
    if type(x) is list:
        x.sort()
    y = [x,i[1]]
    if y not in filtered:
        filtered.append(y)

'''
for i in filtered:
    print(i)
'''
chosen = []   # This is where the selected essential prime implicants are stored
#print(filtered)
copylist=minTerms.copy()

copy2 = filtered.copy()      # Turns integers to lists and make them ready to iterate.
for i in copy2:
    if type(i[0]) is int :
        filtered[copy2.index(i)][0] = [filtered[copy2.index(i)][0]]
#print(filtered)

'''
Following code consists the Graphical crossing method we used at last. I discovered an
algorithm that is easy to use and simple(There can be bugs)  :) 
'''

for i in copylist:
    counti = 0
    memory = []
    for j in filtered:
        if i in j[0]:
            counti+=1
            memory.append(j)
    if counti==1:
        if memory[0] not in chosen: chosen.append(memory[0])

        for a in memory[0][0]:
            if a in minTerms: minTerms.remove(a)


for i in chosen:
    filtered.remove(i)

while len(minTerms) > 0 :
    maxx = 0
    nextTerm = 0
    for i in filtered :
        c = 0
        for j in i[0] :
            if j in minTerms :
                c += 1
        if c>maxx :
            maxx=c
            nextTerm = i
    filtered.remove(nextTerm)
    chosen.append(nextTerm)
    for b in nextTerm[0]:
        if b in minTerms: minTerms.remove(b)

for i in chosen:  # Finally!
    print(i[1])











