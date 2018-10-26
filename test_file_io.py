import file_io
import pytest


def test_read_data():
    filename = './test_data/test_data1.csv'
    time, voltage = file_io.read_data(filename)
    assert float(time[0]) == 0
    assert float(voltage[0]) == -0.145
    assert float(time[1]) == 0.003
    assert float(voltage[1]) == -0.145

    filename = './test_data/test_data2.csv'
    time, voltage = file_io.read_data(filename)
    assert float(time[0]) == 0
    assert float(voltage[0]) == -0.345
    assert float(time[1]) == 0.003
    assert float(voltage[1]) == -0.345


def test_is_number():
    test1 = 10.8
    ans1 = True
    assert file_io.is_number(test1) == ans1

    test2 = '5.93'
    ans2 = True
    assert file_io.is_number(test2) == ans2

    test3 = 'FIVE'
    ans3 = False
    assert file_io.is_number(test3) == ans3
    # with pytest.raises(ValueError):
    #     file_io.is_number('FIVE')
    # print(file_io.is_number(test3))


def test_bad_data():
    time2, voltage2 = file_io.read_data('test2.csv')
    assert len(time2) == len(voltage2)


def test_write_json():
    import json
    output_1 = {"Name": "Kasey",
                "Age": 23,
                "Favorite Color": "Black"}
    filename = "TestOutput.csv"
    file_io.write_json(filename, output_1)

    read_file = json.load(open('TestOutput.json'))
    assert read_file == {"Name": "Kasey",
                         "Age": 23,
                         "Favorite Color": "Black"}
