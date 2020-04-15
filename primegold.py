import math
import operator

results = []
operators = [operator.add, operator.sub, operator.mul, operator.truediv]
inputs = []  # will contain all combinations of factorial and not


def operation(num1, op, num2, fac):
    if num1 is None:
        return num2

    # decimal value
    if op is operator.truediv and op(num1, num2) != int(num1/num2):
        return None

    if fac == 1:
        if op(num1, num2) > 20:
            print("too big")
            return op(num1, num2)
        if op(num1, num2) < 1:
            print("negative")
            return op(num1, num2)
        if op(num1, num2) == 0:
            print("zerooo")
            return op(num1, num2)
        return math.factorial(op(num1, num2))
    return op(num1, num2)


def listWithoutElement(list, element):
    index = list.index(element)
    copy = list.copy()
    del copy[index]
    return copy


def rf(op, current, num, fac, remaining):
    if len(remaining) > 0:
        for nextNum in remaining:
            for nextOp in operators:
                for nextFac in range(0, 2):
                    if operation(current, op, num, fac) is not None:
                        results.append(rf(nextOp, operation(current, op, num, fac),
                                          nextNum, nextFac, listWithoutElement(remaining, nextNum)))
    else:
        return operation(current, op, num, fac)


def appendToNewList(element, prevList):
    newList = prevList.copy()
    newList.append(element)
    return newList


def comb(currentList, remainingList):
    if len(remainingList) == 0:
        inputs.append(currentList)
    else:
        comb(appendToNewList(remainingList[-1], currentList), remainingList[:-1])
        comb(appendToNewList(math.factorial(remainingList[-1]), currentList), remainingList[:-1])


numbers = [5, 7, 10]
comb([], numbers)
print(inputs)

for numList in inputs:
    for n in numList:
        rf(None, None, n, 0, listWithoutElement(numList, n))

print(results)

# filter results
results = list(filter(lambda x: x is not None, results))
results = list(dict.fromkeys(results))
print(results)

results = list(filter(lambda x: 241 > x > 0, results))
results.sort()
print(results)

# # get only evens
# results = list(filter(lambda x: x % 2 == 0, results))
# print(results)

# cast all to int
results = list(map(lambda x: int(x), results))
# print(results)

for r in results:
    print(r, end=" ")
