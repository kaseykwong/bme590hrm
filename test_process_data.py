import pytest
import process_data

# def test_duration():
#     with pytest.raises(RuntimeWarning):
#         process_data.ECG_data('sine.csv')

def test_ECG_data():
    '''
    This test function tests that the ECG_data class and related functions can accurately
    determine ECG beat data based on Moving Average algorithm. Verification using number
    of beats counted and max/min ECG voltage
    :return: No values returned, just assertions
    '''
    SineTest = process_data.ECG_data('sine.csv')
    assert SineTest.maxV == 1 and SineTest.minV == -1
    assert SineTest.numbeats == 7


def test_no_data():
    """
    This test determines if the ECG_data function can detect when the input file doesn't exist
    and properly throws and IOError
    :return:
    """
    with pytest.raises(IOError):
        process_data.ECG_data('test0.csv')

test1 = process_data.ECG_data('test2.csv')

def test_beat_voltage():
    """
    This test checks that the beat_voltage function can correctly determine the voltages
    of the peaks found
    :return:
    """
    peaklist = [2, 4, 6, 8]
    voltage = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    beat_list = [2, 4, 6, 8]
    assert test1.beat_voltage(peaklist,voltage) == beat_list

def test_find_RR():
    """
    This test checks that the find_RR function can create a list of all R-R intervals
    :return:
    """
    peaklist = [2, 4, 6, 8]
    fs = 1
    rr_list = [2000,2000,2000]
    assert test1.find_RR(peaklist,fs) == rr_list

def test_calc_bpm():
    """
    This test checks that the calc_bpm can accurately calculate the heart rate and number
    of beats in the data set
    :return:
    """
    rr_list = [2000,2000,2000]
    hrm, numbeats = test1.calc_bpm(rr_list)
    assert hrm == 30 and numbeats == 3

def test_find_beat_time():
    """
    This test checks that the find_beat_time function can accurately determine the time
    that each beat occurs at
    :return:
    """
    peaklist = [2, 4, 6, 8]
    fs = 1
    beattime = [2, 4, 6, 8]
    assert test1.find_beat_time(peaklist,fs)== beattime

