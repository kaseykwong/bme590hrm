from file_io import read_data
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import logging
import warnings


class ECG_data:

    def __init__(self,filename_in = ''):
        """
        Initializes an instance of the ECG_data class
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
            open(self.filename,'r')
        except IOError:
            logging.error(self.filename +' not found')
        self.time, self.voltage = read_data(self.filename)

        if len(self.time) != len(self.voltage):
            logging.error('Time and Voltage data arrays are not the same length')
            raise RuntimeError

        if self.time == [] or self.voltage == []:
            logging.error('Time or voltage data is empty')
            raise RuntimeError
        self.hrm = []
        self.beattimes = []
        self.numbeats = 0
        self.maxV = max(self.voltage)
        self.minV = min(self.voltage)

        self.duration = self.time[len(self.time) - 1] - self.time[0]
        try:
            if self.duration < 5:
                raise RuntimeWarning
            #print('Duration less than 5 seconds, Accuracy may be affected')
        except RuntimeWarning:
            logging.error('Duration is less than 5 seconds, calculation accuracy may be affected.')

        self.peakdetect()


    def peakdetect(self):


        if self.time == [] or self.voltage == []:
            logging.warning("Time and/or Voltage of " + self.filename +" is empty")
            return

        voltage = pd.Series(data = self.voltage)
        fs = 1/(self.time[1] - self.time[0])
        hrw = 0.5
        mov_avg = voltage.rolling(int(hrw * fs)).mean()
        avg_hr = (np.mean(voltage))
        mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
        mov_avg = [(x+abs(avg_hr-abs(self.minV/2)))*1.2 for x in mov_avg]
        #mov_avg = [(x+avg_hr)*1.2 for x in mov_avg]
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
                    beatposition = listpos - len(window) + (window.index(max(window)))
                    peaklist.append(beatposition)
                    window = []
            else:
                beatposition = listpos - len(window) + (window.index(max(window)))
                peaklist.append(beatposition)
                window = []
                listpos += 1

        ybeat = self.beat_voltage(peaklist,voltage)
        RR_list = self.find_RR(peaklist,fs)
        self.calc_bpm(RR_list)
        self.find_beat_time(peaklist,fs)

        # plt.plot(voltage, alpha=0.5, color='blue', label="raw signal")
        # plt.plot(mov_avg, color ='green', label="moving average")
        # plt.scatter(peaklist, ybeat, color='red', label="average: %.1f BPM" %self.hrm)
        # plt.legend(loc=4, framealpha=0.6)
        # plt.show()
        #print(peaklist)
        #print(self.hrm)

    def beat_voltage(self,peaklist,voltage):
        ybeat = [voltage[x] for x in peaklist]
        return ybeat

    def find_RR(self,peaklist,fs):
        RR_list = []
        cnt = 0
        while (cnt < (len(peaklist) - 1)):
            RR_interval = (peaklist[cnt + 1] - peaklist[cnt])
            ms_dist = ((RR_interval / fs) * 1000.0)
            RR_list.append(ms_dist)
            cnt += 1

        return RR_list

    def calc_bpm(self,RR_list):
        self.hrm = 60000 / np.mean(RR_list)
        self.numbeats = len(RR_list)
        return self.hrm, self.numbeats


    def find_beat_time(self,peaklist,fs):
        beats = []
        for row in peaklist:
            self.beattimes.append(float(row)/fs)
            beats.append(float(row)/fs)
        return beats









def main():
    try:
        x = ECG_data('sine.csv')
    except IOError:
        print('main: File not Found')
        return
    except RuntimeError:
        print('Error in data found. Refer to log')
        return

    print(x.time)
    print(x.voltage)
    print(x.duration)
    print(x.maxV)
    print(x.minV)
    print(x.beattimes)
    print(x.hrm)
    print(x.numbeats)

if __name__ == "__main__":
    main()