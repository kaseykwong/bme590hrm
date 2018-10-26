from file_io import read_data
from file_io import write_json
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import logging
import warnings


class ECG_data:

    def __init__(self, filename_in=''):
        """
        Initializes an instance of the ECG_data class.
        :param filename_in: name of the input file
        """

        self.filename = filename_in

        try:
            import logging
        except ImportError:
            logging.error("No such file")
            print("No Imported file")

        logging.basicConfig(filename='hrm_log.txt',
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)

        logging.info("%s%s", "Opened ", self.filename)

        try:
            open(self.filename, 'r')
        except IOError:
            logging.error(self.filename + ' not found')
        self.time, self.voltage = read_data(self.filename)

        # if len(self.time) != len(self.voltage):
        #     logging.error('Time and Voltage data arrays are not the '
        #                   'same length')
        #     raise RuntimeError

        if self.time == [] or self.voltage == []:
            logging.error('Time or voltage data is empty')
            raise RuntimeError
        self.hrm = []
        self.beattimes = []
        self.numbeats = 0
        self.maxV = max(self.voltage)
        self.minV = min(self.voltage)
        logging.info("ECG Voltage extremes found.")
        if abs(self.maxV) > 300 or abs(self.minV) > 300:
            logging.warning("Warning: Voltage is outside of ECG range "
                            "(>300 mV)")

        self.duration = self.time[len(self.time) - 1] - self.time[0]
        try:
            if self.duration < 5:
                raise RuntimeWarning
        #    print('Duration less than 5 seconds, Accuracy may be affected')
        except RuntimeWarning:
            logging.error('Duration is less than 5 seconds, calculation '
                          'accuracy may be affected.')

        self.peakdetect()

        if self.hrm > 180:
            logging.warning("Warning: Mean heart rate detected to be higher"
                            " than 180 bpm.")
        if self.hrm < 40:
            logging.warning("Warning: Mean heart rate detected to be lower"
                            " than 40 bpm.")

        self.output()

    def peakdetect(self):
        """
        This function performs peak detection and all the heart rate
        parameter calculations and assigns them to the class parameters

        Adapted from
        van Gent, P. (2016). Analyzing a Discrete Heart Rate Signal
        Using Python. A tech blog about fun things with Python and
        embedded electronics. Retrieved from:
        http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-
        heart-rate-signal-using-python-part-1/

        licensed under GNU 3.0 Open source license

        :return:
        """

        # if self.time == [] or self.voltage == []:
        #     logging.warning("Time and/or Voltage of " + self.filename +
        #                     " is empty")
        #     return

        voltage = pd.Series(data=self.voltage)
        fs = 1/(self.time[1] - self.time[0])
        hrw = 0.5
        mov_avg = voltage.rolling(int(hrw * fs)).mean()
        avg_hr = (np.mean(voltage))
        if avg_hr < 0 and abs(self.minV) - abs(avg_hr) > \
                abs(self.maxV) - abs(avg_hr):
            voltage = voltage + abs(avg_hr)+abs(self.minV)

        mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
        mov_avg = [(x+abs(avg_hr-abs(self.minV/2)))*1.2 for x in mov_avg]
        window = []
        peaklist = []
        listpos = 0
        for datapoint in voltage:
            rollingmean = mov_avg[listpos]
            if (datapoint < rollingmean) and (len(window) < 1):
                listpos += 1
            elif (datapoint > rollingmean):
                window.append(datapoint)
                listpos += 1
                if (listpos >= len(voltage)):
                    beatposition = listpos - len(window) + \
                                   (window.index(max(window)))
                    peaklist.append(beatposition)
                    window = []
            else:
                beatposition = listpos - len(window) + \
                               (window.index(max(window)))
                peaklist.append(beatposition)
                window = []
                listpos += 1

        ybeat = self.beat_voltage(peaklist, self.voltage)
        RR_list = self.find_RR(peaklist, fs)
        self.calc_bpm(RR_list)
        self.find_beat_time(peaklist, fs)

        # plt.plot(self.voltage, alpha=0.5, color='blue', label="raw signal")
        # plt.plot(mov_avg, color='green', label="moving average")
        # plt.scatter(peaklist, ybeat, color='red',
        #             label="average: %.1f BPM" % self.hrm)
        # plt.legend(loc=4, framealpha=0.6)
        # plt.show()

    def beat_voltage(self, peaklist, voltage):
        """
        Based on the indexing of peaks, determines the voltage at each peak
        :param peaklist: list of peak index locations
        :param voltage: voltage array of input
        :return: ybeat which is the voltage value of each peak
        """
        ybeat = [voltage[x] for x in peaklist]
        return ybeat

    def find_RR(self, peaklist, fs):
        """
        Finds the R-R peak intervals
        :param peaklist: list of peak index locations
        :param fs: sampling rate
        :return: list of R-R interval times
        """
        RR_list = []
        cnt = 0
        while (cnt < (len(peaklist) - 1)):
            RR_interval = (peaklist[cnt + 1] - peaklist[cnt])
            ms_dist = ((RR_interval / fs) * 1000.0)
            RR_list.append(ms_dist)
            cnt += 1

        return RR_list

    def calc_bpm(self, RR_list):
        """
        Calculates heart rate and counts number of beats in the dataset
        :param RR_list: list of R-R interval times
        :return: heart rate and number of beats
        """
        self.hrm = 60000 / np.mean(RR_list)
        logging.info("Heart Rate successfully calculated.")
        self.numbeats = len(RR_list)
        logging.info("Number of beats counted.")
        return self.hrm, self.numbeats

    def find_beat_time(self, peaklist, fs):
        """
        Identify the actual times of each beat
        :param peaklist: list of voltage peak index location
        :param fs: sampling rate
        :return: list of beat times
        """
        beats = []
        for row in peaklist:
            self.beattimes.append(float(row)/fs)
            beats.append(float(row)/fs)
        logging.info("Heart beat times recorded.")
        return beats

    def output(self):
        """Summarizes calculated outputs from the functions of this class.
        :return hrm_info: a dictionary containing all the object attributes
        """

        hrm_info = {'Mean Heart Rate': self.hrm,
                    'Max Voltage': self.maxV,
                    'Minimum Voltage': self.minV,
                    'Duration': self.duration,
                    'Number of Beats': self.numbeats,
                    'Times when beats occurred': self.beattimes
                    }

        write_json(self.filename, hrm_info)

        logging.info("%s%s", "Completed ", self.filename)

        return hrm_info


def main():
    """
    Main File to run process_data
    :return: instance of ECG_data
    """
    try:
        x = ECG_data('test0.csv')
    except IOError:
        print('main: File not Found')
        return
    except RuntimeError:
        print('Error in data found. Refer to log')
        return

    # print(x.time)
    # print(x.voltage)
    # print(x.duration)
    # print(x.maxV)
    # print(x.minV)
    # print(x.beattimes)
    # print(x.hrm)
    # print(x.numbeats)
    return x

if __name__ == "__main__":
    main()
