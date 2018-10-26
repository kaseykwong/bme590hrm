import pytest
import process_data

# def test_duration():
#     with pytest.raises(RuntimeWarning):
#         process_data.ECG_data('sine.csv')


def test_ECG_data():
    SineTest = process_data.ECG_data('sine.csv')
    assert SineTest.maxV == 1 and SineTest.minV == -1
    assert SineTest.numbeats == 7


def test_ECG_data2():
    test = process_data.ECG_data('./test_data/test_data9.csv')
    assert test.maxV == 0.255 and test.minV == -1.07
    assert test.numbeats == 28


# def test_high_volt():
#     test = process_data.ECG_data('./test_data/test_data32.csv')
#


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


def test_output():
    import json
    test4 = process_data.ECG_data('./test_data/test_data2.csv')

    output_1 = {"Mean Heart Rate": 62.810252254077604,
                "Max Voltage": 1.375,
                "Minimum Voltage": -0.59,
                "Duration": 27.775,
                "Number of Beats": 31,
                "Times when beats occurred": [0.24600000000000002,
                                              1.1880000000000002,
                                              2.133, 3.096, 4.104,
                                              5.136, 6.1080000000000005,
                                              7.047000000000001,
                                              7.9830000000000005,
                                              8.916, 9.903, 10.89, 11.88,
                                              12.849, 13.827, 14.784, 15.72,
                                              16.704, 17.694000000000003,
                                              18.666, 19.581,
                                              20.490000000000002,
                                              21.426000000000002,
                                              22.386000000000003,
                                              23.355, 24.315, 25.242, 26.163,
                                              27.075000000000003,
                                              27.96, 28.884, 29.859]}
    assert test4.output() == output_1
