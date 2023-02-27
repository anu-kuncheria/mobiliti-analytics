import pandas as pd
import matplotlib.pyplot as plt

def basic_check1(legs):
    trips = len(legs)
    print("Number of trips legs = ", trips)
    print('---------------')
    print ("Trips by purpose (%)", legs['purpose'].value_counts()*100/trips )
    print('---------------')
    print ("Trips Energy category (%)", legs['energy cat.'].value_counts()*100/trips )
    print('---------------')

def basic_check2(legs):
    print(" ====== Started converting to date time ======")
    legs['startt'] = pd.to_datetime(legs['start time (actual)'],errors = 'coerce',format = "%d:%H:%M:%S.%f")
    legs['startt_hr'] = legs['startt'].dt.hour
    plt.figure()
    legs.groupby(['startt_hr'])['leg id'].count().plot.bar()
    plt.title("Distribution of trips by start time")

def basic_check3(flow):
    print("Number of links with traffic = ", len(flow))
    print('---------------')
    plt.figure()
    flow.iloc[:, 1:].sum().plot()
    plt.xlabel("Time of day")
    plt.ylabel("Sum of flows")
    plt.title("Sum of flows by time of day")




