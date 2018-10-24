import file_io
import pytest

def test_read_data():
    """
    This checks that the read_data function collects the correct time and voltage data
    :return:
    """
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
    """
    This test checks that the is_number function can determine if an input is a floating point
    number or a string that can or cannot be converted to a float
    :return:
    """
    test1 = 10.8
    assert file_io.is_number(test1) == True

    test2 = '5.93'
    assert file_io.is_number(test2) == True

    test3 = 'FIVE'
    assert file_io.is_number(test3) == False
    # with pytest.raises(ValueError):
    #     file_io.is_number('FIVE')
    #print(file_io.is_number(test3))

