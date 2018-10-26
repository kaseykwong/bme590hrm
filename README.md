# bme590hrm
Python program to detect heart rate values from ECG data

Author: Kasey Kwong

This program takes input csv files with time and voltage data.

Creates a .json output file with BPM, Voltage Extremes (min and max), Number of beats, Duration of the ECG signal, Voltage and Time of R peaks.
Peak detection algorithm adapted from Paul van Gent. This algorithm uses a windowed moving average to create a threshold where peaks above the 
threshold are counted as heart beat peaks. 

How to use code:
```
Create Virtual Environment
Install requirements.txt
Change filename in process_data.main()
Run process_data.py in python3

```

Files:
- file_io.py: Includes functions to read and parse time and voltage data from input csv file, check that input values are correct type, and write .json files
- process_data.py: Includes functions to process the raw ECG data, obtaining the mean heart rate, total number of beats, the corresponding times of each beat, duration of the ECG test.
- test_file_io.py: Unit testing for file_io.py
- test_process_data.py: Unit Testing for process_data.py


Travis CI Status: [![Build Status](https://travis-ci.com/kaseykwong/bme590hrm.svg?branch=master)](https://travis-ci.com/kaseykwong/bme590hrm)