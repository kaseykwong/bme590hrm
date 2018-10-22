from file_io import read_data

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import logging
class ECG_data:

    def __init__(self,filename_in):
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

        self.time, self.voltage = read_data(self.filename)
        #self.time = []
        #self.voltage = []
        #self.data_in()
        self.maxV = max(self.voltage)
        self.minV = min(self.voltage)
        self.duration = self.time[len(self.time)-1] - self.time[0]
        self.hrm = []
        self.beattimes = []
        self.numbeats = 0

        self.peakdetect()

    # def data_in(self):
    #     try:
    #         t , v = read_data(self.filename)
    #             if t is False or v is False:
    #                 logging.warning("File Not Found")
    #                 raise
    #                 return
    #     else:
    #         self.time = t
    #         self.voltage = v

    def peakdetect(self):
        """

        :return: array of peak locations
        """
        measures = {}
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
        measures['peaklist'] = peaklist
        measures['ybeat'] = [voltage[x] for x in peaklist]
        RR_list = []
        peaklist = measures['peaklist']
        cnt = 0
        while (cnt < (len(peaklist) - 1)):
            RR_interval = (peaklist[cnt + 1] - peaklist[cnt])
            ms_dist = ((RR_interval / fs) * 1000.0)
            RR_list.append(ms_dist)
            cnt += 1
        measures['RR_list'] = RR_list
        RR_list = measures['RR_list']
        measures['bpm'] = 60000 / np.mean(RR_list)
        peaklist = measures['peaklist']
        for row in peaklist:
            self.beattimes.append(float(row)/fs)

        self.hrm = measures['bpm']
        self.numbeats = len(RR_list)
        ybeat = measures['ybeat']

        plt.plot(voltage, alpha=0.5, color='blue', label="raw signal")
        plt.plot(mov_avg, color ='green', label="moving average")
        plt.scatter(peaklist, ybeat, color='red', label="average: %.1f BPM" %measures['bpm'])
        plt.legend(loc=4, framealpha=0.6)
        plt.show()
        print(measures['peaklist'])
        print(measures['bpm'])

    def check_data(self):
        if self.time == [] or self.voltage == []:
            logging.warning("Time and voltage inputs are empty.")
            return




def main():
    x = ECG_data('./test_data/test_data1.csv')
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