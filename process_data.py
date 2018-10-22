from file_io import read_data
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

class ECG_data:

    def __init__(self,filename_in):


        self.time, self.voltage = read_data(filename_in)
        self.filename = filename_in
        self.maxV = max(self.voltage)
        self.minV = min(self.voltage)
        self.duration = self.time[len(self.time)-1]
        self.hrm = []
        self.beattimes = []

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
                    maximum = max(window)
                    beatposition = listpos - len(window) + (window.index(max(window)))
                    peaklist.append(beatposition)
                    window = []
            else:
                maximum = max(window)
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
        ybeat = measures['ybeat']

        plt.plot(voltage, alpha=0.5, color='blue', label="raw signal")
        plt.plot(mov_avg, color ='green', label="moving average")
        plt.scatter(peaklist, ybeat, color='red', label="average: %.1f BPM" %measures['bpm'])
        plt.legend(loc=4, framealpha=0.6)
        plt.show()
        print(measures['peaklist'])
        print(measures['bpm'])




def main():
    x = ECG_data('./test_data/test_data1.csv')
    print(x.time)
    print(x.voltage)
    print(x.duration)
    print(x.maxV)
    print(x.minV)
    y = x.peakdetect()
    print(y)

if __name__ == "__main__":
    main()