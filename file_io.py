import csv
import numpy
import logging
import json


def is_number(input):
    """
    Check if the input is a floating point number and if the input is a real
    number
    :param input: value
    :return: Boolean of whether or not the value passes
    """
    try:
        float(input)
        if numpy.isreal(float(input)):
            return True
        else:
            raise ValueError
    except ValueError:
        logging.warning('Dataset contains non-real or non-numerical values.')
        return False


def read_data(filename):
    """read the data from the csv input file. Checks to see if file exists and
    checks for bad data. Should automatically ensure that time and voltage
    arrays end up as equal size arrays

    :param filename: input file name
    :return: time = time array, voltage = voltage array
    """

    file = open(filename, 'r')

    # except IOError:
    #     print("File Not Found")
    #     return
    #    logging.error('File Not Found')
    time = []
    voltage = []
    temp = csv.reader(file, delimiter=',')
    for row in temp:
        if (is_number(row[0])) and (is_number(row[1])):
            temptime = float(row[0])
            tempvolt = float(row[1])

            time.append(temptime)
            voltage.append(tempvolt)

    return time, voltage


def write_json(filename, info):
    """Write data to .json file
    :param filename: Output filename
    :param info: Dictionary containing data to write
    :return:
    """
    json_filename = filename.replace('.csv', '.json')
    json_file = open(json_filename, "w")
    json.dump(info, json_file)
    json_file.close

    return


def main():
    try:
        xtime, xvoltage = read_data('./test1.csv')
    except IOError:
        print('main: File not Found')
        return
    print(xtime)
    print(xvoltage)

    print(is_number('FIVE'))

if __name__ == "__main__":
    main()
