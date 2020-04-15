# Autor:    Jakub Svajka
# Datum:    25.11.2019      16:52
# Revised:  8.3.2020        11:55

from math import log10

def MAX(arr):
    """Finds biggest number in an array."""
    try:
        result = arr[0]
        for i in range(1, len(arr)):
            if result < arr[i]:
                result = arr[i]
        return result
    except:
        print("{MAX()} Generic Error.")
        return -1
    pass

def MIN(arr):
    """Finds smallest number in an array."""
    try:
        result = arr[0]
        for i in range(1, len(arr)):
            if result > arr[i]:
                result = arr[i]
        return result
    except:
        print("{MIN()} Generic Error.")
        return -1
    pass

def SUM(arr):
    """Sum of all numbers in an array."""
    try:
        result = 0
        for i in range(len(arr)):
            result += float(arr[i])
        return result
    except:
        print("{SUM()} Error: At least one value of an array is not a convertible number.")
        return -1
    pass

def AVG(arr):
    """Average of all numbers in an array."""
    try:
        result = 0
        size = len(arr)
        for i in range(size):
            result += float(arr[i])
        return result/size
    except:
        print("{AVG()} Error: At least one value of an array is not a convertible number.")
        return -1
    pass

def convertToDecibel(num):
    try:
        return 10*log10(num)
    except:
        print("Error. Cannot convert to decibel!")
        return -1
    pass