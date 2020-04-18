import math
import operator
from termcolor import cprint

results = dict()  # will store tuples of numerical results and operation strings
operators = [operator.add, operator.sub, operator.mul, operator.truediv, operator.pow]
opsAndStrs = {operator.add: '+', operator.sub: '-', operator.mul: '*', operator.truediv: '/', operator.pow: '^'}
inputs = []  # will contain all combinations inputs with and without factorials


# returns the result of performing a given operation and optional factorial on two numbers
def operation(num1, op, num2, fac):
    if num1 is None:
        return num2

    if op == operator.pow and (num1 > 15 or num2 > 15):
        return None

    # decimal value
    if op is operator.truediv and op(num1, num2) != int(num1/num2):
        return None

    if fac == 1:
        if op(num1, num2) > 20 or op(num1, num2) < 1:
            # can't do factorial
            return None
        if op(num1, num2) == math.factorial(op(num1, num2)):
            # number is 1 or 2 and factorial equals number
            # eliminate so non-fac version is used instead
            return None
        return math.factorial(op(num1, num2))

    return op(num1, num2)


# returns copy of given list with element removed
def listWithoutElement(list, element):
    index = list.index(element)
    copy = list.copy()
    del copy[index]
    return copy


def getFacStr(fac):
    if fac == 1:
        return "!"
    return ""


# returns updated operation string
def updateOpStr(opStr, op, num, fac):
    if op is not None:
        opStr = "(" + opStr + opsAndStrs[op] + " " + str(num[1]) + ")" + getFacStr(fac) + " "
    else:
        opStr += " "
    return opStr


# recursively generates all possible results
# num is a tuple like (5, '5') or (120, '5!')
# current is the intermediate numerical result
# remaining is a list of nums left to be used (for this combo)
# opStr contains the operation string
def rf(op, current, num, fac, remaining, opStr):
    if len(remaining) > 0 and operation(current, op, num[0], fac) is not None:
        opStr = updateOpStr(opStr, op, num, fac)
        for nextNum in remaining:
            for nextOp in operators:
                for nextFac in range(0, 2):
                    result = rf(nextOp, operation(current, op, num[0], fac),
                                      nextNum, nextFac, listWithoutElement(remaining, nextNum), opStr)
                    if result is not None:
                        # map resulting number to string of result
                        results[result[0]] = result[1]
    else:
        if operation(current, op, num[0], fac) is not None:
            # opStr += opsAndStrs[op] + " " + str(num[1]) + " "
            opStr = updateOpStr(opStr, op, num, fac)[1:-2]  # remove outer parentheses
            return abs(operation(current, op, num[0], fac)), opStr
        return None


# returns copy of given list with item appended to the end
def appendToNewList(element, prevList):
    newList = prevList.copy()
    newList.append(element)
    return newList


# sets inputs list with all combinations of factorial and non-factorial values
def comb(currentList, remainingList):
    if len(remainingList) == 0:
        inputs.append(currentList)
    else:
        comb(appendToNewList(remainingList[-1], currentList), remainingList[:-1])
        # make sure n! does not equal n
        if remainingList[-1][0] not in (1, 2):
            comb(appendToNewList((math.factorial(remainingList[-1][0]), remainingList[-1][1] + '!'), currentList), remainingList[:-1])


# returns list of primes up (and including) max
def sieve(max):
    nums = []
    for i in range(3, max+1):
        nums.append(i)
    for d in range(2, max+1):
        for n in nums:
            if n % d == 0 and n != d:
                nums.remove(n)

    return nums


# handle user input and generate numbers and input (combinations) lists
maxBoardVal = 121
primes = sieve(maxBoardVal)
numInput = input('Enter the integers you want to do math with, separated by commas.\n')
numInput = numInput.strip(' ').split(',')  # convert to list
numbers = []
for n in numInput:
    numbers.append((int(n), str(n).strip(' ')))
comb([], numbers)

# generate results list
for inputList in inputs:
    for n in inputList:
        rf(None, None, n, 0, listWithoutElement(inputList, n), n[1])


# filter results
results = dict(filter(lambda x: x[0] is not None, results.items()))
results = dict(filter(lambda x: primes[-1] + primes[-2] >= x[0] > 0, results.items()))
results = dict(map(lambda x: (int(x[0]), x[1]), results.items()))  # remove trailing .0's

primeSums = dict()  # keys are even sum and key is list of prime tuples
primeResults = dict()

# fill dict of even numbers with the primes that sum to them
for r in results.keys():
    if r % 2 == 0:
        primeSums[r] = set()
        for p in primes:
            if primes.__contains__(r-p):
                pTup = (min(p, r-p), max(p, r-p))
                primeSums[r].add(pTup)

# fill dict of primes that sum to available even numbers
for p in primes:
    primeResults[p] = set()
    for r in results.keys():
        if primes.__contains__(r-p):
            primeResults[p].add(str(r) + " - " + str(r-p))

# add results of goldbach sums to results list
for p in primeResults.keys():
    try:
        results[p] += ' or '
    except:
        results[p] = ''  # initialize string
    finally:
        for r in primeResults[p]:
            results[p] += r + ' or '
        results[p] = results[p][:-3]

# list primes that sum to each even number at end of equation strings
for n in results.keys():
    if n % 2 == 0 and n > 5:
        results[n] += ' is equal to '
        for pTup in primeSums[n]:
            results[n] += str(pTup[0]) + " + " + str(pTup[1]) + ' and '
        results[n] = results[n][:-4]

# print results, color coded for even/odd
for val in sorted(results.keys()):
    color = 'blue'
    if primes.__contains__(val):
        color = 'green'
    if val % 2 == 0:
        color = 'red'
    cprint(str(val) + " = " + results[val], color)
