import pytest
import process_data

# def test_duration():
#     with pytest.raises(RuntimeWarning):
#         process_data.ECG_data('sine.csv')


def test_ECG_data():
    SineTest = process_data.ECG_data('sine.csv')
    assert SineTest.maxV == 1 and SineTest.minV == -1
    assert SineTest.numbeats == 7


def test_empty_data():
    with pytest.raises(RuntimeError):
        process_data.ECG_data('test1.csv')


def test_no_data():
    with pytest.raises(IOError):
        process_data.ECG_data('test0.csv')

test1 = process_data.ECG_data('test2.csv')


def test_beat_voltage():
    peaklist = [2, 4, 6, 8]
    voltage = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    beat_list = [2, 4, 6, 8]
    assert test1.beat_voltage(peaklist, voltage) == beat_list


def test_find_RR():
    peaklist = [2, 4, 6, 8]
    fs = 1
    rr_list = [2000, 2000, 2000]
    assert test1.find_RR(peaklist, fs) == rr_list


def test_calc_bpm():
    rr_list = [2000, 2000, 2000]
    hrm, numbeats = test1.calc_bpm(rr_list)
    assert hrm == 30 and numbeats == 3


def test_find_beat_time():
    peaklist = [2, 4, 6, 8]
    fs = 1
    beattime = [2, 4, 6, 8]
    assert test1.find_beat_time(peaklist, fs) == beattime
