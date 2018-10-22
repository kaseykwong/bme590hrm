import csv
import numpy
import logging
import sys

def is_number(input):
    try:
        if float(input) and numpy.isreal(float(input)):
            return True
        else:
            raise ValueError
    except ValueError:
        logging.warning('Dataset contains non-real or non-numerical values. Interpolating data')
        return False

def read_data(filename):
    """read the data from the csv input file. Checks to see if file exists and checks for bad data

    :param filename: input file name
    :return: time = time array, voltage = voltage array
    """
    try:
        file = open(filename,'r')

    except IOError:
        print("File Not Found")
        logging.error('File Not Found')
        #sys.exit("File Not Found")

    time = []
    voltage = []
    temp = csv.reader(file,delimiter=',')
    #if (len(temp[0]) == len(temp[1])):
    for row in temp:
        if (is_number(row[0])) and (is_number(row[1])):
            temptime = float(row[0])
            tempvolt = float(row[1])

            time.append(temptime)
            voltage.append(tempvolt)



    #timef = [float([x]) for x in time]
    #voltagef = [float([x]) for x in voltage]

    return time, voltage






def main():
    [xtime, xvoltage] = read_data("./test_data/test_data0.csv")
    print(xtime)
    print(xvoltage)

if __name__ == "__main__":
    main()

