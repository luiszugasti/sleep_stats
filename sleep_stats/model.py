from sktime.forecasting.all import *
from loadData import *

def main():
    sleepArray, timeInBedArray = dataLoader()
    print(sleepArray)
    print(timeInBedArray)


if __name__ == '__main__':
    main()